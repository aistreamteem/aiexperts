"""Cursor preToolUse rules hook matches write:doc and write:csv for this role."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"


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
    # Import classifier table for direct unit checks.
    sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
    import inject_rules_on_action as rules  # noqa: E402

    cases = [
        ("Write", "out/day-list.md", "", ["write:doc"]),
        ("Write", "out/recall.csv", "", ["write:csv"]),
        ("Write", "docs/note.html", "", ["write:doc"]),
        ("Write", "db/foo.sql", "", []),
        ("Shell", "", "npm run build --config webpack.js", []),
        ("Shell", "", "git commit -m hello", []),
        ("Read", "README.md", "", []),
    ]
    for tool, path, command, expected in cases:
        got = rules.classify(tool, path, command)
        _assert(
            got == expected,
            f"classify({tool!r}, {path!r}, {command!r}) -> {got}, expected {expected}",
        )

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
        (facts / "trigger-index.json").write_text(json.dumps(index), encoding="utf-8")

        doc = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "work-items\\WID-1\\out\\day-list.md"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in doc.get("additional_context", ""), "doc rule missing")
        _assert(doc.get("continue") is True, "doc continue missing")

        csv = _run(
            {
                "tool_name": "Write",
                "tool_input": {"file_path": "work-items/WID-1/out/recall.csv"},
            },
            tmp,
        )
        _assert("CSV_RULE_BODY" in csv.get("additional_context", ""), "csv rule missing")

        quiet = _run(
            {"tool_name": "Read", "tool_input": {"path": "README.md"}},
            tmp,
        )
        _assert("additional_context" not in quiet, "read injected a rule")
        _assert(quiet.get("continue") is True, "read continue missing")

        no_config = _run(
            {
                "tool_name": "Shell",
                "tool_input": {"command": "npm run build --config webpack.js"},
            },
            tmp,
        )
        _assert("additional_context" not in no_config, "config substring fired a token")

    print("cursor rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
