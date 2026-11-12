"""Stop-hook merge writes to the active node and commits journal paths only."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


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
        # Minimal repo layout
        for rel in [
            ".cursor/hooks",
            "journals/work-items/WID-TEST/nodes",
            "journals/work-items/WID-TEST/agent-notes",
            "journals/expert",
            "work-items/WID-TEST",
            "facts",
        ]:
            (tmp / rel).mkdir(parents=True, exist_ok=True)

        # Copy hook modules
        for name in (
            "journal_fields.py",
            "merge_agent_notes.py",
            "journal_snapshot.py",
            "on_stop.py",
        ):
            (tmp / ".cursor" / "hooks" / name).write_text(
                (ROOT / ".cursor" / "hooks" / name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )

        (tmp / ".cursor" / "active-context.txt").write_text(
            "work-item:WID-TEST\n", encoding="utf-8"
        )
        (tmp / "journals" / "expert" / "progress.md").write_text(
            "**Current work item:** WID-TEST\n", encoding="utf-8"
        )
        (tmp / "journals" / "work-items" / "WID-TEST" / "progress.md").write_text(
            "**Completion status:** in progress\n", encoding="utf-8"
        )
        (tmp / "journals" / "work-items" / "WID-TEST" / "state.json").write_text(
            json.dumps({"active": ["work-item", "intake"], "nodes": {}}),
            encoding="utf-8",
        )
        leaf = tmp / "journals" / "work-items" / "WID-TEST" / "nodes" / "intake.md"
        leaf.write_text("# intake\n\n**Next action:** run pack\n", encoding="utf-8")
        (tmp / "work-items" / "WID-TEST" / "STATUS.md").write_text(
            "status ok\n", encoding="utf-8"
        )

        # Loose note
        (tmp / "journals" / "work-items" / "WID-TEST" / "agent-notes" / "helper.md").write_text(
            "LOOSE_NOTE_BODY\n", encoding="utf-8"
        )

        # Shared task missing one subtask
        task = tmp / "journals" / "work-items" / "WID-TEST" / "agent-notes" / "tasks" / "t1"
        task.mkdir(parents=True)
        (task / "manifest.json").write_text(
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
            encoding="utf-8",
        )
        (task / "a.md").write_text("sub-a\n", encoding="utf-8")

        # Unrelated staged file should not ride along
        (tmp / "unrelated.txt").write_text("leave me\n", encoding="utf-8")

        _git(tmp, "init")
        _git(tmp, "config", "user.email", "test@example.com")
        _git(tmp, "config", "user.name", "Test")
        _git(tmp, "add", "journals", "work-items", ".cursor", "unrelated.txt")
        _git(tmp, "commit", "-m", "seed")
        _git(tmp, "add", "unrelated.txt")  # keep staged after seed if needed
        (tmp / "unrelated.txt").write_text("leave me changed\n", encoding="utf-8")
        _git(tmp, "add", "unrelated.txt")

        merge = subprocess.run(
            [sys.executable, str(tmp / ".cursor" / "hooks" / "merge_agent_notes.py")],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(merge.returncode == 0, merge.stderr or "merge failed")

        leaf_body = leaf.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in leaf_body, "loose note not merged into active node")
        _assert(not (task / ".merged").is_file(), "partial shared task was merged")
        _assert((task / "a.md").is_file(), "partial shared task note removed")

        # Unrelated staged change must still be only unrelated.txt content change
        staged = _git(tmp, "diff", "--cached", "--name-only")
        names = {n.strip().replace("\\", "/") for n in staged.stdout.splitlines() if n.strip()}
        _assert("unrelated.txt" in names, "unrelated staged file was unstaged")
        # Journal commit should have happened for merged loose note
        log = _git(tmp, "log", "-1", "--name-only", "--pretty=format:")
        committed = {n.strip().replace("\\", "/") for n in log.stdout.splitlines() if n.strip()}
        _assert(
            any(n.startswith("journals/") for n in committed),
            f"audit commit missing journals paths: {committed}",
        )
        _assert("unrelated.txt" not in committed, "audit commit swept unrelated file")

        print("cursor stop hook tests passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
