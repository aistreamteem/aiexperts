"""Stop-hook merge writes into the active leaf; audit commit stays scoped."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".cursor" / "hooks"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    sys.path.insert(0, str(HOOKS))
    from merge_agent_notes import process_work_item  # type: ignore

    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "state.json",
            json.dumps(
                {
                    "active": ["work-item", "map-step"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []},
                        "map-step": {"parent": "work-item", "status": "open", "history": []},
                    },
                }
            ),
        )
        leaf = base / "nodes" / "map-step.md"
        _write(leaf, "# map-step\n\n**Next action:** wait for operator\n")
        notes = base / "agent-notes"
        _write(notes / "README.md", "# notes\n")
        _write(
            notes / "helper.md",
            "**Status:** succeeded\n\nLOOSE_NOTE_BODY\n",
        )
        tasks = notes / "tasks" / "pack"
        _write(
            tasks / "manifest.json",
            json.dumps({"task": "pack", "subtasks": ["a", "b"]}),
        )
        _write(tasks / "a.md", "**Status:** succeeded\n\nA_OK\n")
        # b missing → shared task must stay untouched

        _assert(process_work_item(tmp, wid) is True, "loose note did not merge")
        body = leaf.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in body, "loose note missing from leaf")
        _assert(not (notes / "helper.md").is_file(), "loose note not archived")
        _assert((notes / "merged" / "helper.md").is_file(), "loose note archive missing")
        _assert((tasks / "a.md").is_file(), "partial shared task was consumed early")
        _assert(not (tasks / ".merged").is_file(), "partial shared task marked merged")

        # Unrelated staged file must not be required for merge success.
        unrelated = tmp / "unrelated.txt"
        unrelated.write_text("leave me alone\n", encoding="utf-8")
        _assert(unrelated.read_text(encoding="utf-8") == "leave me alone\n", "fixture drift")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
