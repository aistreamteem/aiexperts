"""Stop-hook merge targets the real journal leaf, not the legacy pointer."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGE = ROOT / ".cursor" / "hooks" / "merge_agent_notes.py"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(tmp / "journals" / "expert" / "progress.md", "**Current work item:** WID-TEST\n")
        _write(
            base / "progress.md",
            "# Work item journal\n\n**Completion status:** in progress\n",
        )
        _write(
            base / "state.json",
            json.dumps(
                {
                    "active": ["work-item", "intake"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []},
                        "intake": {"parent": "work-item", "status": "open", "history": []},
                    },
                }
            ),
        )
        leaf = base / "nodes" / "intake.md"
        _write(leaf, "# intake\n\n**Next action:** list files\n")
        _write(base / "nodes" / "work-item.md", "# work-item\n")
        notes = base / "agent-notes"
        _write(notes / "README.md", "docs\n")
        _write(notes / "research.md", "**Status:** ok\n\nFound award PDF.\n")

        # Shared task with one subtask missing must stay pending.
        task = notes / "tasks" / "gap-check"
        _write(
            task / "manifest.json",
            json.dumps({"task": "gap-check", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\n\nA done\n")

        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)
        (tmp / ".cursor" / "active-context.txt").write_text(
            "work-item:WID-TEST\n", encoding="utf-8"
        )
        # Copy hook package so imports resolve.
        hooks_src = ROOT / ".cursor" / "hooks"
        hooks_dst = tmp / ".cursor" / "hooks"
        hooks_dst.mkdir(parents=True, exist_ok=True)
        for name in (
            "journal_fields.py",
            "merge_agent_notes.py",
            "journal_snapshot.py",
            "on_stop.py",
        ):
            shutil.copy2(hooks_src / name, hooks_dst / name)

        completed = subprocess.run(
            [sys.executable, str(hooks_dst / "merge_agent_notes.py")],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "merge failed")

        leaf_text = leaf.read_text(encoding="utf-8")
        _assert("Found award PDF" in leaf_text, "loose note missing from active leaf")
        _assert(not (notes / "research.md").is_file(), "loose note was not archived")
        _assert((notes / "merged" / "research.md").is_file(), "loose note archive missing")
        _assert((task / "a.md").is_file(), "partial shared task was merged too early")
        _assert(not (task / ".merged").is_file(), "partial shared task marked merged")

        # Unrelated staged file must not be required for merge success (snapshot may no-op).
        _write(tmp / "unrelated.txt", "leave me alone\n")
        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
