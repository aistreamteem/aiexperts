"""Claude PreToolUse rules hook matches doc/CSV writes; no config:change."""

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
    if not completed.stdout.strip():
        return {}
    return json.loads(completed.stdout)


def _ctx(payload: dict) -> str:
    return (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""


def main() -> int:
    cases = [
        ("Write", "work/arrivals.csv", "", ["write:csv"]),
        ("Write", "out/pack.md", "", ["write:doc"]),
        ("Write", "docs/note.html", "", ["write:doc"]),
        ("Write", "notes/summary.txt", "", ["write:doc"]),
        ("Write", "db/migrations/add_user.sql", "", []),
        ("Shell", "", "gh pr create --title t", []),
        ("Shell", "", "git -C repo push origin HEAD", []),
        ("Shell", "", "git commit -m msg", []),
        ("Shell", "", "npm run build --config webpack.js", []),
        ("Shell", "", "git config user.name x", []),
    ]
    for tool, path, command, expected in cases:
        got = classify(tool, path, command)
        _assert(got == expected, f"{tool} {path or command}: expected {expected}, got {got}")

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
            "write:csv": [
                {
                    "title": "Csv",
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
                "tool_name": "Edit",
                "tool_input": {"file_path": "work-items\\WID-1\\out\\pack.md"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in _ctx(doc), "doc rule missing")

        csv = _run(
            {
                "tool_name": "Write",
                "tool_input": {"file_path": "work-items\\WID-1\\work\\arrivals.csv"},
            },
            tmp,
        )
        _assert("CSV_RULE_BODY" in _ctx(csv), "csv rule missing")

        quiet = _run(
            {"tool_name": "Read", "tool_input": {"file_path": "README.md"}},
            tmp,
        )
        _assert(not _ctx(quiet), "read injected a rule")

        quiet_config = _run(
            {
                "tool_name": "Bash",
                "tool_input": {"command": "npm run build --config webpack.js"},
            },
            tmp,
        )
        _assert(not _ctx(quiet_config), "config substring injected a rule")
    print("claude rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
