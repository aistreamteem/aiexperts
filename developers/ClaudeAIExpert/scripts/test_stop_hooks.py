"""Tests for the Python stop / merge / snapshot hooks (stdlib only)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "hooks"))

import journal_fields  # noqa: E402
import journal_snapshot  # noqa: E402
import merge_agent_notes  # noqa: E402
import on_stop  # noqa: E402

WID = "WID-TEST"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", check=False
    )
    if done.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {done.stderr}")
    return done.stdout


def make_workspace(base: Path, active: list[str] | None = None) -> Path:
    """Workspace the way the continue skill sets one up."""
    root = base
    wi = root / "journals" / "work-items" / WID
    _write(root / ".claude" / "active-context.txt", f"work-item:{WID}\n")
    _write(root / "journals" / "expert" / "progress.md", "**Current work item:** other\n")
    _write(wi / "progress.md", "**Completion status:** in progress\n")
    path = active or ["work-item", "spec"]
    nodes = {n: {"parent": None, "status": "open", "history": []} for n in path}
    _write(wi / "state.json", json.dumps({"active": path, "nodes": nodes}))
    _write(wi / "nodes" / "work-item.md", "# work-item\n\n**Next action:** root step\n")
    _write(wi / "nodes" / "spec.md", "# spec\n\n**Next action:** write the HLD\n")
    return root


def init_repo(root: Path) -> None:
    _git(root, "init", "-q")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "baseline")


def test_fields(tmp: Path) -> None:
    root = make_workspace(tmp / "fields")
    _assert(journal_fields.field("**Next action:** go\n", "Next action") == "go", "bold field")
    _assert(journal_fields.field("Next action: go\n", "next ACTION") == "go", "plain field")
    _assert(journal_fields.active_work_id(root) == WID, "active-context lookup")
    (root / ".claude" / "active-context.txt").unlink()
    _assert(journal_fields.active_work_id(root) == "other", "expert journal fallback")
    _write(root / ".claude" / "active-work-item.txt", "LEGACY-1\n")
    _assert(journal_fields.active_work_id(root) == "LEGACY-1", "legacy pointer fallback")
    _assert(journal_fields.active_leaf(root, WID) == "spec", "active leaf")


def test_loose_note(tmp: Path) -> None:
    root = make_workspace(tmp / "loose")
    notes = root / "journals" / "work-items" / WID / "agent-notes"
    _write(notes / "note.md", "LOOSE_NOTE_BODY\n")
    _write(notes / "README.md", "docs, not a note\n")
    merged = merge_agent_notes.merge_all(root)
    _assert(merged == [WID], f"loose note not merged: {merged}")
    leaf = (root / "journals" / "work-items" / WID / "nodes" / "spec.md").read_text(encoding="utf-8")
    _assert("LOOSE_NOTE_BODY" in leaf, "loose note missing from active leaf node")
    root_node = (root / "journals" / "work-items" / WID / "nodes" / "work-item.md").read_text(encoding="utf-8")
    _assert("LOOSE_NOTE_BODY" not in root_node, "note merged into the wrong node")
    _assert((notes / "merged" / "note.md").is_file(), "note not archived")
    _assert(not (notes / "note.md").exists(), "note left in place")
    _assert((notes / "README.md").is_file(), "README must be left alone")
    _assert(not (notes / ".merge.lock").exists(), "lock left behind")
    _assert(merge_agent_notes.merge_all(root) == [], "second run should be a no-op")


def test_legacy_path(tmp: Path) -> None:
    root = make_workspace(tmp / "legacy")
    legacy = root / "work-items" / WID / "journal" / "agent-notes"
    _write(legacy / "old.md", "LEGACY_NOTE_BODY\n")
    _write(root / "work-items" / "_TEMPLATE" / "journal" / "agent-notes" / "x.md", "TEMPLATE\n")
    _assert(merge_agent_notes.merge_all(root) == [WID], "legacy note not merged")
    leaf = (root / "journals" / "work-items" / WID / "nodes" / "spec.md").read_text(encoding="utf-8")
    _assert("LEGACY_NOTE_BODY" in leaf, "legacy note must land in the node file")
    _assert((legacy / "merged" / "old.md").is_file(), "legacy note not archived")
    _assert((root / "work-items" / "_TEMPLATE" / "journal" / "agent-notes" / "x.md").is_file(), "_TEMPLATE touched")
    _assert(not (root / "work-items" / WID / "journal" / "progress.md").exists(), "pointer file written")


def _task(root: Path, name: str, subtasks: list[str], deadline: str | None = None) -> Path:
    task_dir = root / "journals" / "work-items" / WID / "agent-notes" / "tasks" / name
    manifest = {"task": name, "subtasks": subtasks}
    if deadline:
        manifest["deadline"] = deadline
    _write(task_dir / "manifest.json", json.dumps(manifest))
    return task_dir


def test_shared_task(tmp: Path) -> None:
    root = make_workspace(tmp / "task")
    leaf_path = root / "journals" / "work-items" / WID / "nodes" / "spec.md"
    before = leaf_path.read_text(encoding="utf-8")
    task_dir = _task(root, "t1", ["a", "b"])
    _write(task_dir / "a.md", "SUBTASK_A\n")
    _assert(merge_agent_notes.merge_all(root) == [], "partial task must not merge")
    _assert(leaf_path.read_text(encoding="utf-8") == before, "partial task leaked into node")
    _assert((task_dir / "a.md").is_file(), "partial task note was moved")
    _assert(not (task_dir / ".merged").exists(), "partial task marked merged")

    _write(task_dir / "b.md", "SUBTASK_B\n")
    _assert(merge_agent_notes.merge_all(root) == [WID], "complete task should merge")
    text = leaf_path.read_text(encoding="utf-8")
    _assert("SUBTASK_A" in text and "SUBTASK_B" in text, "subtasks missing after merge")
    _assert("Background Task Complete: t1" in text, "complete header missing")
    _assert((task_dir / ".merged").is_file(), "merged marker missing")
    archive = root / "journals" / "work-items" / WID / "agent-notes" / "merged" / "t1"
    _assert((archive / "a.md").is_file() and (archive / "manifest.json").is_file(), "task not archived")
    _assert(not (root / "work-items" / WID / "NEEDS-ATTENTION.md").exists(), "unexpected attention file")


def test_failed_task(tmp: Path) -> None:
    root = make_workspace(tmp / "failed")
    task_dir = _task(root, "t2", ["a", "b"])
    _write(task_dir / "a.md", "**Status:** success\nok\n")
    _write(task_dir / "b.md", "**Status:** FAILED after retries\n")
    _assert(merge_agent_notes.merge_all(root) == [WID], "failed task should still merge")
    text = (root / "journals" / "work-items" / WID / "nodes" / "spec.md").read_text(encoding="utf-8")
    _assert("PARTIAL" in text, "partial header missing")
    attention = root / "work-items" / WID / "NEEDS-ATTENTION.md"
    _assert(attention.is_file() and "PARTIAL" in attention.read_text(encoding="utf-8"), "NEEDS-ATTENTION missing")


def test_stalled_task(tmp: Path) -> None:
    root = make_workspace(tmp / "stalled")
    past = (datetime.now().astimezone() - timedelta(hours=1)).isoformat(timespec="seconds")
    task_dir = _task(root, "t3", ["a", "b"], deadline=past)
    _write(task_dir / "a.md", "SUBTASK_A\n")
    leaf_path = root / "journals" / "work-items" / WID / "nodes" / "spec.md"
    _assert(merge_agent_notes.merge_all(root) == [WID], "stalled task should escalate")
    _assert("STALLED" in leaf_path.read_text(encoding="utf-8"), "stall section missing")
    _assert((task_dir / ".stall-warned").is_file(), "stall marker missing")
    _assert(not (task_dir / ".merged").exists(), "stalled task marked merged")
    _assert("STALLED" in (root / "work-items" / WID / "NEEDS-ATTENTION.md").read_text(encoding="utf-8"), "attention file")
    size = len(leaf_path.read_text(encoding="utf-8"))
    _assert(merge_agent_notes.merge_all(root) == [], "stall must escalate only once")
    _assert(len(leaf_path.read_text(encoding="utf-8")) == size, "stall escalated twice")


def test_snapshot_commit(tmp: Path) -> None:
    root = make_workspace(tmp / "git")
    _write(root / "work-items" / WID / "STATUS.md", "status\n")
    _write(root / "other.txt", "baseline\n")
    init_repo(root)
    # User's unrelated staged work, plus unstaged journal edits.
    _write(root / "unrelated.txt", "staged by the user\n")
    _git(root, "add", "unrelated.txt")
    notes = root / "journals" / "work-items" / WID / "agent-notes"
    _write(notes / "note.md", "SNAP_NOTE_BODY\n")
    _write(root / "journals" / "expert" / "progress.md", "**Current work item:** other\nchanged\n")

    _assert(merge_agent_notes.merge_all(root) == [WID], "merge should run")
    log = _git(root, "log", "-1", "--format=%s").strip()
    _assert(log == f"WI-{WID}: work-item/spec \u2192 write the HLD", f"bad commit subject: {log!r}")
    files = set(_git(root, "show", "--name-only", "--format=", "HEAD").split())
    _assert("journals/work-items/WID-TEST/nodes/spec.md" in files, f"leaf node not committed: {files}")
    _assert("journals/work-items/WID-TEST/agent-notes/merged/note.md" in files, f"archive not committed: {files}")
    _assert("journals/expert/progress.md" in files, f"expert journal not committed: {files}")
    _assert("unrelated.txt" not in files, "unrelated staged file was committed")
    staged = _git(root, "diff", "--cached", "--name-only").split()
    _assert(staged == ["unrelated.txt"], f"unrelated file should stay staged: {staged}")

    # No journal changes -> no new commit.
    count = _git(root, "rev-list", "--count", "HEAD").strip()
    _assert(journal_snapshot.snapshot(root, WID) is False, "nothing to commit")
    _assert(_git(root, "rev-list", "--count", "HEAD").strip() == count, "empty commit created")


def test_snapshot_ignored(tmp: Path) -> None:
    root = make_workspace(tmp / "ignored")
    _write(root / ".gitignore", "journals/\n")
    init_repo(root)
    count = _git(root, "rev-list", "--count", "HEAD").strip()
    notes = root / "journals" / "work-items" / WID / "agent-notes"
    _write(notes / "note.md", "IGNORED_NOTE_BODY\n")
    _assert(merge_agent_notes.merge_all(root) == [WID], "merge still happens on disk")
    leaf = (root / "journals" / "work-items" / WID / "nodes" / "spec.md").read_text(encoding="utf-8")
    _assert("IGNORED_NOTE_BODY" in leaf, "ignored journal not merged on disk")
    _assert(_git(root, "rev-list", "--count", "HEAD").strip() == count, "ignored journal was committed")


def test_no_repo_no_init(tmp: Path) -> None:
    root = make_workspace(tmp / "norepo")
    _assert(journal_snapshot.snapshot(root, WID) is False, "no repo means no commit")
    _assert(not (root / ".git").exists(), "snapshot must not git init")


def test_on_stop(tmp: Path) -> None:
    root = make_workspace(tmp / "stop")
    notes = root / "journals" / "work-items" / WID / "agent-notes"
    _write(notes / "note.md", "STOP_NOTE\n")
    on_stop.run(root, {"stop_hook_active": True})
    _assert((notes / "note.md").is_file(), "stop_hook_active must skip the merge")
    on_stop.run(root, {})
    _assert((notes / "merged" / "note.md").is_file(), "stop hook did not merge")

    facts = root / "facts"
    _write(facts / "trigger-index.json", "{}")
    _assert(not on_stop.index_is_stale(root), "fresh index reported stale")
    rules = facts / "rules-custom.md"
    _write(rules, "rule\n")
    import os

    future = (facts / "trigger-index.json").stat().st_mtime + 10
    os.utime(rules, (future, future))
    _assert(on_stop.index_is_stale(root), "any facts/rules-*.md should mark the index stale")


def test_cli_exit_codes() -> None:
    hooks = ROOT / ".claude" / "hooks"
    done = subprocess.run(
        [sys.executable, str(hooks / "on_stop.py")],
        input=json.dumps({"stop_hook_active": True}),
        capture_output=True,
        text=True,
        check=False,
    )
    _assert(done.returncode == 0, f"on_stop exit {done.returncode}: {done.stderr}")
    _assert(json.loads(done.stdout) == {}, f"on_stop output not {{}}: {done.stdout!r}")

def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-stop-hooks-"))
    try:
        test_fields(tmp)
        test_loose_note(tmp)
        test_legacy_path(tmp)
        test_shared_task(tmp)
        test_failed_task(tmp)
        test_stalled_task(tmp)
        test_snapshot_commit(tmp)
        test_snapshot_ignored(tmp)
        test_no_repo_no_init(tmp)
        test_on_stop(tmp)
        test_cli_exit_codes()
        print("stop hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
