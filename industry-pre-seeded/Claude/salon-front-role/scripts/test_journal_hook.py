"""Claude PreToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "inject_journal_context.py"
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


def _fill_expert(path: Path, work_id: str) -> None:
    text = EXPERT_TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("**Current work item:**", f"**Current work item:** {work_id}", 1)
    # Keep a marker the test can assert on.
    text = "EXPERT_JOURNAL\n\n" + text
    path.write_text(text, encoding="utf-8")


def _fill_work_item(base: Path, status: str = "in progress") -> None:
    shutil.copytree(WI_TEMPLATE, base, dirs_exist_ok=True)
    progress = (base / "progress.md").read_text(encoding="utf-8")
    if "**Completion status:**" in progress:
        # Replace the whole line: the template already carries a value
        # ("not started"), which would otherwise be left after the new one.
        progress = re.sub(
            r"\*\*Completion status:\*\*[^\n]*",
            f"**Completion status:** {status}",
            progress,
            count=1,
        )
    else:
        progress = progress.rstrip() + f"\n\n**Completion status:** {status}\n"
    # Marker for assertions.
    progress = "WORK_ITEM_JOURNAL\n\n" + progress
    (base / "progress.md").write_text(progress, encoding="utf-8")
    _write(
        base / "state.json",
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
    )
    _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n")
    _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n")
    _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")


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


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        (tmp / ".claude").mkdir(parents=True, exist_ok=True)
        expert = tmp / "journals" / "expert" / "progress.md"
        expert.parent.mkdir(parents=True, exist_ok=True)
        _fill_expert(expert, "WID-1")
        base = tmp / "journals" / "work-items" / "WID-1"
        _fill_work_item(base)

        # No pointer files: work item found only from the expert journal line.
        loaded = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        body = _context(json.dumps(loaded) if False else json.dumps(loaded))
        # Re-run via helper that returns dict; rebuild body from the dict.
        body = loaded.get("additional_context") or ""
        nested = (loaded.get("hookSpecificOutput") or {}).get("additionalContext") or ""
        _assert(bool(body), "additional_context missing")
        _assert(nested == body, "nested additionalContext drifted")
        _assert(loaded.get("continue") is True, "continue was not true")
        _assert("EXPERT_JOURNAL" in body, "expert journal missing")
        _assert("WORK_ITEM_JOURNAL" in body, "work item journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")
        _assert((base / "nodes" / "implement.md").is_file(), "inactive note removed")

        reading = _run(
            {
                "tool_name": "Read",
                "tool_input": {"file_path": "journals/work-items/WID-1/nodes/spec.md"},
            },
            tmp,
        )
        read_body = reading.get("additional_context") or ""
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")
        _assert("EXPERT_JOURNAL" in read_body, "expert journal dropped on note read")

        reading_path = _run(
            {
                "tool_name": "Read",
                "tool_input": {"path": "journals/work-items/WID-1/nodes/spec.md"},
            },
            tmp,
        )
        path_body = reading_path.get("additional_context") or ""
        _assert("ACTIVE_BRANCH_NOTE" not in path_body, "active note injected onto a path read")

        # Done case: edit the template's own Completion status line.
        progress = (base / "progress.md").read_text(encoding="utf-8")
        progress = progress.replace(
            "**Completion status:** in progress",
            "**Completion status:** done",
            1,
        )
        (base / "progress.md").write_text(progress, encoding="utf-8")
        done = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        done_body = done.get("additional_context") or ""
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert("WORK_ITEM_JOURNAL" in done_body, "done work item journal missing")
        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
