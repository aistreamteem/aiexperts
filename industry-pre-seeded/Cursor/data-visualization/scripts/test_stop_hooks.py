"""Stop-hook merge targets the active journal node and audits journals/ paths."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
import merge_agent_notes  # noqa: E402
import journal_snapshot  # noqa: E402


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
        _write(tmp / ".cursor" / "active-context.txt", f"work-item:{wid}\n")
        _write(tmp / "journals" / "expert" / "progress.md", f"**Current work item:** {wid}\n")
        _write(
            base / "progress.md",
            "**Work item ID:** WID-TEST\n**Completion status:** in progress\n",
        )
        _write(
            base / "state.json",
            json.dumps({"active": ["work-item", "chart"], "nodes": {}}),
        )
        node = base / "nodes" / "chart.md"
        _write(node, "**Next action:** pack\n\n## Step notes\n\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "status\n")

        # Loose note merges into active leaf.
        _write(
            base / "agent-notes" / "plotter.md",
            "**Status:** ok\n\nPlotted the chart.\n",
        )
        merged = merge_agent_notes.process_work_item(tmp, wid)
        _assert(merged, "loose note did not merge")
        body = node.read_text(encoding="utf-8")
        _assert("Plotted the chart" in body, "loose note missing from node")
        _assert(not (base / "agent-notes" / "plotter.md").exists(), "loose note not archived")
        _assert((base / "agent-notes" / "merged" / "plotter.md").is_file(), "archive missing")

        # Shared task with one subtask missing stays untouched.
        task = base / "agent-notes" / "tasks" / "t1"
        _write(
            task / "manifest.json",
            json.dumps({"task": "dual", "subtasks": ["a", "b"]}),
        )
        _write(task / "a.md", "**Status:** ok\n\nA done\n")
        before = node.read_text(encoding="utf-8")
        again = merge_agent_notes.process_work_item(tmp, wid)
        _assert(not again, "partial shared task should not merge")
        _assert(node.read_text(encoding="utf-8") == before, "partial task mutated journal")
        _assert(not (task / ".merged").exists(), "partial task marked merged")

        # Audit commit paths include journals/ and exclude unrelated staged file.
        subprocess.run(["git", "init"], cwd=tmp, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=tmp,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=tmp,
            check=True,
            capture_output=True,
        )
        _write(tmp / "unrelated.txt", "leave me staged\n")
        subprocess.run(["git", "add", "unrelated.txt"], cwd=tmp, check=True, capture_output=True)
        journal_snapshot.snapshot(tmp, wid)
        show = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:"],
            cwd=tmp,
            text=True,
            capture_output=True,
            check=False,
        )
        names = show.stdout
        _assert("journals/work-items/WID-TEST" in names or "journals/work-items/WID-TEST/" in names or "nodes/chart.md" in names, f"journals missing from commit: {names!r}")
        _assert("unrelated.txt" not in names, "unrelated staged file was committed")

        print("cursor stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
