"""Claude PreToolUse rules hook matches doc/CSV writes; no config:change."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _run(payload: dict, workspace: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or "rules hook failed")
    return json.loads(completed.stdout)


def main() -> int:
    # Unit-level classify checks (table vocabulary for this role).
    sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
    import inject_rules_on_action as rules  # noqa: E402

    cases = [
        ("Write", "work-items/WID-1/out/pack.md", "", ["write:doc"]),
        ("Write", "work-items/WID-1/work/dispatch.csv", "", ["write:csv"]),
        ("Write", "docs/note.html", "", ["write:doc"]),
        ("Write", "db/migrations/add_user.sql", "", []),
        ("Shell", "", "git commit -m hello", []),
        ("Shell", "", "git config user.name x", []),
        ("Shell", "", "npm run build --config webpack.js", []),
        ("Shell", "", "copy out/pack.md archive/", ["write:doc"]),
        ("Read", "README.md", "", []),
    ]
    for tool, path, cmd, expected in cases:
        got = rules.classify(tool, path, cmd)
        _assert(got == expected, f"{tool} {path or cmd}: got {got}, expected {expected}")

    with tempfile.TemporaryDirectory(prefix="cursor-rules-") as tmp_name:
        tmp = Path(tmp_name)
        index = {
            "write:doc": [
                {
                    "title": "Doc",
                    "file": "facts/rules-operations.md",
                    "line": 1,
                    "body": "DOC_RULE_BODY",
                }
            ],
            "write:csv": [
                {
                    "title": "CSV",
                    "file": "facts/rules-operations.md",
                    "line": 2,
                    "body": "CSV_RULE_BODY",
                }
            ],
        }
        facts = tmp / "facts"
        facts.mkdir()
        (facts / "trigger-index.json").write_text(
            json.dumps(index), encoding="utf-8"
        )

        doc = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "work-items\\WID-1\\out\\pack.md"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in doc.get("additional_context", ""), "doc rule missing")
        _assert(doc.get("continue") is True, "doc continue missing")

        csv = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\WID-1\\work\\dispatch.csv"},
            },
            tmp,
        )
        _assert("CSV_RULE_BODY" in csv.get("additional_context", ""), "csv rule missing")

        quiet_sql = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "db\\migrations\\add_user.sql"},
            },
            tmp,
        )
        _assert("additional_context" not in quiet_sql, "sql write injected a rule")

        quiet_config = _run(
            {"tool_name": "Shell", "tool_input": {"command": "git config user.name x"}},
            tmp,
        )
        _assert("additional_context" not in quiet_config, "config:change still firing")

        quiet = _run(
            {"tool_name": "Read", "tool_input": {"path": "README.md"}},
            tmp,
        )
        _assert("additional_context" not in quiet, "read injected a rule")
        _assert(quiet.get("continue") is True, "read continue missing")
    print("claude rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
