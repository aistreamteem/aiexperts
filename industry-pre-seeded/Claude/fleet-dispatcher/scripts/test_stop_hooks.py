"""Stop-hook merge targets the real journal leaf and scopes the audit commit."""

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
        # Minimal mirror of hooks + journals layout
        shutil.copytree(HOOKS, tmp / ".claude" / "hooks")
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "progress.md",
            "# Work item\n\n**Completion status:** in progress\n",
        )
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {"parent": None}}}),
        )
        leaf = base / "nodes" / "work-item.md"
        _write(leaf, "# work-item\n\n**Next action:** code bank feed\n\n")
        notes = base / "agent-notes"
        _write(notes / "README.md", "notes\n")
        _write(notes / "loose-one.md", "LOOSE_NOTE_BODY\n")

        # Shared task with one subtask missing — must be left alone
        task = notes / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\nA_DONE\n")

        (tmp / ".claude").mkdir(exist_ok=True)
        (tmp / ".claude" / "active-context.txt").write_text(
            f"work-item:{wid}\n", encoding="utf-8"
        )
        _write(tmp / "work-items" / wid / "STATUS.md", "status\n")
        _write(tmp / "unrelated.txt", "DO_NOT_COMMIT\n")

        merge = subprocess.run(
            [sys.executable, str(tmp / ".claude" / "hooks" / "merge_agent_notes.py"), wid],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(merge.returncode == 0, merge.stderr or "merge failed")
        leaf_text = leaf.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in leaf_text, "loose note not merged into leaf")
        _assert("A_DONE" not in leaf_text, "partial shared task was merged early")
        _assert((task / "a.md").is_file(), "partial task note was archived early")
        _assert(not (notes / "loose-one.md").exists(), "loose note not archived")

        # Init git and ensure snapshot does not pick unrelated staged file
        subprocess.run(["git", "init", "-q"], cwd=str(tmp), check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"], cwd=str(tmp), check=True
        )
        subprocess.run(
            ["git", "config", "user.name", "test"], cwd=str(tmp), check=True
        )
        subprocess.run(["git", "add", "unrelated.txt"], cwd=str(tmp), check=True)
        snap = subprocess.run(
            [sys.executable, str(tmp / ".claude" / "hooks" / "journal_snapshot.py"), wid],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(snap.returncode == 0, snap.stderr or "snapshot failed")
        show = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:"],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        names = show.stdout or ""
        _assert("journals/work-items/WID-TEST" in names.replace("\\", "/"), "journal not committed")
        _assert("unrelated.txt" not in names, "unrelated staged file was committed")
        print("fleet stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
