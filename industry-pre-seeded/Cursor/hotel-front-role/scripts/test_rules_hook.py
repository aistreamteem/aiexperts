"""Cursor preToolUse rules hook matches doc/CSV writes; no config:change."""

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
                "tool_input": {"path": "work-items\\WID-1\\out\\pack.md"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in doc.get("additional_context", ""), "doc rule missing")

        html = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\WID-1\\out\\index.html"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in html.get("additional_context", ""), "html doc rule missing")

        csv = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\WID-1\\work\\arrivals.csv"},
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
            {
                "tool_name": "Shell",
                "tool_input": {"command": "npm run build --config webpack.js"},
            },
            tmp,
        )
        _assert("additional_context" not in quiet_config, "config substring injected a rule")

        quiet_commit = _run(
            {"tool_name": "Shell", "tool_input": {"command": "git commit -m hello"}},
            tmp,
        )
        _assert("additional_context" not in quiet_commit, "git commit injected a rule")

        quiet = _run(
            {"tool_name": "Read", "tool_input": {"path": "README.md"}},
            tmp,
        )
        _assert("additional_context" not in quiet, "read injected a rule")
        _assert(quiet.get("continue") is True, "read continue missing")
    print("cursor rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
