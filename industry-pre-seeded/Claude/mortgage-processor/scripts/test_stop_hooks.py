"""Stop-hook merge writes into the active node and snapshots journals/ paths."""

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
    tmp = Path(tempfile.mkdtemp(prefix="claude-stop-"))
    try:
        # Copy hooks so imports resolve from the temp workspace via cwd + sys.path
        shutil.copytree(HOOKS, tmp / ".claude" / "hooks")
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "progress.md",
            "# Work item journal\n\n**Completion status:** in progress\n",
        )
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {"parent": None}}}),
        )
        node = base / "nodes" / "work-item.md"
        _write(node, "# work-item\n\n**Next action:** run intake\n")
        notes = base / "agent-notes"
        _write(notes / "loose-one.md", "**Status:** ok\n\nDid the index.\n")
        # Shared task missing one subtask — must not merge
        task = notes / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\n\nPart a\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "Status\n")
        _write(tmp / ".claude" / "active-context.txt", f"work-item:{wid}\n")
        _write(tmp / "journals" / "expert" / "progress.md", "**Current work item:** WID-TEST\n")
        # Unrelated staged file must not be in the audit commit (when git exists)
        unrelated = tmp / "unrelated.txt"
        unrelated.write_text("leave me alone\n", encoding="utf-8")

        env_python = sys.executable
        merge = subprocess.run(
            [env_python, str(tmp / ".claude" / "hooks" / "merge_agent_notes.py"), wid],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(merge.returncode == 0, merge.stderr or "merge failed")
        body = node.read_text(encoding="utf-8")
        _assert("Did the index." in body, "loose note not merged into active node")
        _assert("Part a" not in body, "partial shared task leaked into journal")
        _assert(not (notes / "loose-one.md").exists(), "loose note not archived")
        _assert((notes / "merged" / "loose-one.md").is_file(), "loose note missing from merged/")
        _assert(not (task / ".merged").exists(), "incomplete shared task marked merged")

        # Init a tiny repo and ensure snapshot prefers journals/ paths
        subprocess.run(["git", "init", "-q"], cwd=str(tmp), check=False)
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=str(tmp),
            check=False,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=str(tmp),
            check=False,
        )
        _write(notes / "loose-two.md", "**Status:** ok\n\nSecond note.\n")
        snap = subprocess.run(
            [env_python, str(tmp / ".claude" / "hooks" / "merge_agent_notes.py"), wid],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(snap.returncode == 0, snap.stderr or "second merge failed")
        body2 = node.read_text(encoding="utf-8")
        _assert("Second note." in body2, "second loose note missing")
        log = subprocess.run(
            ["git", "log", "-1", "--name-only", "--pretty=format:"],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        names = log.stdout or ""
        if names.strip():
            _assert("journals/" in names.replace("\\", "/"), "audit commit missing journals/")
            _assert("unrelated.txt" not in names, "unrelated staged file was committed")
        print("claude stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
