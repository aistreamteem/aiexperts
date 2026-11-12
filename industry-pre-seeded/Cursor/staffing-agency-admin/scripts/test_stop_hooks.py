"""Stop-hook merge writes into the active node; shared tasks wait for all notes."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
import merge_agent_notes as merge  # noqa: E402


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        wid = "WID-TEST"
        base = tmp / "journals" / "work-items" / wid
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {"parent": None}}}),
        )
        node = base / "nodes" / "work-item.md"
        _write(node, "# work-item\n\n**Next action:** wait\n")
        notes = base / "agent-notes"
        _write(notes / "worker-a.md", "Loose note body A\n")
        _assert(merge.process_work_item(tmp, wid), "loose note did not merge")
        body = node.read_text(encoding="utf-8")
        _assert("Loose note body A" in body, "loose note missing from node")
        _assert(not (notes / "worker-a.md").is_file(), "loose note not archived")
        _assert((notes / "merged" / "worker-a.md").is_file(), "archive missing")

        task = notes / "tasks" / "pack"
        _write(
            task / "manifest.json",
            json.dumps({"task": "pack", "subtasks": ["one", "two"]}),
        )
        _write(task / "one.md", "**Status:** ok\nfirst\n")
        _assert(not merge.process_work_item(tmp, wid), "partial shared task merged early")
        _assert(not (task / ".merged").is_file(), "partial task marked merged")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
