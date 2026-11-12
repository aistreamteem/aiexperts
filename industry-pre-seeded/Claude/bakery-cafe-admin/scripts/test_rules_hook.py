"""Claude PreToolUse rules hook matches bakery-cafe write and check actions."""

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
    # Classifier table cases (no index needed)
    sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
    import inject_rules_on_action as rules  # noqa: E402

    cases = [
        ("Write", "work/bake-list.csv", "", ["write:sheet"]),
        ("Write", "out/bake-list-day.md", "", ["write:pack"]),
        ("Write", "in/standing.csv", "", ["file:intake", "write:sheet"]),
        ("Write", "work/notes.md", "", ["write:pack"]),
        ("Shell", "", "py -3 docs/tools/checks/csv-has-columns.py work/x.csv", ["write:sheet"]),
        ("Shell", "", "npm run build --config webpack.js", []),
        ("Read", "README.md", "", []),
    ]
    for tool, path, command, expected in cases:
        got = rules.classify(tool, path, command)
        _assert(
            got == expected,
            f"classify({tool!r}, {path!r}, {command!r}) -> {got!r}, want {expected!r}",
        )

    with tempfile.TemporaryDirectory(prefix="claude-rules-") as tmp_name:
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
        (facts / "trigger-index.json").write_text(json.dumps(index), encoding="utf-8")

        sheet = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "work\\bake-list.csv"},
            },
            tmp,
        )
        _assert("SHEET_RULE_BODY" in sheet.get("additional_context", ""), "sheet rule missing")
        _assert(sheet.get("continue") is True, "sheet continue missing")

        pack = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "out\\bake-list-day.md"},
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
                "tool_input": {"path": "in\\orders.csv"},
            },
            tmp,
        )
        ctx = intake.get("additional_context", "")
        _assert("INTAKE_RULE_BODY" in ctx, "intake rule missing")
        _assert("SHEET_RULE_BODY" in ctx, "intake sheet rule missing")

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
