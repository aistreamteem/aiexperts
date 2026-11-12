"""Stop-hook merge targets the active node and leaves incomplete shared tasks alone."""

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
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        # Copy hooks into a temp workspace that looks like the expert root.
        shutil.copytree(ROOT / ".cursor" / "hooks", tmp / ".cursor" / "hooks")
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item", "role-job"], "nodes": {}}),
        )
        node = base / "nodes" / "role-job.md"
        _write(node, "# Role job\n\n**Next action:** pull schedule export\n")
        notes = base / "agent-notes"
        _write(notes / "helper.md", "LOOSE_NOTE_BODY\n")
        task = notes / "tasks" / "pack"
        _write(
            task / "manifest.json",
            json.dumps({"task": "pack", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "SUB_A\n")
        # b.md missing → shared task must wait

        # Patch ROOT inside merge module by running from tmp with hooks that
        # resolve parents[2] to tmp when hooks live at tmp/.cursor/hooks.
        merge = tmp / ".cursor" / "hooks" / "merge_agent_notes.py"
        completed = subprocess.run(
            [sys.executable, str(merge)],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "merge failed")
        body = node.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in body, "loose note not merged into active node")
        _assert(not (notes / "helper.md").exists(), "loose note not archived")
        _assert((task / "a.md").exists(), "partial shared task was consumed")
        _assert("Background Task Complete" not in body, "partial shared task merged early")

        # Complete the shared task and merge again.
        _write(task / "b.md", "SUB_B\n")
        again = subprocess.run(
            [sys.executable, str(merge)],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(again.returncode == 0, again.stderr or "second merge failed")
        body2 = node.read_text(encoding="utf-8")
        _assert("Background Task Complete: pack" in body2, "shared task not merged")
        _assert((task / ".merged").exists(), "shared task not marked merged")
        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
