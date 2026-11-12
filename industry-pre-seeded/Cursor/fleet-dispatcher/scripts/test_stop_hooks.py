"""Stop-hook merge + audit: notes land on the active leaf; commit stays scoped."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".cursor" / "hooks"
sys.path.insert(0, str(HOOKS))

from merge_agent_notes import process_work_item  # noqa: E402
from journal_snapshot import snapshot  # noqa: E402


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="cursor-stop-") as tmp_name:
        tmp = Path(tmp_name)
        wid = "WID-TEST"
        journals = tmp / "journals" / "work-items" / wid
        _write(
            journals / "progress.md",
            "# Work item\n\n**Completion status:** in progress\n",
        )
        _write(
            journals / "state.json",
            json.dumps(
                {
                    "active": ["work-item"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []}
                    },
                }
            ),
        )
        leaf = journals / "nodes" / "work-item.md"
        _write(leaf, "# work-item\n\n**Next action:** pack\n")
        notes = journals / "agent-notes"
        _write(notes / "README.md", "docs\n")
        _write(notes / "bg-1.md", "LOOSE_NOTE_BODY\n")

        # Shared task incomplete: one subtask missing → leave alone
        task = notes / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\nA_DONE\n")

        _assert(process_work_item(tmp, wid) is True, "loose note should merge")
        body = leaf.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in body, "loose note missing from leaf")
        _assert(not (notes / "bg-1.md").exists(), "loose note not archived")
        _assert((notes / "merged" / "bg-1.md").is_file(), "archive missing")
        _assert((task / "a.md").is_file(), "partial shared task was consumed")
        _assert(not (task / ".merged").exists(), "partial task marked merged")

        # Audit commit paths: only journal files, not an unrelated staged file
        subprocess.run(["git", "init", "-q"], cwd=str(tmp), check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=str(tmp),
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=str(tmp),
            check=True,
        )
        _write(tmp / "journals" / "expert" / "progress.md", "EXPERT\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "STATUS\n")
        _write(tmp / "unrelated.txt", "LEAVE_ME\n")
        subprocess.run(["git", "add", "unrelated.txt"], cwd=str(tmp), check=True)
        (tmp / ".cursor").mkdir(exist_ok=True)
        (tmp / ".cursor" / "active-context.txt").write_text(
            f"work-item:{wid}\n", encoding="utf-8"
        )
        snapshot(tmp, wid)
        show = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:"],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        names = show.stdout
        _assert("journals/" in names, "journal paths missing from audit commit")
        _assert("unrelated.txt" not in names, "unrelated staged file was committed")

    print("cursor stop hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
