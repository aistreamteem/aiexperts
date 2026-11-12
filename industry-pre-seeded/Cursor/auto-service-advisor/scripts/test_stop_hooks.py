"""Stop-hook merge writes to the active leaf; shared incomplete tasks wait."""

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


def _run_merge(workspace: Path) -> None:
    env_py = str(HOOKS / "merge_agent_notes.py")
    completed = subprocess.run(
        [sys.executable, env_py],
        cwd=str(workspace),
        capture_output=True,
        text=True,
        check=False,
        env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "PYTHONPATH": str(HOOKS)},
    )
    # merge always exits 0; import path: run via -c from hooks dir
    if completed.returncode != 0:
        # Fallback: execute with sys.path injection
        code = (
            "import sys; from pathlib import Path; "
            f"sys.path.insert(0, r'{HOOKS}'); "
            "import merge_agent_notes; "
            f"merge_agent_notes.ROOT = Path(r'{workspace}'); "
            "raise SystemExit(merge_agent_notes.main())"
        )
        completed = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(workspace),
            capture_output=True,
            text=True,
            check=False,
        )
    _assert(completed.returncode == 0, completed.stderr or completed.stdout or "merge failed")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-stop-"))
    try:
        # Copy hooks so imports resolve relative to a fake root that also has hooks
        shutil.copytree(HOOKS, tmp / ".cursor" / "hooks")
        wid = "WID-TEST"
        jbase = tmp / "journals" / "work-items" / wid
        _write(
            jbase / "state.json",
            json.dumps(
                {
                    "active": ["work-item", "pack"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []},
                        "pack": {"parent": "work-item", "status": "open", "history": []},
                    },
                }
            ),
        )
        _write(jbase / "progress.md", "# WI\n\n**Completion status:** in progress\n")
        _write(jbase / "nodes" / "work-item.md", "# root\n\n**Next action:**\n")
        _write(
            jbase / "nodes" / "pack.md",
            "# pack\n\n**Next action:** finish pack\n\n**Last completed:** start\n",
        )
        _write(
            jbase / "agent-notes" / "README.md",
            "# notes\n",
        )
        _write(jbase / "agent-notes" / "scout.md", "**Status:** ok\n\nFound parts file.\n")
        (tmp / "work-items" / wid).mkdir(parents=True, exist_ok=True)

        # Point merge ROOT at tmp by running from copied hooks with patched ROOT
        merge_path = tmp / ".cursor" / "hooks" / "merge_agent_notes.py"
        text = merge_path.read_text(encoding="utf-8")
        text = text.replace(
            "ROOT = Path(__file__).resolve().parents[2]",
            f"ROOT = Path(r'{tmp}')",
        )
        merge_path.write_text(text, encoding="utf-8")
        snap = tmp / ".cursor" / "hooks" / "journal_snapshot.py"
        # Avoid git commits in the test: stub snapshot
        snap.write_text(
            "def snapshot_work_item(root, work_id):\n    return\n\n"
            "def main():\n    return 0\n",
            encoding="utf-8",
        )

        completed = subprocess.run(
            [sys.executable, str(merge_path)],
            cwd=str(tmp),
            capture_output=True,
            text=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "loose merge failed")
        pack = (jbase / "nodes" / "pack.md").read_text(encoding="utf-8")
        _assert("Found parts file" in pack, "loose note not merged into active leaf")
        _assert(not (jbase / "agent-notes" / "scout.md").is_file(), "loose note not archived")
        _assert((jbase / "agent-notes" / "merged" / "scout.md").is_file(), "archive missing")

        # Shared task with one subtask missing: left alone
        task = jbase / "agent-notes" / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "scan", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\n\nA done\n")
        completed = subprocess.run(
            [sys.executable, str(merge_path)],
            cwd=str(tmp),
            capture_output=True,
            text=True,
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "shared wait failed")
        _assert((task / "a.md").is_file(), "partial shared task was consumed")
        _assert(not (task / ".merged").is_file(), "partial shared task marked merged")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
