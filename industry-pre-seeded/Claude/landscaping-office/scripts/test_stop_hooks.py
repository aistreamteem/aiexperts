"""Stop-hook merge + audit: notes land on the real journal, not the pointer."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".claude" / "hooks"
sys.path.insert(0, str(HOOKS))
from merge_agent_notes import process_work_item  # noqa: E402
from journal_snapshot import snapshot  # noqa: E402


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _setup(tmp: Path, work_id: str = "WID-TEST") -> Path:
    base = tmp / "journals" / "work-items" / work_id
    shutil.copytree(ROOT / "journals" / "work-items" / "_TEMPLATE", base)
    (tmp / ".claude").mkdir(parents=True, exist_ok=True)
    (tmp / ".claude" / "active-context.txt").write_text(
        f"work-item:{work_id}\n", encoding="utf-8"
    )
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
    node.write_text(
        "# work-item\n\n**Next action:** intake\n\n## Step notes\n\n",
        encoding="utf-8",
    )
    _write(tmp / "work-items" / work_id / "STATUS.md", "# status\n")
    _write(tmp / "journals" / "expert" / "progress.md", f"**Current work item:** {work_id}\n")
    return base


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        work_id = "WID-TEST"
        base = _setup(tmp, work_id)
        notes = base / "agent-notes"
        notes.mkdir(parents=True, exist_ok=True)
        _write(notes / "agent-a.md", "**Status:** ok\n\nLOOSE_NOTE_BODY\n")

        # Shared task with one subtask missing must be left alone.
        task = notes / "tasks" / "t1"
        task.mkdir(parents=True)
        _write(
            task / "manifest.json",
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\n\nA_DONE\n")

        _assert(process_work_item(tmp, work_id), "loose note did not merge")
        node_text = (base / "nodes" / "work-item.md").read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in node_text, "loose note missing from active node")
        _assert(not (notes / "agent-a.md").exists(), "loose note not archived")
        _assert((notes / "merged" / "agent-a.md").is_file(), "loose note archive missing")
        _assert((task / "a.md").is_file(), "partial shared task was consumed")
        _assert(not (task / ".merged").exists(), "partial shared task marked merged")

        # Audit commit should include journals/ and leave unrelated staged files alone.
        subprocess.run(["git", "init", "-q"], cwd=str(tmp), check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"], cwd=str(tmp), check=True
        )
        subprocess.run(
            ["git", "config", "user.name", "test"], cwd=str(tmp), check=True
        )
        unrelated = tmp / "unrelated.txt"
        unrelated.write_text("leave me staged\n", encoding="utf-8")
        subprocess.run(["git", "add", "unrelated.txt"], cwd=str(tmp), check=True)
        # Seed an initial commit so later pathspec commits are clean.
        _write(tmp / "README.md", "seed\n")
        subprocess.run(["git", "add", "README.md"], cwd=str(tmp), check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "seed"], cwd=str(tmp), check=True
        )
        # Re-stage unrelated after seed so it is staged-but-unrelated for the audit.
        unrelated.write_text("leave me staged again\n", encoding="utf-8")
        subprocess.run(["git", "add", "unrelated.txt"], cwd=str(tmp), check=True)

        snapshot(tmp, work_id)
        show = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", "HEAD"],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        names = show.stdout
        _assert("journals/" in names, "audit commit missing journals/")
        _assert("unrelated.txt" not in names, "audit commit swept unrelated staged file")
        print("claude stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
