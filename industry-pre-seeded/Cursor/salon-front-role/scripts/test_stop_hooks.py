"""Stop hooks: note merge into the active node, shared-task gating, scoped audit commit."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".cursor" / "hooks"
WID = "WID-TEST"
LEAF = "implement"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def _run_stop(work: Path, payload: dict | None = None) -> str:
    result = subprocess.run(
        [sys.executable, str(work / ".cursor" / "hooks" / "on_stop.py")],
        cwd=str(work),
        input=json.dumps(payload or {}),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    _assert(result.returncode == 0, f"on_stop exited {result.returncode}: {result.stderr}")
    _assert(result.stdout.strip() == "{}", f"on_stop stdout was {result.stdout!r}")
    return result.stderr


def _build(work: Path) -> dict[str, Path]:
    shutil.copytree(HOOKS, work / ".cursor" / "hooks", ignore=shutil.ignore_patterns("__pycache__"))
    _write(work / ".cursor" / "active-context.txt", f"work-item:{WID}\n")
    base = work / "journals" / "work-items" / WID
    _write(work / "journals" / "expert" / "progress.md", f"# Expert journal\n\n**Current work item:** {WID}\n")
    _write(base / "progress.md", "# Work item journal\n\n**Completion status:** in progress\n")
    _write(base / "state.json", json.dumps({"active": ["work-item", LEAF], "nodes": {}}))
    _write(base / "nodes" / "work-item.md", "# work-item\n\n**Next action:** root\n")
    _write(base / "nodes" / f"{LEAF}.md", f"# {LEAF}\n\n**Next action:** write the tests\n")
    _write(work / "work-items" / WID / "STATUS.md", "# Status\n")
    notes = base / "agent-notes"
    _write(notes / "README.md", "docs, never merged\n")
    _write(notes / "scout.md", "**Status:** done\nLOOSE-NOTE-MARKER\n")
    task = notes / "tasks" / "t1"
    _write(task / "manifest.json", json.dumps({"task": "split", "subtasks": ["a", "b"]}))
    _write(task / "a.md", "**Status:** done\nSUBTASK-A-MARKER\n")
    return {"base": base, "notes": notes, "task": task, "node": base / "nodes" / f"{LEAF}.md"}


def main() -> int:
    have_git = shutil.which("git") is not None
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        p = _build(work)
        if have_git:
            _assert(_git(work, "init", "-q").returncode == 0, "git init")
            _git(work, "config", "user.name", "Test")
            _git(work, "config", "user.email", "test@example.invalid")
            _git(work, "config", "commit.gpgsign", "false")
            _write(work / "baseline.txt", "baseline\n")
            _git(work, "add", "baseline.txt")
            _git(work, "commit", "-q", "-m", "baseline")
            _write(work / "unrelated.txt", "someone else's work\n")
            _git(work, "add", "unrelated.txt")

        # A loop-guarded stop must not merge.
        _run_stop(work, {"stop_hook_active": True})
        _assert((p["notes"] / "scout.md").is_file(), "stop_hook_active should skip the merge")

        _run_stop(work)

        node = p["node"].read_text(encoding="utf-8")
        _assert("LOOSE-NOTE-MARKER" in node, "loose note content missing from active node")
        _assert(not (p["notes"] / "scout.md").exists(), "loose note was not moved")
        _assert((p["notes"] / "merged" / "scout.md").is_file(), "loose note not archived to merged/")
        _assert((p["notes"] / "README.md").is_file(), "README.md must not be merged")
        _assert("LOOSE-NOTE-MARKER" not in (p["base"] / "progress.md").read_text(encoding="utf-8"),
                "note leaked into flat progress.md")
        _assert(not (p["notes"] / ".merge.lock").exists(), "lock left behind")

        # Shared task with a missing subtask is left alone.
        _assert("SUBTASK-A-MARKER" not in node, "incomplete shared task was merged")
        _assert((p["task"] / "a.md").is_file(), "incomplete task note was moved")
        _assert(not (p["task"] / ".merged").exists(), "incomplete task marked merged")

        # Completing the task merges it once.
        _write(p["task"] / "b.md", "**Status:** FAILED after retries\nSUBTASK-B-MARKER\n")
        _run_stop(work)
        node = p["node"].read_text(encoding="utf-8")
        _assert("SUBTASK-A-MARKER" in node and "SUBTASK-B-MARKER" in node, "completed task not merged")
        _assert("PARTIAL" in node, "failed subtask should make the merge partial")
        _assert((p["task"] / ".merged").is_file(), ".merged marker missing")
        _assert((work / "work-items" / WID / "NEEDS-ATTENTION.md").is_file(), "NEEDS-ATTENTION.md missing")
        _assert((p["notes"] / "merged" / "t1" / "manifest.json").is_file(), "manifest not archived")
        before = node
        _run_stop(work)
        _assert(p["node"].read_text(encoding="utf-8") == before, "second run merged again")

        if have_git:
            log = _git(work, "log", "-1", "--name-only", "--format=%s").stdout
            _assert(log.startswith(f"WI-{WID}:"), f"unexpected commit subject: {log!r}")
            _assert("write the tests" in log, "subject should carry the node's Next action")
            files = {line.strip() for line in log.splitlines()[1:] if line.strip()}
            _assert(f"journals/work-items/{WID}/nodes/{LEAF}.md" in files, f"node not committed: {files}")
            _assert(f"work-items/{WID}/NEEDS-ATTENTION.md" in files, f"attention file not committed: {files}")
            _assert("unrelated.txt" not in files, "unrelated staged file was swept into the commit")
            staged = _git(work, "diff", "--cached", "--name-only").stdout.split()
            _assert("unrelated.txt" in staged, "unrelated file should remain staged")
            status = _git(work, "status", "--porcelain", "--", "journals", "work-items").stdout
            _assert(not status.strip(), f"journal paths left uncommitted: {status}")
        else:
            print("git not available - commit checks skipped")

    print("test_stop_hooks: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
