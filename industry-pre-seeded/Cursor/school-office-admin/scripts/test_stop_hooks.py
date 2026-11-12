"""Stop-hook merge targets the real journal node, not the legacy pointer."""

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
        sys.path.insert(0, str(HOOKS))
        from merge_agent_notes import process_work_item  # noqa: E402

        wid = "WID-TEST"
        jbase = tmp / "journals" / "work-items" / wid
        nodes = jbase / "nodes"
        notes = jbase / "agent-notes"
        nodes.mkdir(parents=True)
        notes.mkdir(parents=True)
        (tmp / "work-items" / wid).mkdir(parents=True)
        (tmp / ".cursor").mkdir(parents=True)
        (tmp / ".cursor" / "active-context.txt").write_text(
            f"work-item:{wid}\n", encoding="utf-8"
        )
        (jbase / "state.json").write_text(
            json.dumps(
                {
                    "active": ["work-item"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []}
                    },
                }
            ),
            encoding="utf-8",
        )
        leaf = nodes / "work-item.md"
        leaf.write_text("# work-item\n\n**Next action:** wait\n", encoding="utf-8")
        (notes / "alpha.md").write_text(
            "**Status:** ok\n\nDid the CSV check.\n", encoding="utf-8"
        )

        # Shared task with one subtask missing must stay untouched.
        task = notes / "tasks" / "t1"
        task.mkdir(parents=True)
        (task / "manifest.json").write_text(
            json.dumps({"task": "pair", "subtasks": ["a", "b"]}),
            encoding="utf-8",
        )
        (task / "a.md").write_text("**Status:** ok\n\nonly a\n", encoding="utf-8")

        cwd = Path.cwd()
        try:
            import os

            os.chdir(tmp)
            process_work_item(tmp, wid)
        finally:
            os.chdir(cwd)

        body = leaf.read_text(encoding="utf-8")
        _assert("Did the CSV check" in body, "loose note not merged into active node")
        _assert(not (notes / "alpha.md").exists(), "loose note not archived")
        _assert((notes / "merged" / "alpha.md").is_file(), "loose note missing from merged/")
        _assert((task / "a.md").is_file(), "partial shared task was consumed early")
        _assert(not (task / ".merged").exists(), "partial shared task marked merged")

        # on_stop always prints {}
        completed = subprocess.run(
            [sys.executable, str(HOOKS / "on_stop.py")],
            input="{}",
            text=True,
            capture_output=True,
            cwd=str(tmp),
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "on_stop failed")
        _assert(completed.stdout.strip() == "{}", f"bad stdout: {completed.stdout!r}")
        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
