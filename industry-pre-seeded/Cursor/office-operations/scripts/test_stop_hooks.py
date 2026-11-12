"""Stop-hook merge and audit commit use the real journals/ paths."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".cursor" / "hooks"
sys.path.insert(0, str(HOOKS))
from merge_agent_notes import process_work_item  # noqa: E402
from journal_snapshot import snapshot_work_item  # noqa: E402


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        wid = "WID-TEST"
        journals = tmp / "journals" / "work-items" / wid
        session = tmp / "work-items" / wid
        _write(tmp / ".cursor" / "active-context.txt", f"work-item:{wid}\n")
        _write(tmp / "journals" / "expert" / "progress.md", f"**Current work item:** {wid}\n")
        _write(
            journals / "progress.md",
            "**Completion status:** in progress\n**Workflow type:** weekly-pack\n",
        )
        _write(
            journals / "state.json",
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
        _write(
            journals / "nodes" / "intake.md",
            "**Next action:** run calendar step\n**Last completed:** none\n",
        )
        _write(session / "STATUS.md", "status ok\n")
        _write(
            journals / "agent-notes" / "README.md",
            "notes folder\n",
        )
        _write(
            journals / "agent-notes" / "worker-a.md",
            "**Status:** done\n\nFilled the intake CSV.\n",
        )
        _write(
            journals / "agent-notes" / "tasks" / "pack" / "manifest.json",
            json.dumps({"task": "pack", "subtasks": ["a", "b"]}),
        )
        _write(
            journals / "agent-notes" / "tasks" / "pack" / "a.md",
            "**Status:** done\n\nsubtask a\n",
        )
        # b missing → shared task must stay untouched

        _git(tmp, "init", "-q")
        _git(tmp, "config", "user.name", "Test")
        _git(tmp, "config", "user.email", "test@example.com")
        _write(tmp / "unrelated.txt", "leave me staged\n")
        _git(tmp, "add", "unrelated.txt")
        _git(tmp, "commit", "-q", "-m", "seed")
        _write(tmp / "unrelated.txt", "dirty staged other work\n")
        _git(tmp, "add", "unrelated.txt")

        process_work_item(tmp, wid)

        leaf = (journals / "nodes" / "intake.md").read_text(encoding="utf-8")
        _assert("Filled the intake CSV" in leaf, "loose note was not merged into active leaf")
        _assert(
            not (journals / "agent-notes" / "worker-a.md").is_file(),
            "loose note was not archived",
        )
        _assert(
            (journals / "agent-notes" / "merged" / "worker-a.md").is_file(),
            "loose note missing from merged/",
        )
        _assert(
            (journals / "agent-notes" / "tasks" / "pack" / "a.md").is_file(),
            "partial shared task should not merge early",
        )
        _assert(
            not (journals / "agent-notes" / "tasks" / "pack" / ".merged").is_file(),
            "partial shared task was marked merged",
        )

        # Complete shared task and merge again
        _write(
            journals / "agent-notes" / "tasks" / "pack" / "b.md",
            "**Status:** done\n\nsubtask b\n",
        )
        process_work_item(tmp, wid)
        leaf2 = (journals / "nodes" / "intake.md").read_text(encoding="utf-8")
        _assert("Background Task Complete: pack" in leaf2, "shared task was not merged")

        # Explicit snapshot already ran inside process_work_item; verify commit contents
        show = _git(tmp, "log", "-1", "--name-only", "--pretty=format:")
        names = {line.strip().replace("\\", "/") for line in show.stdout.splitlines() if line.strip()}
        _assert(any(n.startswith(f"journals/work-items/{wid}/") for n in names), "journals/ missing from commit")
        _assert("unrelated.txt" not in names, "unrelated staged file was committed")

        # snapshot alone still exits 0
        _assert(snapshot_work_item(tmp, wid) == 0, "snapshot failed")
        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
