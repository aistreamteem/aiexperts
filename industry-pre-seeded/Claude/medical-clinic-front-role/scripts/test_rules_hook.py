"""Claude PreToolUse rules hook matches CSV/pack/doc writes for medical-clinic-front-role."""

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
    cases = [
        ("Write", "work/check-in.csv", "", ["write:csv"]),
        ("Write", "work-items/WID-1/out/pack-note.md", "", ["write:pack", "write:doc"]),
        ("Write", "notes/summary.md", "", ["write:doc"]),
        ("Write", "docs/page.html", "", ["write:doc"]),
        ("Write", "work/flags.xlsx", "", ["write:csv"]),
        ("Shell", "", "python docs/tools/checks/file-exists.py work/x.csv", ["write:csv"]),
        ("Shell", "", "npm run build --config webpack.js", []),
        ("Shell", "", "git config user.name x", []),
    ]
    for tool, path, command, expected in cases:
        got = classify(tool, path, command)
        _assert(
            got == expected,
            f"{tool} {path or command}: expected {expected}, got {got}",
        )

    with tempfile.TemporaryDirectory(prefix="claude-rules-") as tmp_name:
        tmp = Path(tmp_name)
        index = {
            "write:csv": [
                {
                    "title": "CSV",
                    "file": "facts/rules-operations.md",
                    "line": 1,
                    "body": "CSV_RULE_BODY",
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
            "write:doc": [
                {
                    "title": "Doc",
                    "file": "facts/rules-operations.md",
                    "line": 3,
                    "body": "DOC_RULE_BODY",
                }
            ],
        }
        facts = tmp / "facts"
        facts.mkdir()
        (facts / "trigger-index.json").write_text(
            json.dumps(index), encoding="utf-8"
        )

        csv = _run(
            {
                "tool_name": "Edit",
                "tool_input": {"path": "work-items\\WID-1\\work\\coded.csv"},
            },
            tmp,
        )
        _assert("CSV_RULE_BODY" in csv.get("additional_context", ""), "csv rule missing")
        _assert(csv.get("continue") is True, "csv continue missing")

        pack = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items/WID-1/out/pack-note.md"},
            },
            tmp,
        )
        _assert(
            "PACK_RULE_BODY" in pack.get("additional_context", ""),
            "pack rule missing",
        )

        doc = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items/WID-1/work/notes.md"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in doc.get("additional_context", ""), "doc rule missing")

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
