"""Cursor preToolUse rules hook matches Shell and StrReplace actions."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
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
    # Classifier table cases (fix 5).
    cases = [
        ("Shell", "", "git config user.name x", []),
        (
            "Write",
            "outputs/fix.sql",
            "",
            ["write:sql", "sql:generate"],
        ),
        ("Write", "notes/readme.md", "", ["write:doc"]),
        ("Write", "docs/page.html", "", ["write:doc"]),
        ("Shell", "", "git -C repo push", ["git:push"]),
        ("Shell", "", "npm run build --config webpack.js", []),
        (
            "Write",
            "docs/walkthrough.html",
            "",
            ["write:doc"],
        ),
        ("Shell", "", "gh pr create --title t", ["pr:open"]),
        ("Shell", "", "git commit -m hello", ["git:commit"]),
        ("Write", "db/migrations/add_user.sql", "", ["write:sql", "sql:generate"]),
        ("Read", "README.md", "", []),
    ]
    for tool, path, command, expected in cases:
        got = classify(tool, path, command)
        _assert(
            got == expected,
            f"classify({tool!r}, {path!r}, {command!r}) -> {got!r}, want {expected!r}",
        )

    with tempfile.TemporaryDirectory(prefix="cursor-rules-") as tmp_name:
        tmp = Path(tmp_name)
        index = {
            "write:sql": [
                {
                    "title": "SQL",
                    "file": "facts/rules-developer.md",
                    "line": 1,
                    "body": "SQL_RULE_BODY",
                }
            ],
            "git:commit": [
                {
                    "title": "Commit",
                    "file": "facts/rules-developer.md",
                    "line": 2,
                    "body": "COMMIT_RULE_BODY",
                }
            ],
        }
        facts = tmp / "facts"
        facts.mkdir()
        (facts / "trigger-index.json").write_text(
            json.dumps(index), encoding="utf-8"
        )

        sql = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "db\\migrations\\add_user.sql"},
            },
            tmp,
        )
        _assert("SQL_RULE_BODY" in sql.get("additional_context", ""), "sql rule missing")
        _assert(sql.get("continue") is True, "sql continue missing")

        commit = _run(
            {"tool_name": "Shell", "tool_input": {"command": "git commit -m hello"}},
            tmp,
        )
        _assert(
            "COMMIT_RULE_BODY" in commit.get("additional_context", ""),
            "commit rule missing",
        )

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
