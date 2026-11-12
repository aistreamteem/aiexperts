"""Cursor preToolUse rules hook matches write/edit actions for this role."""

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
    # Classifier table cases for this role (write:doc; no config:change / git / sql)
    cases = [
        ("Write", "work-items/ro-1/out/ro-writeup.md", "", ["write:doc"]),
        ("Write", "docs/note.markdown", "", ["write:doc"]),
        ("Write", "out/pack.html", "", ["write:doc"]),
        ("Write", "work/parts.csv", "", ["write:doc"]),
        ("Shell", "", "npm run build --config webpack.js", []),
        ("Shell", "", "git config user.name x", []),
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
            "write:doc": [
                {
                    "title": "Doc",
                    "file": "facts/rules-operations.md",
                    "line": 1,
                    "body": "DOC_RULE_BODY",
                }
            ],
        }
        facts = tmp / "facts"
        facts.mkdir()
        (facts / "trigger-index.json").write_text(
            json.dumps(index), encoding="utf-8"
        )

        md = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "work-items\\ro-5521\\out\\ro-writeup.md"},
            },
            tmp,
        )
        _assert("DOC_RULE_BODY" in md.get("additional_context", ""), "doc rule missing")
        _assert(md.get("continue") is True, "doc continue missing")

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
