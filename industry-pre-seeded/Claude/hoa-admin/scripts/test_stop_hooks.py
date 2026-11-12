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
sys.path.insert(0, str(HOOKS))
from merge_agent_notes import process_work_item  # noqa: E402


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


def _setup(tmp: Path) -> Path:
    (tmp / ".claude").mkdir(parents=True)
    (tmp / ".claude" / "active-context.txt").write_text(
        "work-item:WID-TEST\n", encoding="utf-8"
    )
    shutil.copytree(
        ROOT / "journals" / "work-items" / "_TEMPLATE",
        tmp / "journals" / "work-items" / "WID-TEST",
    )
    (tmp / "journals" / "expert").mkdir(parents=True)
    (tmp / "journals" / "expert" / "progress.md").write_text(
        "# Expert\n\n**Current work item:** WID-TEST\n", encoding="utf-8"
    )
    base = tmp / "journals" / "work-items" / "WID-TEST"
    (base / "state.json").write_text(
        json.dumps(
            {
                "active": ["work-item"],
                "nodes": {
                    "work-item": {"parent": None, "status": "open", "history": []}
                },
            }
        ),
        encoding="utf-8",
    )
    node = base / "nodes" / "work-item.md"
    node.write_text(
        "# work-item\n\n**Next action:** intake files\n", encoding="utf-8"
    )
    (tmp / "work-items" / "WID-TEST").mkdir(parents=True)
    (tmp / "work-items" / "WID-TEST" / "STATUS.md").write_text(
        "status\n", encoding="utf-8"
    )
    notes = base / "agent-notes"
    notes.mkdir(parents=True, exist_ok=True)
    return base


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-stop-"))
    try:
        base = _setup(tmp)
        _git(tmp, "init", "-q")
        _git(tmp, "config", "user.name", "Test")
        _git(tmp, "config", "user.email", "test@example.com")
        # Baseline commit so later audit commits are isolated.
        _git(tmp, "add", "-A")
        _git(tmp, "commit", "-q", "-m", "baseline")

        notes = base / "agent-notes"
        (notes / "scout.md").write_text(
            "**Status:** complete\n\nLOOSE_NOTE_BODY\n", encoding="utf-8"
        )
        task = notes / "tasks" / "pack"
        task.mkdir(parents=True)
        (task / "manifest.json").write_text(
            json.dumps({"task": "pack", "subtasks": ["a", "b"]}),
            encoding="utf-8",
        )
        (task / "a.md").write_text("**Status:** complete\nA_ONLY\n", encoding="utf-8")
        # b missing → shared task left alone

        unrelated = tmp / "unrelated.txt"
        unrelated.write_text("do-not-commit\n", encoding="utf-8")
        _git(tmp, "add", "--", "unrelated.txt")

        _assert(process_work_item(tmp, "WID-TEST"), "loose merge did not run")
        leaf = (base / "nodes" / "work-item.md").read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in leaf, "loose note missing from leaf")
        _assert("A_ONLY" not in leaf, "partial shared task leaked")
        _assert((task / "a.md").is_file(), "partial task note was archived early")
        _assert(not (notes / "scout.md").is_file(), "loose note not archived")
        _assert((notes / "merged" / "scout.md").is_file(), "loose archive missing")

        show = _git(tmp, "show", "--name-only", "--pretty=format:")
        names = {
            line.strip().replace("\\", "/")
            for line in show.stdout.splitlines()
            if line.strip()
        }
        _assert(any(n.startswith("journals/") for n in names), f"journals missing: {names}")
        _assert("unrelated.txt" not in names, "unrelated staged file was committed")
        print("claude stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
