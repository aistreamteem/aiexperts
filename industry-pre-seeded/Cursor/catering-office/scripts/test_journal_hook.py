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


def _setup_from_templates(tmp: Path, work_id: str = "WID-1") -> Path:
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
    progress.write_text(
        progress.read_text(encoding="utf-8").replace("work-items/", f"work-items/{work_id}/"),
        encoding="utf-8",
    )
    state = {
        "active": ["work-item", "spec"],
        "nodes": {
            "work-item": {"parent": None, "status": "open", "history": []},
            "spec": {"parent": "work-item", "status": "open", "history": []},
            "implement": {"parent": "work-item", "status": "open", "history": []},
        },
    }
    (base / "state.json").write_text(json.dumps(state), encoding="utf-8")
    _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n")
    _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n")
    _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")
    (tmp / ".cursor").mkdir(parents=True, exist_ok=True)
    return base


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        base = _setup_from_templates(tmp)
        (tmp / ".cursor" / "active-context.txt").write_text("work-item:WID-1\n", encoding="utf-8")

        body = _context(_run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp))
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        tmp2 = Path(tempfile.mkdtemp(prefix="cursor-journal-noptr-"))
        try:
            _setup_from_templates(tmp2)
            body2 = _context(
                _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp2)
            )
            _assert("ACTIVE_BRANCH_NOTE" in body2, "journal-only work item failed")
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)

        read_body = _context(
            _run(
                {
                    "tool_name": "Read",
                    "tool_input": {"file_path": "journals/work-items/WID-1/nodes/spec.md"},
                },
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")

        progress = base / "progress.md"
        text = progress.read_text(encoding="utf-8")
        progress.write_text(
            text.replace("**Completion status:** not started", "**Completion status:** done"),
            encoding="utf-8",
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
