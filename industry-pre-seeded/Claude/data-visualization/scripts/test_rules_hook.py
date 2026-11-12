"""Claude PreToolUse rules hook matches Shell and StrReplace actions."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"

# Import classify / KNOWN_TOKENS from the hook module under test.
sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
import inject_rules_on_action as rules_hook  # noqa: E402


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
    # Classifier table cases (role vocabulary).
    cases = [
        ("Write", "work/plot.py", "", ["write:python"]),
        ("Write", "work/values.csv", "", ["write:csv"]),
        ("Write", "out/chart.png", "", ["write:chart"]),
        ("Write", "out/writeup.md", "", ["write:doc"]),
        ("Shell", "", "python plot.py && matplotlib savefig", ["write:chart", "write:python"]),
        ("Shell", "", "npm run build --config webpack.js", []),
    ]
    for tool, path, command, expected in cases:
        got = rules_hook.classify(tool, path, command)
        _assert(
            got == expected,
            f"classify({tool!r}, {path!r}, {command!r}) => {got!r}, expected {expected!r}",
        )
    _assert("write:doc" in rules_hook.KNOWN_TOKENS, "write:doc missing from KNOWN_TOKENS")
    _assert("config:change" not in rules_hook.KNOWN_TOKENS, "config:change must stay dropped")

    with tempfile.TemporaryDirectory(prefix="claude-rules-") as tmp_name:
        tmp = Path(tmp_name)
        index = {
            "write:python": [
                {
                    "title": "Python",
                    "file": "facts/rules-operations.md",
                    "line": 1,
                    "body": "PYTHON_RULE_BODY",
                }
            ],
            "write:chart": [
                {
                    "title": "Chart",
                    "file": "facts/rules-operations.md",
                    "line": 2,
                    "body": "CHART_RULE_BODY",
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
        (facts / "trigger-index.json").write_text(json.dumps(index), encoding="utf-8")

        py = _run(
            {
                "tool_name": "StrReplace",
                "tool_input": {"path": "work-items\\WID-1\\work\\plot.py"},
            },
            tmp,
        )
        _assert("PYTHON_RULE_BODY" in py.get("additional_context", ""), "python rule missing")
        _assert(py.get("continue") is True, "python continue missing")

        chart = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\WID-1\\out\\sales-by-week.png"},
            },
            tmp,
        )
        _assert(
            "CHART_RULE_BODY" in chart.get("additional_context", ""),
            "chart rule missing",
        )

        doc = _run(
            {
                "tool_name": "Write",
                "tool_input": {"path": "work-items\\WID-1\\out\\writeup.md"},
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
