"""Stop-hook merge and audit snapshot behaviour."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".cursor" / "hooks"
sys.path.insert(0, str(HOOKS))

from merge_agent_notes import process_work_item  # noqa: E402
from journal_snapshot import snapshot_work_item  # noqa: E402


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
        jbase = tmp / "journals" / "work-items" / wid
        _write(
            jbase / "state.json",
            json.dumps({"active": ["work-item"], "nodes": {"work-item": {"parent": None}}}),
        )
        node = jbase / "nodes" / "work-item.md"
        _write(node, "# work-item\n\n**Next action:** bake-list-day:list\n\n")
        _write(tmp / "journals" / "expert" / "progress.md", "**Current work item:** WID-TEST\n")
        _write(tmp / "work-items" / wid / "STATUS.md", "Work Item Status\n")
        _write(tmp / ".cursor" / "active-context.txt", "work-item:WID-TEST\n")

        # Loose note merges into active node
        notes = jbase / "agent-notes"
        _write(notes / "scale.md", "**Status:** ok\n\nScaled flour.\n")
        process_work_item(tmp, notes)
        body = node.read_text(encoding="utf-8")
        _assert("Scaled flour" in body, "loose note missing from node")
        _assert(not (notes / "scale.md").is_file(), "loose note not archived")
        _assert((notes / "merged" / "scale.md").is_file(), "loose note archive missing")

        # Shared task with one subtask missing is left alone
        task = notes / "tasks" / "join"
        _write(
            task / "manifest.json",
            json.dumps({"task": "join", "subtasks": ["csv", "pdfs"]}),
        )
        _write(task / "csv.md", "**Status:** ok\n\nCSV done\n")
        before = node.read_text(encoding="utf-8")
        process_work_item(tmp, notes)
        after = node.read_text(encoding="utf-8")
        _assert(before == after, "partial shared task should not merge")
        _assert((task / "csv.md").is_file(), "partial subtask note removed early")

        # Complete shared task
        _write(task / "pdfs.md", "**Status:** ok\n\nPDFs done\n")
        process_work_item(tmp, notes)
        body = node.read_text(encoding="utf-8")
        _assert("Background Task Complete: join" in body, "shared task header missing")
        _assert((task / ".merged").is_file(), "shared task not marked merged")

        # Audit commit contains journals paths and not an unrelated staged file
        subprocess.run(["git", "init", "-q"], cwd=str(tmp), check=True)
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=str(tmp),
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=str(tmp),
            check=True,
        )
        unrelated = tmp / "secrets.txt"
        unrelated.write_text("do-not-commit\n", encoding="utf-8")
        subprocess.run(["git", "add", "secrets.txt"], cwd=str(tmp), check=True)
        _write(node, node.read_text(encoding="utf-8") + "\nextra note\n")
        snapshot_work_item(tmp, wid)
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        # secrets should remain staged alone if commit used pathspec; verify last commit
        show = subprocess.run(
            ["git", "show", "--name-only", "--pretty=format:", "HEAD"],
            cwd=str(tmp),
            text=True,
            capture_output=True,
            check=False,
        )
        if show.returncode == 0 and show.stdout.strip():
            names = show.stdout.strip().splitlines()
            _assert(
                any(n.replace("\\", "/").startswith("journals/") for n in names),
                f"commit missing journals paths: {names}",
            )
            _assert(
                "secrets.txt" not in names,
                f"unrelated staged file was committed: {names}",
            )
        else:
            # If commit skipped (e.g. nothing tracked yet), ensure secrets still only staged file intent
            _assert("secrets.txt" in staged, "expected unrelated file to stay staged")

        # on_stop always emits {}
        completed = subprocess.run(
            [sys.executable, str(HOOKS / "on_stop.py")],
            input="{}",
            text=True,
            capture_output=True,
            cwd=str(tmp),
            check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "on_stop failed")
        _assert(completed.stdout.strip() == "{}", f"bad on_stop stdout: {completed.stdout!r}")

    print("cursor stop hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
