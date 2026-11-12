"""Stop-hook merge targets the real journal node and scopes the audit commit."""

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
from journal_snapshot import snapshot  # noqa: E402


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
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        wid = "WID-TEST"
        jbase = tmp / "journals" / "work-items" / wid
        notes = jbase / "agent-notes"
        nodes = jbase / "nodes"
        nodes.mkdir(parents=True)
        notes.mkdir(parents=True)
        (jbase / "progress.md").write_text(
            "# Work item journal\n\n**Completion status:** in progress\n",
            encoding="utf-8",
        )
        (jbase / "state.json").write_text(
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {"parent": None}}}),
            encoding="utf-8",
        )
        leaf = nodes / "work-item.md"
        leaf.write_text("# work-item\n\n**Next action:** pack\n", encoding="utf-8")
        (notes / "scout.md").write_text(
            "**Status:** done\n\nFound rate file.\n",
            encoding="utf-8",
        )

        # Shared task with one subtask missing must be left alone.
        task = notes / "tasks" / "t1"
        task.mkdir(parents=True)
        (task / "manifest.json").write_text(
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
            encoding="utf-8",
        )
        (task / "a.md").write_text("**Status:** done\n\nA ok\n", encoding="utf-8")

        _assert(process_work_item(tmp, wid), "loose note should merge")
        body = leaf.read_text(encoding="utf-8")
        _assert("Found rate file" in body, "loose note missing from leaf")
        _assert(not (notes / "scout.md").exists(), "loose note not archived")
        _assert((notes / "merged" / "scout.md").is_file(), "loose note archive missing")
        _assert((task / "a.md").is_file(), "partial shared task was consumed")
        _assert(not (task / ".merged").exists(), "partial shared task marked merged")

        # Audit commit includes journals/ and excludes unrelated staged file.
        _git(tmp, "init")
        _git(tmp, "config", "user.name", "Test")
        _git(tmp, "config", "user.email", "test@example.com")
        (tmp / "work-items" / wid).mkdir(parents=True)
        (tmp / "work-items" / wid / "STATUS.md").write_text("status\n", encoding="utf-8")
        (tmp / "journals" / "expert").mkdir(parents=True)
        (tmp / "journals" / "expert" / "progress.md").write_text(
            "**Current work item:** WID-TEST\n",
            encoding="utf-8",
        )
        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)
        (tmp / ".cursor" / "active-context.txt").write_text("work-item:WID-TEST\n", encoding="utf-8")
        unrelated = tmp / "secrets.txt"
        unrelated.write_text("do-not-commit\n", encoding="utf-8")
        _git(tmp, "add", "journals", "work-items")
        _git(tmp, "commit", "-m", "seed")
        _git(tmp, "add", "secrets.txt")  # staged but must not ride along
        leaf.write_text(leaf.read_text(encoding="utf-8") + "\nextra note\n", encoding="utf-8")
        _assert(snapshot(tmp, wid), "snapshot should commit")
        show = _git(tmp, "show", "--name-only", "--pretty=format:", "HEAD")
        names = {line.strip().replace("\\", "/") for line in show.stdout.splitlines() if line.strip()}
        _assert(any(n.startswith("journals/") for n in names), "journals missing from commit")
        _assert("secrets.txt" not in names, "unrelated staged file was committed")
        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
