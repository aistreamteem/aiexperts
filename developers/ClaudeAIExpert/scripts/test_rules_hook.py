"""Classifier and PreToolUse rules hook tests."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
from inject_rules_on_action import KNOWN_TOKENS, classify  # noqa: E402

HOOK = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


CASES = [
    ("Shell", "", "git config user.name x", []),
    ("Write", "db/fix.sql", "", ["write:sql", "sql:generate"]),
    ("Write", "docs/report.html", "", ["write:doc"]),
    ("Write", "docs/note.md", "", ["write:doc"]),
    ("Write", "page.htm", "", ["write:doc"]),
    ("Shell", "", "gh pr create --title t", ["pr:open"]),
    ("Shell", "", "git -C repo push origin HEAD", ["git:push"]),
    ("Shell", "", "git -C repo commit -m msg", ["git:commit"]),
    ("Shell", "", "npm run build --config webpack.js", []),
    ("Bash", "", "git push", ["git:push"]),
    ("Edit", "migrations/demo.sql", "", ["write:sql", "sql:generate"]),
]


def main() -> int:
    for tool, path, command, expected in CASES:
        got = classify(tool, path, command)
        _assert(got == expected, f"{tool} {path!r} {command!r}: got {got}, expected {expected}")

    expected_tokens = {
        "write:sql",
        "sql:generate",
        "write:doc",
        "pr:open",
        "git:push",
        "git:commit",
    }
    _assert(set(KNOWN_TOKENS) == expected_tokens, f"unexpected KNOWN_TOKENS: {KNOWN_TOKENS}")

    tmp = Path(tempfile.mkdtemp(prefix="claude-rules-"))
    facts = tmp / "facts"
    facts.mkdir(parents=True)
    (facts / "trigger-index.json").write_text(
        json.dumps(
            {
                "write:sql": [
                    {
                        "title": "SQL rule",
                        "file": "rules-developer.md",
                        "line": 1,
                        "body": "### SQL rule\n\nDo not drop tables.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": "db/x.sql"}}),
        text=True,
        capture_output=True,
        cwd=str(tmp),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or "rules hook failed")
    body = json.loads(completed.stdout)["hookSpecificOutput"]["additionalContext"]
    _assert("Do not drop tables" in body, "rule body missing")
    _assert("write:sql" in body, "trigger label missing")

    no_match = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"tool_name": "Shell", "tool_input": {"command": "git config user.name x"}}),
        text=True,
        capture_output=True,
        cwd=str(tmp),
        check=False,
    )
    _assert(no_match.returncode == 0, "config command should exit 0")
    _assert(not no_match.stdout.strip(), "config:change must not fire")

    print("claude rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
