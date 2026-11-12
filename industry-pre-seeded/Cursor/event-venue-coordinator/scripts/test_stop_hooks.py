"""Stop-hook merge and audit behavior for the real journals path."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
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
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {"parent": None}}}),
        )
        leaf = base / "nodes" / "work-item.md"
        _write(leaf, "# work-item\n\n**Next action:** intake\n")
        notes = base / "agent-notes"
        _write(notes / "README.md", "notes format\n")
        _write(notes / "scout.md", "LOOSE_NOTE_BODY\n")
        _write(
            notes / "tasks" / "pack" / "manifest.json",
            json.dumps({"task": "pack", "subtasks": ["a", "b"]}),
        )
        _write(notes / "tasks" / "pack" / "a.md", "SUB_A\n")
        # b missing → shared task left alone

        _assert(process_work_item(tmp, wid), "loose merge should succeed")
        leaf_text = leaf.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in leaf_text, "loose note missing from leaf")
        _assert(not (notes / "scout.md").exists(), "loose note not archived")
        _assert((notes / "tasks" / "pack" / "a.md").exists(), "partial shared task altered")
        _assert(not (notes / "tasks" / "pack" / ".merged").exists(), "partial task marked merged")

        # Audit commit paths: only journal files, not unrelated staged file.
        subprocess.run(["git", "init"], cwd=tmp, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=tmp,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "test"],
            cwd=tmp,
            check=True,
            capture_output=True,
        )
        _write(tmp / "journals" / "expert" / "progress.md", "**Current work item:** WID-TEST\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "status\n")
        _write(tmp / "unrelated.txt", "do not commit\n")
        subprocess.run(["git", "add", "unrelated.txt"], cwd=tmp, check=True, capture_output=True)
        snapshot(tmp, wid)
        show = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:"],
            cwd=tmp,
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
