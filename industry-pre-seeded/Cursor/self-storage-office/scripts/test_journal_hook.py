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


def _context(payload: dict) -> str:
    text = payload.get("additional_context") or ""
    nested = (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""
    _assert(bool(text), "additional_context missing")
    _assert(nested == text, "nested additionalContext drifted")
    _assert(payload.get("continue") is True, "continue was not true")
    return text


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
        expert = tmp / "journals" / "expert" / "progress.md"
        lines = []
        for line in expert.read_text(encoding="utf-8").splitlines():
            if "Current work item" in line:
                lines.append("**Current work item:** WID-1")
            else:
                lines.append(line)
        expert.write_text("\n".join(lines) + "\n", encoding="utf-8")

        base = tmp / "journals" / "work-items" / "WID-1"
        shutil.copytree(ROOT / "journals" / "work-items" / "_TEMPLATE", base)
        progress = base / "progress.md"
        progress.write_text(
            progress.read_text(encoding="utf-8").replace(
                "**Completion status:** not started",
                "**Completion status:** in progress",
            ),
            encoding="utf-8",
        )
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
        (base / "nodes" / "work-item.md").write_text("ROOT_NOTE\n", encoding="utf-8")
        (base / "nodes" / "spec.md").write_text("ACTIVE_BRANCH_NOTE\n", encoding="utf-8")
        (base / "nodes" / "implement.md").write_text("INACTIVE_BRANCH_NOTE\n", encoding="utf-8")
        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)

        # No pointer files: work item found only from the expert journal line.
        body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("Premise" in body or "Current work item" in body, "expert journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

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
        _assert("Premise" in read_body or "Current work item" in read_body, "expert journal dropped on note read")

        path_body = _context(
            _run(
                {
                    "tool_name": "Read",
                    "tool_input": {"path": "journals/work-items/WID-1/nodes/spec.md"},
                },
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in path_body, "active note injected onto a path read")

        progress.write_text(
            progress.read_text(encoding="utf-8").replace(
                "**Completion status:** in progress",
                "**Completion status:** done",
            ),
            encoding="utf-8",
        )
        done_body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert(
            "Decisions" in done_body or "Completion status" in done_body,
            "done work item journal missing",
        )
        print("cursor journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
