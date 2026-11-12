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


def _fill_templates(tmp: Path, work_id: str = "WID-1") -> Path:
    shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
    base = tmp / "journals" / "work-items" / work_id
    shutil.copytree(ROOT / "journals" / "work-items" / "_TEMPLATE", base)
    expert = tmp / "journals" / "expert" / "progress.md"
    expert_text = expert.read_text(encoding="utf-8")
    if "**Current work item:**" in expert_text:
        expert_text = expert_text.replace(
            "**Current work item:**", f"**Current work item:** {work_id}", 1
        )
    else:
        expert_text = expert_text.rstrip() + f"\n\n**Current work item:** {work_id}\n"
    expert.write_text(expert_text, encoding="utf-8")
    flat = base / "progress.md"
    flat_text = flat.read_text(encoding="utf-8")
    flat.write_text(
        flat_text.replace(
            "**Completion status:** not started",
            "**Completion status:** in progress",
            1,
        ),
        encoding="utf-8",
    )
    _write(
        base / "state.json",
        json.dumps(
            {
                "active": ["work-item", "pack"],
                "nodes": {
                    "work-item": {"parent": None, "status": "open", "history": []},
                    "pack": {"parent": "work-item", "status": "open", "history": []},
                    "other": {"parent": "work-item", "status": "open", "history": []},
                },
            }
        ),
    )
    _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n")
    _write(base / "nodes" / "pack.md", "ACTIVE_BRANCH_NOTE\n")
    _write(base / "nodes" / "other.md", "INACTIVE_BRANCH_NOTE\n")
    return base


def _run(payload: dict, workspace: Path) -> str:
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or completed.stdout or "hook failed")
    return completed.stdout


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)
        base = _fill_templates(tmp)
        (tmp / ".cursor" / "active-context.txt").write_text(
            "work-item:WID-1\n", encoding="utf-8"
        )

        body = _context(_run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp))
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        (tmp / ".cursor" / "active-context.txt").unlink(missing_ok=True)
        (tmp / ".cursor" / "active-work-item.txt").unlink(missing_ok=True)
        from_body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" in from_body, "expert-journal work item not found")

        read_body = _context(
            _run(
                {
                    "tool_name": "Read",
                    "tool_input": {
                        "file_path": "journals/work-items/WID-1/nodes/pack.md"
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
        (tmp / ".cursor" / "active-context.txt").write_text(
            "work-item:WID-1\n", encoding="utf-8"
        )
        done_body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        print("cursor journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
