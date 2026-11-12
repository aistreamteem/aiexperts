"""Claude PreToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _context(payload: dict) -> str:
    text = payload.get("additional_context") or ""
    nested = (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""
    _assert(bool(text), "additional_context missing")
    _assert(nested == text, "nested additionalContext drifted")
    _assert(payload.get("continue") is True, "continue was not true")
    return text


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run_hook(payload: dict, workspace: Path) -> dict:
    hook = str(ROOT / ".claude" / "hooks" / "inject_journal_context.py")
    completed = subprocess.run(
        [sys.executable, hook],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or "hook failed")
    if not completed.stdout.strip():
        return {}
    return json.loads(completed.stdout)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-journal-"))
    try:
        shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
        wi_src = ROOT / "journals" / "work-items" / "_TEMPLATE"
        wi = tmp / "journals" / "work-items" / "WID-1"
        shutil.copytree(wi_src, wi)
        (tmp / ".claude").mkdir(parents=True, exist_ok=True)

        expert = tmp / "journals" / "expert" / "progress.md"
        expert_text = expert.read_text(encoding="utf-8")
        expert_text = expert_text.replace(
            "**Current work item:**",
            "**Current work item:** WID-1",
            1,
        )
        expert.write_text(expert_text, encoding="utf-8")

        progress = wi / "progress.md"
        progress_text = progress.read_text(encoding="utf-8")
        progress_text = progress_text.replace(
            "**Work item record:** work-items/",
            "**Work item record:** work-items/WID-1/",
            1,
        )
        progress_text = progress_text.replace(
            "**Completion status:** not started",
            "**Completion status:** in progress",
            1,
        )
        progress.write_text(progress_text, encoding="utf-8")

        _write(
            wi / "state.json",
            json.dumps(
                {
                    "active": ["work-item", "chart"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []},
                        "chart": {"parent": "work-item", "status": "open", "history": []},
                        "pack": {"parent": "work-item", "status": "open", "history": []},
                    },
                }
            ),
        )
        _write(wi / "nodes" / "work-item.md", "ROOT_NOTE\n\n**Next action:** run chart\n")
        _write(wi / "nodes" / "chart.md", "ACTIVE_BRANCH_NOTE\n\n**Next action:** write PNG\n")
        _write(wi / "nodes" / "pack.md", "INACTIVE_BRANCH_NOTE\n")

        # No pointer files: work item found only from the expert journal line.
        loaded = _run_hook(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        body = _context(loaded)
        _assert("WID-1" in body or "Current work item" in body, "expert journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")
        _assert(
            "Completion status" in body or "Work item" in body,
            "work item journal missing",
        )

        reading = _run_hook(
            {
                "tool_name": "Read",
                "tool_input": {"file_path": "journals/work-items/WID-1/nodes/chart.md"},
            },
            tmp,
        )
        read_body = _context(reading)
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")

        reading_path = _run_hook(
            {
                "tool_name": "Read",
                "tool_input": {"path": "journals/work-items/WID-1/nodes/chart.md"},
            },
            tmp,
        )
        path_body = _context(reading_path)
        _assert("ACTIVE_BRANCH_NOTE" not in path_body, "active note injected onto a path read")

        done_text = progress.read_text(encoding="utf-8")
        done_text = done_text.replace(
            "**Completion status:** in progress",
            "**Completion status:** done",
            1,
        )
        progress.write_text(done_text, encoding="utf-8")
        done = _run_hook(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        done_body = _context(done)
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")

        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
