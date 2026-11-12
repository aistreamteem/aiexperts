"""Stop-hook merge targets the real journal node and commits journal paths only."""

from __future__ import annotations

import json
import shutil
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


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        hooks = tmp / ".cursor" / "hooks"
        hooks.mkdir(parents=True, exist_ok=True)
        for name in (
            "journal_fields.py",
            "merge_agent_notes.py",
            "journal_snapshot.py",
            "on_stop.py",
        ):
            shutil.copy2(ROOT / ".cursor" / "hooks" / name, hooks / name)

        wid = "WID-TEST"
        jdir = tmp / "journals" / "work-items" / wid
        _write(
            jdir / "state.json",
            json.dumps({"active": ["work-item", "day-list"], "nodes": {}}),
        )
        node = jdir / "nodes" / "day-list.md"
        _write(node, "# day-list\n\n**Next action:** run eligibility\n\n")
        _write(jdir / "progress.md", "**Completion status:** in progress\n")
        _write(tmp / "journals" / "expert" / "progress.md", f"**Current work item:** {wid}\n")
        _write(tmp / ".cursor" / "active-context.txt", f"work-item:{wid}\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "# status\n")
        _write(jdir / "agent-notes" / "README.md", "Background agents drop notes here.\n")
        _write(jdir / "agent-notes" / "scout.md", "LOOSE_NOTE_BODY\n")

        task = jdir / "agent-notes" / "tasks" / "pack"
        _write(
            task / "manifest.json",
            json.dumps({"task": "pack", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\nA_DONE\n")

        _git(tmp, "init", "-q")
        _git(tmp, "config", "user.name", "Test")
        _git(tmp, "config", "user.email", "test@example.com")
        _write(tmp / "unrelated.txt", "seed\n")
        _git(tmp, "add", ".")
        _git(tmp, "commit", "-q", "-m", "seed")
        _write(tmp / "unrelated.txt", "staged but unrelated\n")
        _git(tmp, "add", "unrelated.txt")

        sys.path.insert(0, str(hooks))
        from merge_agent_notes import process_work_item  # type: ignore

        process_work_item(tmp, wid)

        node_text = node.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in node_text, "loose note not merged into active node")
        _assert("A_DONE" not in node_text, "partial shared task was merged early")
        _assert((task / "a.md").is_file(), "shared-task note was archived while incomplete")
        _assert(not (jdir / "agent-notes" / "scout.md").is_file(), "loose note was not archived")
        _assert((jdir / "agent-notes" / "merged" / "scout.md").is_file(), "loose note missing from merged/")

        show = _git(tmp, "show", "--name-only", "--pretty=format:", "HEAD")
        names = {ln.strip().replace("\\", "/") for ln in show.stdout.splitlines() if ln.strip()}
        _assert(any(n.startswith("journals/") for n in names), f"journals missing from commit: {names}")
        _assert("unrelated.txt" not in names, f"unrelated file was committed: {names}")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
