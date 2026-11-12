"""Cursor preToolUse rules hook matches sheet/pack/intake writes."""

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


def _classify(tool_name: str, file_path: str, command: str = "") -> list[str]:
    ns: dict = {}
    exec(HOOK.read_text(encoding="utf-8"), ns)
    return ns["classify"](tool_name, file_path, command)


def main() -> int:
    _assert(
        _classify("Write", "work/prep.csv") == ["write:sheet"],
        "csv should be write:sheet",
    )
    _assert(
        "write:pack" in _classify("Write", "out/prep.md"),
        "out md should be write:pack",
    )
    _assert(
        "file:intake" in _classify("Write", "in/count.csv"),
        "in path should be file:intake",
    )
    _assert(
        _classify("Shell", "", "py docs/tools/checks/csv-has-columns.py x.csv")
        == ["write:sheet"],
        "check script should be write:sheet",
    )
    _assert(
        _classify("Shell", "", "npm run build --config webpack.js") == [],
        "config in command must not fire",
    )
    _assert(_classify("Shell", "", "git commit -m x") == [], "git commit quiet")

    with tempfile.TemporaryDirectory(prefix="cursor-rules-") as tmp_name:
        tmp = Path(tmp_name)
        index = {
            "write:sheet": [
                {
                    "title": "Sheet",
                    "file": "facts/rules-operations.md",
                    "line": 1,
                    "body": "SHEET_RULE_BODY",
                }
            ],
            "write:pack": [
                {
                    "title": "Pack",
                    "file": "facts/rules-operations.md",
                    "line": 2,
                    "body": "PACK_RULE_BODY",
                }
            ],
            "file:intake": [
                {
                    "title": "Intake",
                    "file": "facts/rules-operations.md",
                    "line": 3,
                    "body": "INTAKE_RULE_BODY",
                }
            ],
        }
        facts = tmp / "facts"
        facts.mkdir()
        (facts / "trigger-index.json").write_text(
            json.dumps(index), encoding="utf-8"
        )

        sheet = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "work\\prep.csv"},
            },
            tmp,
        )
        _assert("SHEET_RULE_BODY" in sheet.get("additional_context", ""), "sheet rule missing")
        _assert(sheet.get("continue") is True, "sheet continue missing")

        pack = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "out\\prep.md"},
            },
            tmp,
        )
        _assert(
            "PACK_RULE_BODY" in pack.get("additional_context", ""),
            "pack rule missing",
        )

        intake = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "in\\count.csv"},
            },
            tmp,
        )
        _assert(
            "INTAKE_RULE_BODY" in intake.get("additional_context", ""),
            "intake rule missing",
        )

        quiet = _run(
            {"tool_name": "Read", "tool_input": {"path": "README.md"}},
            tmp,
        )
        _assert("additional_context" not in quiet, "read injected a rule")
        _assert(quiet.get("continue") is True, "read continue missing")

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
    print("cursor rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
