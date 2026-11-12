"""Cursor preToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".cursor" / "hooks" / "inject_journal_context.py"
EXPERT_TEMPLATE = ROOT / "journals" / "_TEMPLATE" / "expert" / "progress.md"
WI_TEMPLATE = ROOT / "journals" / "work-items" / "_TEMPLATE"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _context(stdout: str) -> str:
    payload = json.loads(stdout)
    text = payload.get("additional_context") or ""
    nested = (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""
    _assert(bool(text), "additional_context missing")
    _assert(nested == text, "nested additionalContext drifted")
    _assert(payload.get("continue") is True, "continue was not true")
    return text


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run(payload: dict, workspace: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )


def _fill_templates(tmp: Path, work_id: str, *, completion: str = "in progress") -> Path:
    expert_dir = tmp / "journals" / "expert"
    expert_dir.mkdir(parents=True, exist_ok=True)
    expert_text = EXPERT_TEMPLATE.read_text(encoding="utf-8")
    expert_text = expert_text.replace(
        "**Current work item:**",
        f"**Current work item:** {work_id}",
        1,
    )
    (expert_dir / "progress.md").write_text(expert_text, encoding="utf-8")

    base = tmp / "journals" / "work-items" / work_id
    shutil.copytree(WI_TEMPLATE, base)
    flat = base / "progress.md"
    flat_text = flat.read_text(encoding="utf-8")
    flat_text = flat_text.replace(
        "**Completion status:** not started",
        f"**Completion status:** {completion}",
        1,
    )
    flat.write_text(flat_text, encoding="utf-8")
    _write(
        base / "state.json",
        json.dumps(
            {
                "active": ["work-item", "day-list"],
                "nodes": {
                    "work-item": {"parent": None, "status": "open", "history": []},
                    "day-list": {"parent": "work-item", "status": "open", "history": []},
                    "other": {"parent": "work-item", "status": "open", "history": []},
                },
            }
        ),
    )
    _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n")
    _write(base / "nodes" / "day-list.md", "ACTIVE_BRANCH_NOTE\n")
    _write(base / "nodes" / "other.md", "INACTIVE_BRANCH_NOTE\n")
    return base


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)
        base = _fill_templates(tmp, "WID-1")

        # No pointer files: work item from expert journal bold field only.
        loaded = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        _assert(loaded.returncode == 0, loaded.stderr or "hook failed")
        body = _context(loaded.stdout)
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")
        _assert("**Current work item:** WID-1" in body or "WID-1" in body, "expert journal missing")

        reading = _run(
            {
                "tool_name": "Read",
                "tool_input": {"file_path": "journals/work-items/WID-1/nodes/day-list.md"},
            },
            tmp,
        )
        read_body = _context(reading.stdout)
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")

        reading_path = _run(
            {
                "tool_name": "Read",
                "tool_input": {"path": "journals/work-items/WID-1/nodes/day-list.md"},
            },
            tmp,
        )
        path_body = _context(reading_path.stdout)
        _assert("ACTIVE_BRANCH_NOTE" not in path_body, "active note injected onto a path read")

        # Done case: edit the template's own Completion status line.
        flat = base / "progress.md"
        flat.write_text(
            flat.read_text(encoding="utf-8").replace(
                "**Completion status:** in progress",
                "**Completion status:** done",
                1,
            ),
            encoding="utf-8",
        )
        done = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        done_body = _context(done.stdout)
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        print("cursor journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
