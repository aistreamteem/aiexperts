"""Stop-hook merge writes into the active node and audits journal paths."""

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


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-stop-"))
    try:
        wid = "WID-TEST"
        shutil.copytree(ROOT / ".claude" / "hooks", tmp / ".claude" / "hooks")
        (tmp / "journals" / "expert").mkdir(parents=True)
        _write(tmp / "journals" / "expert" / "progress.md", "**Current work item:** WID-TEST\n")
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "progress.md",
            "**Completion status:** in progress\n**Workflow type:** pack-out-list\n",
        )
        _write(
            base / "state.json",
            json.dumps(
                {
                    "active": ["work-item"],
                    "nodes": {"work-item": {"parent": None, "status": "open", "history": []}},
                }
            ),
        )
        _write(base / "nodes" / "work-item.md", "**Next action:** run pack-out step\n")
        _write(base / "agent-notes" / "README.md", "notes\n")
        _write(base / "agent-notes" / "worker-a.md", "LOOSE_NOTE_BODY\n")
        _write(
            base / "agent-notes" / "tasks" / "t1" / "manifest.json",
            json.dumps({"task": "shared", "subtasks": ["a", "b"]}),
        )
        _write(base / "agent-notes" / "tasks" / "t1" / "a.md", "**Status:** ok\nA_DONE\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "status\n")
        _write(tmp / ".claude" / "active-context.txt", "work-item:WID-TEST\n")

        completed = subprocess.run(
            [sys.executable, str(tmp / ".claude" / "hooks" / "merge_agent_notes.py")],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "merge failed")
        node = (base / "nodes" / "work-item.md").read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in node, "loose note not merged into active node")
        _assert("A_DONE" not in node, "partial shared task leaked")
        _assert((base / "agent-notes" / "tasks" / "t1" / "a.md").is_file(), "waiting subtask removed")
        _assert(not (base / "agent-notes" / "worker-a.md").is_file(), "loose note not archived")
        print("claude stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
