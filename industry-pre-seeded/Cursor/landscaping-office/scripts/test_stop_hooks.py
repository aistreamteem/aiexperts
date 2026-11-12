"""Stop-hook merge writes into the active node and audits journals/ only."""

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


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run_merge(workspace: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / ".cursor" / "hooks" / "merge_agent_notes.py")],
        cwd=str(workspace),
        capture_output=True,
        text=True,
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or completed.stdout or "merge failed")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        shutil.copytree(ROOT / "journals" / "work-items" / "_TEMPLATE", base)
        session = tmp / "work-items" / wid
        session.mkdir(parents=True)
        _write(session / "STATUS.md", "# Status\n")
        _write(
            base / "state.json",
            json.dumps(
                {
                    "active": ["work-item"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []}
                    },
                }
            ),
        )
        node = base / "nodes" / "work-item.md"
        _write(node, "# work-item\n\n**Next action:** build crew day\n")
        notes = base / "agent-notes"
        notes.mkdir(parents=True, exist_ok=True)
        _write(notes / "scout.md", "**Status:** done\n\nSaw skip flag on lot 12.\n")

        # Shared task missing one subtask must stay pending
        task = notes / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "split route", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** done\n\nA done\n")

        # Unrelated staged-looking file outside journal paths
        other = tmp / "unrelated.txt"
        other.write_text("leave me alone\n", encoding="utf-8")

        # Local git repo so snapshot can run without touching parent
        subprocess.run(["git", "init", "-q"], cwd=str(tmp), check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"], cwd=str(tmp), check=True
        )
        subprocess.run(
            ["git", "config", "user.name", "test"], cwd=str(tmp), check=True
        )
        subprocess.run(["git", "add", "-A"], cwd=str(tmp), check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "seed"], cwd=str(tmp), check=True
        )
        # Stage an unrelated change that must not ride along
        other.write_text("dirty\n", encoding="utf-8")
        subprocess.run(["git", "add", "--", "unrelated.txt"], cwd=str(tmp), check=True)

        _run_merge(tmp)

        node_text = node.read_text(encoding="utf-8")
        _assert("Saw skip flag on lot 12" in node_text, "loose note not merged into node")
        _assert(not (notes / "scout.md").is_file(), "loose note not archived")
        _assert((notes / "merged" / "scout.md").is_file(), "merged archive missing")
        _assert((task / "a.md").is_file(), "partial shared task was consumed early")
        _assert(not (task / ".merged").is_file(), "partial shared task marked merged")

        # Complete the shared task
        _write(task / "b.md", "**Status:** done\n\nB done\n")
        _run_merge(tmp)
        _assert((task / ".merged").is_file(), "shared task not marked merged")
        node_text = node.read_text(encoding="utf-8")
        _assert("Background Task Complete" in node_text, "shared task header missing")

        # Audit commit should include journals paths, not unrelated staged file content change alone
        log = subprocess.run(
            ["git", "log", "-1", "--name-only", "--pretty=format:"],
            cwd=str(tmp),
            capture_output=True,
            text=True,
            check=False,
        )
        names = log.stdout
        _assert("journals/work-items/WID-TEST" in names.replace("\\", "/"), "journal path missing from commit")
        _assert("unrelated.txt" not in names, "unrelated staged file was committed")
        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
