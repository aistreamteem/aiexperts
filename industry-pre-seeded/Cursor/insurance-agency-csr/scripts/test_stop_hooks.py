"""Stop-hook merge targets the active leaf and commits real journal paths."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
import merge_agent_notes  # noqa: E402


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="cursor-stop-") as tmp_name:
        tmp = Path(tmp_name)
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item", "intake"], "nodes": {}}),
        )
        _write(base / "nodes" / "intake.md", "# intake\n\n**Next action:** assemble pack\n")
        _write(base / "progress.md", "# Work item\n\n**Completion status:** in progress\n")
        _write(tmp / "journals" / "expert" / "progress.md", "**Current work item:** WID-TEST\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "status\n")
        _write(tmp / ".cursor" / "active-context.txt", "work-item:WID-TEST\n")

        notes = base / "agent-notes"
        _write(notes / "worker.md", "**Status:** done\n\nFinished holder list.\n")

        # Shared task incomplete — must stay pending
        task = notes / "tasks" / "batch-1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "batch", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** done\n\nA ok\n")

        did = merge_agent_notes.process_work_item(tmp, wid)
        _assert(did, "loose note should merge")
        leaf = (base / "nodes" / "intake.md").read_text(encoding="utf-8")
        _assert("Finished holder list" in leaf, "loose note missing from active leaf")
        _assert(not (notes / "worker.md").exists(), "loose note not archived")
        _assert((notes / "merged" / "worker.md").is_file(), "loose note archive missing")
        _assert((task / "a.md").is_file(), "incomplete shared task was consumed")
        _assert(not (task / ".merged").is_file(), "incomplete shared task marked merged")

        # Audit commit should touch journals/, not an unrelated staged file
        _git(tmp, "init")
        _git(tmp, "config", "user.email", "test@example.com")
        _git(tmp, "config", "user.name", "Test")
        unrelated = tmp / "UNRELATED.txt"
        unrelated.write_text("leave me staged\n", encoding="utf-8")
        _git(tmp, "add", "UNRELATED.txt")
        from journal_snapshot import snapshot_work_item

        snapshot_work_item(tmp, wid)
        staged = _git(tmp, "diff", "--cached", "--name-only")
        _assert(
            "UNRELATED.txt" in (staged.stdout or ""),
            "unrelated staged file was unstaged",
        )
        show = _git(tmp, "log", "-1", "--name-only", "--pretty=format:")
        names = staged.stdout + "\n" + (show.stdout or "")
        # After commit, last commit should include journals paths
        last = _git(tmp, "log", "-1", "--name-only")
        _assert(
            "journals/work-items/WID-TEST" in (last.stdout or "").replace("\\", "/"),
            "audit commit missing journals path",
        )
        _assert(
            "UNRELATED.txt" not in (last.stdout or ""),
            "audit commit swept unrelated file",
        )
    print("cursor stop hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
