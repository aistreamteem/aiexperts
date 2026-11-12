"""Stop-hook merge writes into the real journals path, not the legacy pointer."""

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


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-stop-"))
    try:
        # Copy hooks into temp workspace so imports resolve.
        shutil.copytree(HOOKS, tmp / ".claude" / "hooks")
        (tmp / "journals" / "expert").mkdir(parents=True)
        (tmp / "journals" / "expert" / "progress.md").write_text(
            "**Current work item:** WID-TEST\n", encoding="utf-8"
        )
        base = tmp / "journals" / "work-items" / "WID-TEST"
        nodes = base / "nodes"
        notes = base / "agent-notes"
        nodes.mkdir(parents=True)
        notes.mkdir(parents=True)
        (base / "progress.md").write_text(
            "**Completion status:** in progress\n", encoding="utf-8"
        )
        (base / "state.json").write_text(
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {}}}),
            encoding="utf-8",
        )
        leaf = nodes / "work-item.md"
        leaf.write_text(
            "# work-item\n\n**Next action:** intake\n\n## Step notes\n",
            encoding="utf-8",
        )
        (notes / "README.md").write_text("# notes\n", encoding="utf-8")
        (notes / "scout.md").write_text(
            "**Status:** ok\n\nFound the rate file.\n", encoding="utf-8"
        )

        # Shared task with one subtask missing — must stay untouched.
        task = notes / "tasks" / "t1"
        task.mkdir(parents=True)
        (task / "manifest.json").write_text(
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
            encoding="utf-8",
        )
        (task / "a.md").write_text("**Status:** ok\n\ndone a\n", encoding="utf-8")

        (tmp / "work-items" / "WID-TEST").mkdir(parents=True)
        (tmp / "work-items" / "WID-TEST" / "STATUS.md").write_text(
            "status\n", encoding="utf-8"
        )
        (tmp / ".claude" / "active-context.txt").write_text(
            "work-item:WID-TEST\n", encoding="utf-8"
        )

        # Patch ROOT inside the copied merge module by running from tmp.
        env_py = tmp / ".claude" / "hooks" / "merge_agent_notes.py"
        text = env_py.read_text(encoding="utf-8")
        text = text.replace(
            "ROOT = Path(__file__).resolve().parents[2]",
            f"ROOT = Path(r'{tmp}')",
        )
        env_py.write_text(text, encoding="utf-8")
        snap = tmp / ".claude" / "hooks" / "journal_snapshot.py"
        snap_text = snap.read_text(encoding="utf-8")
        snap_text = snap_text.replace(
            "ROOT = Path(__file__).resolve().parents[2]",
            f"ROOT = Path(r'{tmp}')",
        )
        snap.write_text(snap_text, encoding="utf-8")

        completed = subprocess.run(
            [sys.executable, str(env_py)],
            cwd=str(tmp),
            capture_output=True,
            text=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "merge failed")

        body = leaf.read_text(encoding="utf-8")
        _assert("Found the rate file" in body, "loose note not merged into leaf")
        _assert(not (notes / "scout.md").exists(), "loose note not archived")
        _assert((notes / "merged" / "scout.md").is_file(), "loose note missing from merged/")
        _assert((task / "a.md").is_file(), "partial shared task was consumed early")
        _assert(not (task / ".merged").exists(), "partial shared task marked merged")

        # Unrelated staged file must not be required for merge success (snapshot may no-op).
        print("claude stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
