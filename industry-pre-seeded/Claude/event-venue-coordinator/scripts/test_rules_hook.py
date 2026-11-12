"""Claude PreToolUse rules hook matches doc/CSV writes for this venue role."""

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


def _run(payload: dict, workspace: Path) -> dict | None:
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
        return None
    return json.loads(completed.stdout)


def _context(payload: dict | None) -> str:
    if not payload:
        return ""
    return (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""


def main() -> int:
    # Classifier table cases (role vocabulary: write:doc, write:csv).
    _assert(
        classify("Write", "work-items/WID-1/out/pack.md", "") == ["write:doc"],
        "md write",
    )
    _assert(
        classify("Write", "work/missing.csv", "") == ["write:csv"],
        "csv write",
    )
    _assert(
        classify("Write", "db/foo.sql", "") == [],
        "sql write stays quiet",
    )
    _assert(
        classify("Shell", "", "git commit -m hello") == [],
        "git commit stays quiet",
    )
    _assert(
        classify("Shell", "", "npm run build --config webpack.js") == [],
        "config string does not fire",
    )
    _assert(
        classify("Shell", "", "python docs/tools/checks/file-exists.py work/a.csv")
        == ["write:csv"],
        "shell csv hint",
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
                    "title": "CSV",
                    "file": "facts/rules-shared.md",
                    "line": 2,
                    "body": "CSV_RULE_BODY",
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
                "tool_name": "Edit",
                "tool_input": {"path": "work-items\\WID-1\\out\\pack.md"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in _context(doc), "doc rule missing")

        csv = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\WID-1\\work\\missing-forms.csv"},
            },
            tmp,
        )
        _assert("CSV_RULE_BODY" in _context(csv), "csv rule missing")

        quiet_sql = _run(
            {
                "tool_name": "Edit",
                "tool_input": {"path": "db\\migrations\\add_user.sql"},
            },
            tmp,
        )
        _assert(quiet_sql is None, "sql write injected a rule")

        quiet_commit = _run(
            {"tool_name": "Bash", "tool_input": {"command": "git commit -m hello"}},
            tmp,
        )
        _assert(quiet_commit is None, "git commit injected a rule")

        quiet = _run(
            {"tool_name": "Read", "tool_input": {"path": "README.md"}},
            tmp,
        )
        _assert(quiet is None, "read injected a rule")
    print("claude rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
