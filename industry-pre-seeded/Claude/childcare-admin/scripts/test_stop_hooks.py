"""Stop-hook merge writes into the active node and leaves incomplete shared tasks alone."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
from merge_agent_notes import merge_all  # noqa: E402


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-stop-"))
    try:
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        notes = base / "agent-notes"
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item", "intake"], "nodes": {}}),
        )
        leaf = base / "nodes" / "intake.md"
        _write(leaf, "# intake\n\n**Next action:** gather sources\n")
        _write(notes / "README.md", "docs\n")
        _write(notes / "helper.md", "LOOSE_NOTE_BODY\n")

        # Incomplete shared task must stay untouched.
        task = notes / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "split", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** done\nA_ONLY\n")

        merged = merge_all(tmp)
        _assert(wid in merged, "expected merge for WID-TEST")
        body = leaf.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in body, "loose note missing from leaf")
        _assert((notes / "merged" / "helper.md").is_file(), "loose note not archived")
        _assert((task / "a.md").is_file(), "partial shared task was consumed")
        _assert(not (task / ".merged").is_file(), "partial shared task marked merged")

        # Completing the shared task merges it.
        _write(task / "b.md", "**Status:** done\nB_DONE\n")
        merged2 = merge_all(tmp)
        _assert(wid in merged2, "expected second merge")
        body2 = leaf.read_text(encoding="utf-8")
        _assert("B_DONE" in body2, "shared task note missing")
        _assert((task / ".merged").is_file(), "shared task not marked merged")

        print("claude stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
