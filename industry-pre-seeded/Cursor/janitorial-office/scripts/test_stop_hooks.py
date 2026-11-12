"""Stop-hook merge targets the real journal and scopes the audit commit."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MERGE = ROOT / ".cursor" / "hooks" / "merge_agent_notes.py"
SNAPSHOT = ROOT / ".cursor" / "hooks" / "journal_snapshot.py"


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
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        hooks = tmp / ".cursor" / "hooks"
        hooks.mkdir(parents=True)
        for name in (
            "journal_fields.py",
            "journal_snapshot.py",
            "merge_agent_notes.py",
            "on_stop.py",
        ):
            shutil.copy2(ROOT / ".cursor" / "hooks" / name, hooks / name)

        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "progress.md",
            "# Work item journal\n\n**Completion status:** in progress\n",
        )
        _write(
            base / "state.json",
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
        node = base / "nodes" / "intake.md"
        _write(node, "# intake\n\n**Next action:** assemble pack\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "# status\n")
        _write(tmp / "journals" / "expert" / "progress.md", "**Current work item:** WID-TEST\n")
        _write(tmp / ".cursor" / "active-context.txt", "work-item:WID-TEST\n")

        notes = base / "agent-notes"
        _write(notes / "worker-a.md", "LOOSE_NOTE_BODY\n")
        task = notes / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "shared", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\nSUB_A\n")

        init = _git(tmp, "init")
        _assert(init.returncode == 0, init.stderr or "git init failed")
        _git(tmp, "config", "user.email", "test@example.com")
        _git(tmp, "config", "user.name", "Test")
        _write(tmp / "unrelated.txt", "leave me staged\n")
        _git(tmp, "add", "journals", "work-items", ".cursor/active-context.txt")
        _git(tmp, "commit", "-m", "seed")
        _git(tmp, "add", "unrelated.txt")

        merge = subprocess.run(
            [sys.executable, str(hooks / "merge_agent_notes.py")],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(merge.returncode == 0, merge.stderr or merge.stdout or "merge failed")

        node_text = node.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in node_text, "loose note missing from active node")
        _assert("SUB_A" not in node_text, "partial shared task should not merge")
        _assert((task / "a.md").is_file(), "partial shared note should remain")
        _assert(not (notes / "worker-a.md").is_file(), "loose note should be archived")
        _assert((notes / "merged" / "worker-a.md").is_file(), "loose note archive missing")

        log = _git(tmp, "log", "-1", "--name-only", "--pretty=format:")
        names = {line.strip().replace("\\", "/") for line in log.stdout.splitlines() if line.strip()}
        _assert(any(n.startswith("journals/") for n in names), "audit commit missing journals/")
        _assert("unrelated.txt" not in names, "unrelated staged file was committed")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
