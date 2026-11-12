"""Claude PreToolUse rules hook matches write/edit actions for this role."""

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
    # Classifier table cases (role + generic vocabulary; no config:change)
    cases = [
        ("Write", "db/foo.sql", "", ["write:sql", "sql:generate"]),
        ("Write", "docs/note.md", "", ["write:doc"]),
        ("Write", "page.html", "", ["write:doc"]),
        ("Write", "work/assignment.csv", "", ["write:csv"]),
        ("Write", "out/estimate-pack.md", "", ["write:doc", "write:estimate"]),
        ("Shell", "", "gh pr create --title t", ["pr:open"]),
        ("Shell", "", "git -C repo push origin HEAD", ["git:push"]),
        ("Shell", "", "git -C repo commit -m msg", ["git:commit"]),
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
            "write:doc": [
                {
                    "title": "Doc",
                    "file": "facts/rules-shared.md",
                    "line": 1,
                    "body": "DOC_RULE_BODY",
                }
            ],
            "write:csv": [
                {
                    "title": "Csv",
                    "file": "facts/rules-shared.md",
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
                "tool_input": {"path": "work-items\\ro-2104\\out\\intake.md"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in doc.get("additional_context", ""), "doc rule missing")
        _assert(doc.get("continue") is True, "doc continue missing")

        csv = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\ro-2104\\work\\assignment.csv"},
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
    print("claude rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
