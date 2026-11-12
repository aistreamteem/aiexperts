"""Stop-hook merge and audit path behaviour."""

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


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
        wi = tmp / "journals" / "work-items" / "WID-TEST"
        shutil.copytree(ROOT / "journals" / "work-items" / "_TEMPLATE", wi)
        (tmp / "work-items" / "WID-TEST").mkdir(parents=True)
        (tmp / "work-items" / "WID-TEST" / "STATUS.md").write_text("status\n", encoding="utf-8")
        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)
        (tmp / ".cursor" / "active-context.txt").write_text("work-item:WID-TEST\n", encoding="utf-8")

        (wi / "state.json").write_text(
            json.dumps(
                {
                    "active": ["work-item", "intake"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []},
                        "intake": {"parent": "work-item", "status": "open", "history": []},
                    },
                }
            ),
            encoding="utf-8",
        )
        leaf = wi / "nodes" / "intake.md"
        leaf.write_text("**Next action:** run charter-writer\n", encoding="utf-8")

        notes = wi / "agent-notes"
        notes.mkdir(parents=True, exist_ok=True)
        (notes / "README.md").write_text("docs\n", encoding="utf-8")
        (notes / "bg-1.md").write_text("LOOSE_NOTE_BODY\n", encoding="utf-8")

        shared = notes / "tasks" / "t1"
        shared.mkdir(parents=True)
        (shared / "manifest.json").write_text(
            json.dumps({"task": "shared", "subtasks": ["a", "b"]}),
            encoding="utf-8",
        )
        (shared / "a.md").write_text("SUB_A\n", encoding="utf-8")
        # b.md intentionally missing → shared task must stay unmerged

        env_python = sys.executable
        merge = subprocess.run(
            [env_python, str(HOOKS / "merge_agent_notes.py")],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        _assert(merge.returncode == 0, merge.stderr or merge.stdout or "merge failed")
        leaf_text = leaf.read_text(encoding="utf-8")
        _assert("LOOSE_NOTE_BODY" in leaf_text, "loose note not merged into active node")
        _assert("SUB_A" not in leaf_text, "partial shared task leaked into journal")
        _assert((shared / "a.md").is_file(), "partial shared note was archived early")
        _assert(not (shared / ".merged").is_file(), "partial shared task marked merged")
        _assert((notes / "merged" / "bg-1.md").is_file(), "loose note not archived")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
