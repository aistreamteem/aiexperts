"""Stop-hook merge targets the real journals tree."""

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
        hooks = ROOT / ".cursor" / "hooks"
        dest_hooks = tmp / ".cursor" / "hooks"
        dest_hooks.mkdir(parents=True, exist_ok=True)
        for name in (
            "journal_fields.py",
            "merge_agent_notes.py",
            "journal_snapshot.py",
            "on_stop.py",
        ):
            shutil.copy2(hooks / name, dest_hooks / name)
        # Patch ROOT inside copied merge module by writing a tiny shim cwd layout
        wid = "WID-TEST"
        _write(tmp / ".cursor" / "active-context.txt", f"work-item:{wid}\n")
        _write(
            tmp / "journals" / "work-items" / wid / "state.json",
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {}}}),
        )
        node = tmp / "journals" / "work-items" / wid / "nodes" / "work-item.md"
        _write(node, "# Node\n\n**Next action:** intake\n")
        notes = tmp / "journals" / "work-items" / wid / "agent-notes"
        _write(notes / "loose-note.md", "LOOSE_NOTE_BODY\n")
        tasks = notes / "tasks" / "t1"
        _write(
            tasks / "manifest.json",
            json.dumps({"task": "pair", "subtasks": ["a", "b"]}),
        )
        _write(tasks / "a.md", "**Status:** ok\nA_DONE\n")
        # b missing → shared task must wait

        # Point merge module ROOT at tmp by running from tmp with PYTHONPATH
        env_hooks = tmp / ".cursor" / "hooks"
        # Rewrite ROOT constants in the copied files
        for fname in ("merge_agent_notes.py", "journal_snapshot.py", "on_stop.py"):
            path = env_hooks / fname
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                "Path(__file__).resolve().parents[2]",
                "Path(__file__).resolve().parents[2]  # expert root",
            )
            path.write_text(text, encoding="utf-8")

        completed = subprocess.run(
            [sys.executable, str(env_hooks / "merge_agent_notes.py")],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "merge failed")
        body = node.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in body, "loose note not merged into leaf")
        _assert(not (notes / "loose-note.md").is_file(), "loose note not archived")
        _assert((notes / "merged" / "loose-note.md").is_file(), "loose archive missing")
        _assert(not (tasks / ".merged").is_file(), "partial shared task was merged")

        # Complete shared task
        _write(tasks / "b.md", "**Status:** ok\nB_DONE\n")
        completed = subprocess.run(
            [sys.executable, str(env_hooks / "merge_agent_notes.py")],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "second merge failed")
        body = node.read_text(encoding="utf-8")
        _assert("A_DONE" in body and "B_DONE" in body, "shared task notes missing")
        _assert((tasks / ".merged").is_file(), "shared task not marked merged")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
