"""Stop-hook merge targets the real journal node; audit paths stay under journals/."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".claude" / "hooks"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        # Minimal workspace with hooks on sys.path via cwd scripts
        shutil.copytree(HOOKS, tmp / ".claude" / "hooks")
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {"parent": None}}}),
        )
        _write(base / "nodes" / "work-item.md", "# Node\n\n**Next action:** wait\n")
        _write(base / "progress.md", "**Completion status:** in progress\n")
        notes = base / "agent-notes"
        _write(notes / "README.md", "notes format\n")
        _write(notes / "agent-a.md", "LOOSE_NOTE_BODY\n")

        # Shared task missing one subtask — must not merge
        task = notes / "tasks" / "task-1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "demo", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\nA_DONE\n")

        sys.path.insert(0, str(tmp / ".claude" / "hooks"))
        # Point merge module ROOT at tmp by running as script with cwd
        env_py = tmp / ".claude" / "hooks" / "merge_agent_notes.py"
        text = env_py.read_text(encoding="utf-8")
        text = text.replace(
            "ROOT = Path(__file__).resolve().parents[2]",
            f"ROOT = Path(r'{tmp}')",
        )
        env_py.write_text(text, encoding="utf-8")

        completed = subprocess.run(
            [sys.executable, str(env_py)],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "merge failed")

        node = (base / "nodes" / "work-item.md").read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in node, "loose note not merged into active node")
        _assert("A_DONE" not in node, "partial shared task leaked into journal")
        _assert(not (notes / "agent-a.md").is_file(), "loose note not archived")
        _assert((notes / "merged" / "agent-a.md").is_file(), "loose note missing from merged/")
        _assert((task / "a.md").is_file(), "partial task note should remain")

        print("claude stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())


