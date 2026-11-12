"""Cursor PreToolUse journal hook loads the active branch only."""

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
    payload_out = json.loads(completed.stdout)
    text = payload_out.get("additional_context") or ""
    nested = (payload_out.get("hookSpecificOutput") or {}).get("additionalContext") or ""
    if text:
        _assert(nested == text, "nested additionalContext drifted")
        _assert(payload_out.get("continue") is True, "continue was not true")
    return payload_out


def _fill_templates(tmp: Path, work_id: str) -> Path:
    shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
    base = tmp / "journals" / "work-items" / work_id
    shutil.copytree(ROOT / "journals" / "work-items" / "_TEMPLATE", base)
    expert = tmp / "journals" / "expert" / "progress.md"
    expert_text = expert.read_text(encoding="utf-8")
    expert.write_text(
        expert_text.replace("**Current work item:**", f"**Current work item:** {work_id}"),
        encoding="utf-8",
    )
    progress = base / "progress.md"
    progress_text = progress.read_text(encoding="utf-8")
    if "**Work item record:** work-items/" in progress_text:
        progress_text = progress_text.replace(
            "**Work item record:** work-items/",
            f"**Work item record:** work-items/{work_id}/",
        )
    progress.write_text(progress_text, encoding="utf-8")
    (base / "nodes" / "work-item.md").write_text(
        "ROOT_NOTE\n\n**Next action:** intake\n", encoding="utf-8"
    )
    (base / "nodes" / "spec.md").write_text(
        "ACTIVE_BRANCH_NOTE\n\n**Next action:** pack\n", encoding="utf-8"
    )
    (base / "nodes" / "implement.md").write_text("INACTIVE_BRANCH_NOTE\n", encoding="utf-8")
    (base / "state.json").write_text(
        json.dumps(
            {
                "active": ["work-item", "spec"],
                "nodes": {
                    "work-item": {"parent": None, "status": "open", "history": []},
                    "spec": {"parent": "work-item", "status": "open", "history": []},
                    "implement": {"parent": "work-item", "status": "open", "history": []},
                },
            }
        ),
        encoding="utf-8",
    )
    return base


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-journal-"))
    try:
        (tmp / ".claude").mkdir(parents=True, exist_ok=True)
        base = _fill_templates(tmp, "WID-1")

        # No pointer files: work item found only from the expert journal line.
        loaded = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        body = loaded.get("additional_context") or ""
        _assert("WID-1" in body, "expert journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")
        _assert("Completion status" in body, "work item journal missing")

        reading = _run(
            {
                "tool_name": "Read",
                "tool_input": {"file_path": "journals/work-items/WID-1/nodes/spec.md"},
            },
            tmp,
        )
        read_body = reading.get("additional_context") or ""
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")

        reading_path = _run(
            {
                "tool_name": "Read",
                "tool_input": {"path": "journals/work-items/WID-1/nodes/spec.md"},
            },
            tmp,
        )
        path_body = reading_path.get("additional_context") or ""
        _assert("ACTIVE_BRANCH_NOTE" not in path_body, "active note injected onto a path read")

        # Done case: edit the template's own **Completion status:** line.
        progress = base / "progress.md"
        text = progress.read_text(encoding="utf-8")
        text = text.replace(
            "**Completion status:** not started", "**Completion status:** done"
        )
        progress.write_text(text, encoding="utf-8")
        done = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        done_body = done.get("additional_context") or ""
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert("Completion status" in done_body, "done work item journal missing")
        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
