"""Claude PreToolUse rules hook matches doc/checklist writes for this TC role."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
from inject_rules_on_action import classify  # noqa: E402


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
    # Classifier table cases (role vocabulary).
    cases = [
        ("Write", "work/out/dates-calendar.md", "", ["write:doc"]),
        ("Write", "work/missing-docs.csv", "", ["write:checklist"]),
        ("Write", "db/migrations/add_user.sql", "", []),
        ("Shell", "", "git commit -m hello", []),
        ("Shell", "", "npm run build --config webpack.js", []),
        ("Shell", "", "py -3 work/export.csv", ["write:checklist"]),
        ("Read", "README.md", "", []),
    ]
    for tool, path, command, expected in cases:
        got = classify(tool, path, command)
        _assert(
            got == expected,
            f"{tool} {path or command!r}: expected {expected}, got {got}",
        )

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
            "write:checklist": [
                {
                    "title": "Checklist",
                    "file": "facts/rules-operations.md",
                    "line": 2,
                    "body": "CHECKLIST_RULE_BODY",
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

        checklist = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\WID-1\\work\\missing-docs.csv"},
            },
            tmp,
        )
        _assert(
            "CHECKLIST_RULE_BODY" in checklist.get("additional_context", ""),
            "checklist rule missing",
        )

        quiet_sql = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "db\\migrations\\add_user.sql"},
            },
            tmp,
        )
        _assert("additional_context" not in quiet_sql, "sql write injected a rule")

        quiet_commit = _run(
            {"tool_name": "Shell", "tool_input": {"command": "git commit -m hello"}},
            tmp,
        )
        _assert("additional_context" not in quiet_commit, "git commit injected a rule")

        quiet_config = _run(
            {
                "tool_name": "Shell",
                "tool_input": {"command": "npm run build --config webpack.js"},
            },
            tmp,
        )
        _assert(
            "additional_context" not in quiet_config,
            "config substring injected a rule",
        )

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
