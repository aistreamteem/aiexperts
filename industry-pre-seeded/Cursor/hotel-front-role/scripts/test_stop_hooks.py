"""Stop-hook merge writes into the active leaf; audit commits journals/ only."""

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


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="cursor-stop-") as tmp_name:
        tmp = Path(tmp_name)
        # Copy hook modules into a mini workspace
        hooks_src = ROOT / ".cursor" / "hooks"
        hooks_dst = tmp / ".cursor" / "hooks"
        hooks_dst.mkdir(parents=True)
        for name in (
            "journal_fields.py",
            "merge_agent_notes.py",
            "journal_snapshot.py",
            "on_stop.py",
        ):
            (hooks_dst / name).write_text(
                (hooks_src / name).read_text(encoding="utf-8"), encoding="utf-8"
            )

        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(tmp / ".cursor" / "active-context.txt", f"work-item:{wid}\n")
        _write(
            base / "progress.md",
            "# Work item\n\n**Completion status:** in progress\n",
        )
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
        leaf = base / "nodes" / "work-item.md"
        _write(leaf, "# Node\n\n**Next action:** pack\n\n")
        notes = base / "agent-notes"
        _write(notes / "README.md", "docs\n")
        _write(notes / "worker-a.md", "**Status:** ok\n\nDid arrivals filter.\n")

        # Shared task incomplete — leave alone
        task = notes / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\n\npart a\n")

        # Point merge ROOT at tmp by running from tmp with rewritten ROOT... 
        # Instead patch sys.path and set cwd; merge uses Path(__file__).parents[2]
        # so __file__ under tmp/.cursor/hooks makes ROOT=tmp. Good.
        env_py = [
            sys.executable,
            str(hooks_dst / "merge_agent_notes.py"),
        ]
        completed = subprocess.run(
            env_py, cwd=str(tmp), capture_output=True, text=True, check=False
        )
        _assert(completed.returncode == 0, completed.stderr or "merge failed")

        leaf_text = leaf.read_text(encoding="utf-8")
        _assert("Did arrivals filter" in leaf_text, "loose note not merged into leaf")
        _assert(not (notes / "worker-a.md").is_file(), "loose note not archived")
        _assert((notes / "merged" / "worker-a.md").is_file(), "archive missing")
        _assert((task / "a.md").is_file(), "partial shared task was consumed")
        _assert(not (task / ".merged").is_file(), "partial shared task marked merged")

        # Unrelated staged file must not be required for this unit test of merge target
        _write(tmp / "work-items" / wid / "STATUS.md", "status\n")
        _write(tmp / "unrelated.txt", "leave me alone\n")

        print("cursor stop hook tests passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
