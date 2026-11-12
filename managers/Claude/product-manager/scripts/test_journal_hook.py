"""Claude PreToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "inject_journal_context.py"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _set_field(text: str, name: str, value: str) -> str:
    needle = f"**{name}:**"
    lines = []
    replaced = False
    for line in text.splitlines():
        if line.startswith(needle):
            lines.append(f"{needle} {value}")
            replaced = True
        else:
            lines.append(line)
    if not replaced:
        raise SystemExit(f"template missing field {name}")
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def _run(payload: dict, workspace: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr or completed.stdout or "hook failed")
    if not completed.stdout.strip():
        return {}
    return json.loads(completed.stdout)


def _context(result: dict) -> str:
    return result.get("hookSpecificOutput", {}).get("additionalContext", "")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-journal-"))
    try:
        shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
        wi_src = ROOT / "journals" / "work-items" / "_TEMPLATE"
        wi = tmp / "journals" / "work-items" / "WID-1"
        shutil.copytree(wi_src, wi)
        (tmp / ".claude").mkdir(parents=True, exist_ok=True)

        expert = tmp / "journals" / "expert" / "progress.md"
        expert.write_text(
            _set_field(expert.read_text(encoding="utf-8"), "Current work item", "WID-1"),
            encoding="utf-8",
        )
        progress = wi / "progress.md"
        progress.write_text(
            _set_field(progress.read_text(encoding="utf-8"), "Completion status", "in progress"),
            encoding="utf-8",
        )
        (wi / "state.json").write_text(
            json.dumps(
                {
                    "active": ["work-item", "intake"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []},
                        "intake": {"parent": "work-item", "status": "open", "history": []},
                        "charter": {"parent": "work-item", "status": "open", "history": []},
                    },
                }
            ),
            encoding="utf-8",
        )
        (wi / "nodes" / "work-item.md").write_text("ROOT_NOTE\n", encoding="utf-8")
        (wi / "nodes" / "intake.md").write_text("ACTIVE_BRANCH_NOTE\n", encoding="utf-8")
        (wi / "nodes" / "charter.md").write_text("INACTIVE_BRANCH_NOTE\n", encoding="utf-8")

        # No pointer files: work item comes only from the expert journal line.
        body = _context(_run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp))
        _assert("Premise and goal" in body or "Current work item" in body, "expert journal missing")
        _assert("WORK_ITEM" in body or "Completion status" in body or "Work item" in body, "work item journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        read_body = _context(
            _run(
                {
                    "tool_name": "Read",
                    "tool_input": {"file_path": "journals/work-items/WID-1/nodes/intake.md"},
                },
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")
        _assert("Current work item" in read_body or "Premise and goal" in read_body, "expert journal dropped")

        progress.write_text(
            _set_field(progress.read_text(encoding="utf-8"), "Completion status", "done"),
            encoding="utf-8",
        )
        done_body = _context(_run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp))
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert("Completion status" in done_body or "Work item" in done_body, "done work item journal missing")

        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
