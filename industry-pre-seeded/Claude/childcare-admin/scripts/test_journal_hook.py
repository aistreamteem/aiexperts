"""claude journal hook loads the active branch from real templates."""

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


def _run(payload: dict, workspace: Path) -> str:
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or "hook failed")
    return completed.stdout


def _fill_templates(tmp: Path) -> Path:
    shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
    base = tmp / "journals" / "work-items" / "WID-1"
    shutil.copytree(ROOT / "journals" / "work-items" / "_TEMPLATE", base)
    expert = tmp / "journals" / "expert" / "progress.md"
    expert_text = expert.read_text(encoding="utf-8")
    if "**Current work item:**" in expert_text:
        expert_text = expert_text.replace(
            "**Current work item:**",
            "**Current work item:** WID-1",
            1,
        )
    else:
        expert_text += "\n**Current work item:** WID-1\n"
    expert.write_text(expert_text, encoding="utf-8")
    flat = base / "progress.md"
    flat_text = flat.read_text(encoding="utf-8")
    flat_text = flat_text.replace(
        "**Completion status:** not started",
        "**Completion status:** in progress",
    )
    if "**Completion status:**" not in flat_text:
        flat_text += "\n**Completion status:** in progress\n"
    flat.write_text(flat_text, encoding="utf-8")
    _write(
        base / "state.json",
        json.dumps(
            {
                "active": ["work-item", "intake"],
                "nodes": {
                    "work-item": {"parent": None, "status": "open", "history": []},
                    "intake": {"parent": "work-item", "status": "open", "history": []},
                    "pack-out": {"parent": "work-item", "status": "open", "history": []},
                },
            }
        ),
    )
    _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n\n**Next action:** intake\n")
    _write(base / "nodes" / "intake.md", "ACTIVE_BRANCH_NOTE\n\n**Next action:** gather\n")
    _write(base / "nodes" / "pack-out.md", "INACTIVE_BRANCH_NOTE\n")
    return base


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        (tmp / ".claude").mkdir(parents=True, exist_ok=True)
        base = _fill_templates(tmp)

        # No pointer files: work item from the expert journal line only.
        body = _context(
            _run({"tool_name": "Shell", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")
        _assert("WID-1" in body or "Current work item" in body, "expert journal missing")

        read_body = _context(
            _run(
                {
                    "tool_name": "Read",
                    "tool_input": {
                        "file_path": "journals/work-items/WID-1/nodes/intake.md"
                    },
                },
                tmp,
            )
        )
        _assert(
            "ACTIVE_BRANCH_NOTE" not in read_body,
            "active note injected onto its own read",
        )

        flat = base / "progress.md"
        flat.write_text(
            flat.read_text(encoding="utf-8").replace(
                "**Completion status:** in progress",
                "**Completion status:** done",
            ),
            encoding="utf-8",
        )
        done_body = _context(
            _run({"tool_name": "Shell", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert(
            "Completion status" in done_body or "Work item" in done_body.lower() or "done" in done_body.lower(),
            "done work item journal missing",
        )
        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
