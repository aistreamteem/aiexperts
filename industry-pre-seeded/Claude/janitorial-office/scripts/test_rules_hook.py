"""Claude PreToolUse rules hook matches file/sheet/doc writes; no config:change."""

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
    sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
    import inject_rules_on_action as rules  # noqa: E402

    cases = [
        ("Write", "work-items/WID-1/out/pack.md", "", ["write:file", "write:doc"]),
        ("Write", "work-items/WID-1/work/par.csv", "", ["write:file", "write:sheet"]),
        ("Write", "docs/note.html", "", ["write:file", "write:doc"]),
        ("Write", "work/onhand.xlsx", "", ["write:file", "write:sheet"]),
        ("Write", "db/migrations/add_user.sql", "", ["write:file"]),
        ("Shell", "", "git commit -m hello", []),
        ("Shell", "", "git config user.name x", []),
        ("Shell", "", "npm run build --config webpack.js", []),
        ("Shell", "", "copy out/pack.md archive/", ["write:doc"]),
        ("Shell", "", "copy work/par.csv archive/", ["write:sheet"]),
        ("Read", "README.md", "", []),
    ]
    for tool, path, cmd, expected in cases:
        got = rules.classify(tool, path, cmd)
        _assert(got == expected, f"{tool} {path or cmd}: got {got}, expected {expected}")

    with tempfile.TemporaryDirectory(prefix="claude-rules-") as tmp_name:
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
            "write:sheet": [
                {
                    "title": "Sheet",
                    "file": "facts/rules-operations.md",
                    "line": 2,
                    "body": "SHEET_RULE_BODY",
                }
            ],
            "write:file": [
                {
                    "title": "File",
                    "file": "facts/rules-operations.md",
                    "line": 3,
                    "body": "FILE_RULE_BODY",
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
        ctx = doc.get("additional_context", "")
        _assert("DOC_RULE_BODY" in ctx, "doc rule missing")
        _assert("FILE_RULE_BODY" in ctx, "file rule missing on doc write")
        _assert(doc.get("continue") is True, "doc continue missing")

        sheet = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\WID-1\\work\\par.csv"},
            },
            tmp,
        )
        sctx = sheet.get("additional_context", "")
        _assert("SHEET_RULE_BODY" in sctx, "sheet rule missing")
        _assert("FILE_RULE_BODY" in sctx, "file rule missing on sheet write")

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
