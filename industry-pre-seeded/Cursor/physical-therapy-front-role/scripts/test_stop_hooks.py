"""Stop-hook merge targets the real journal node; audit paths stay scoped."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".cursor" / "hooks"
sys.path.insert(0, str(HOOKS))


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        shutil.copytree(ROOT / "journals" / "work-items" / "_TEMPLATE", tmp / "journals" / "work-items" / "WID-TEST")
        (tmp / "work-items" / "WID-TEST").mkdir(parents=True)
        (tmp / "work-items" / "WID-TEST" / "STATUS.md").write_text("status\n", encoding="utf-8")
        (tmp / ".cursor").mkdir(parents=True)
        (tmp / ".cursor" / "active-context.txt").write_text("work-item:WID-TEST\n", encoding="utf-8")

        base = tmp / "journals" / "work-items" / "WID-TEST"
        (base / "state.json").write_text(
            json.dumps(
                {
                    "active": ["work-item"],
                    "nodes": {"work-item": {"parent": None, "status": "open", "history": []}},
                }
            ),
            encoding="utf-8",
        )
        node = base / "nodes" / "work-item.md"
        node.write_text("# work-item\n\n**Next action:** run day-list\n", encoding="utf-8")
        notes = base / "agent-notes"
        notes.mkdir(parents=True, exist_ok=True)
        (notes / "loose-one.md").write_text("**Status:** done\n\nLOOSE_NOTE_BODY\n", encoding="utf-8")

        # Shared task with one missing subtask must wait
        task = notes / "tasks" / "t1"
        task.mkdir(parents=True)
        (task / "manifest.json").write_text(
            json.dumps({"task": "pack", "subtasks": ["a", "b"]}),
            encoding="utf-8",
        )
        (task / "a.md").write_text("**Status:** done\n\nA_OK\n", encoding="utf-8")

        import merge_agent_notes

        # Run from tmp as cwd
        old = Path.cwd()
        try:
            import os

            os.chdir(tmp)
            merge_agent_notes.process_work_item(tmp, "WID-TEST")
        finally:
            os.chdir(old)

        body = node.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in body, "loose note not merged into active node")
        _assert((notes / "merged" / "loose-one.md").is_file(), "loose note not archived")
        _assert(not (notes / "loose-one.md").is_file(), "loose note still pending")
        _assert(not (task / ".merged").is_file(), "partial shared task was merged early")
        _assert((task / "a.md").is_file(), "present subtask note was removed early")

        # Complete shared task
        (task / "b.md").write_text("**Status:** done\n\nB_OK\n", encoding="utf-8")
        os.chdir(tmp)
        try:
            merge_agent_notes.process_work_item(tmp, "WID-TEST")
        finally:
            os.chdir(old)
        body2 = node.read_text(encoding="utf-8")
        _assert("Background Task Complete" in body2 or "subtask: a" in body2, "shared task not merged")
        _assert((task / ".merged").is_file(), "shared task not marked merged")

        # on_stop always emits {}
        completed = subprocess.run(
            [sys.executable, str(HOOKS / "on_stop.py")],
            input="{}",
            text=True,
            capture_output=True,
            cwd=str(tmp),
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "on_stop failed")
        _assert(completed.stdout.strip() == "{}", f"bad on_stop stdout: {completed.stdout!r}")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
