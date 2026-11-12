"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import (
    active_leaf,
    active_work_id,
    field,
    journals_dir,
    read_text,
    work_items_dir,
)


def _log(msg: str) -> None:
    print(f"[journal-snapshot] {msg}", file=sys.stderr)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )


def _ensure_repo(root: Path) -> bool:
    inside = _git(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode == 0 and inside.stdout.strip() == "true":
        return True
    _log("No enclosing Git repository - initializing one for audit log...")
    init = _git(root, "init", "-q")
    if init.returncode != 0:
        _log("git init failed")
        return False
    _git(root, "config", "user.name", "Cursor Expert Agent")
    _git(root, "config", "user.email", "expert@cursor.local")
    ignore = root / ".gitignore"
    if not ignore.is_file():
        ignore.write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "Initial commit: Expert template baseline")
    return True


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    check = _git(root, "check-ignore", "-q", rel)
    return check.returncode == 0


def snapshot_work_item(root: Path, work_id: str) -> int:
    if not work_id:
        work_id = active_work_id(root)
    if not work_id:
        _log("No active Work Item - skipping audit log")
        return 0
    if not _ensure_repo(root):
        return 0

    jdir = journals_dir(root, work_id)
    session = work_items_dir(root, work_id)
    expert = root / "journals" / "expert" / "progress.md"
    status = session / "STATUS.md"
    needs = session / "NEEDS-ATTENTION.md"
    state = {}
    state_path = jdir / "state.json"
    try:
        state = json.loads(read_text(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        state = {}
    leaf = active_leaf(state if isinstance(state, dict) else {})
    node = jdir / "nodes" / f"{leaf}.md" if leaf else None
    phase = "/".join(state.get("active") or []) if isinstance(state, dict) else ""
    next_action = field(read_text(node), "Next action") if node and node.is_file() else ""
    last_completed = (
        field(read_text(node), "Last completed") if node and node.is_file() else ""
    )

    commit_paths: list[str] = []
    candidates = [expert, jdir, status, needs]
    for path in candidates:
        if not path.exists():
            continue
        if _ignored(root, path):
            _log(f"{path} is gitignored - merged on disk, skipping commit paths")
            continue
        try:
            rel = str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            continue
        commit_paths.append(rel)

    if not commit_paths:
        _log(f"No tracked journal paths for {work_id}")
        return 0

    # If the whole journals tree is ignored, skip commit entirely.
    if _ignored(root, jdir):
        _log(f"Session {work_id} journal is gitignored - skipping git commit")
        return 0

    add = _git(root, "add", "--", *commit_paths)
    if add.returncode != 0:
        _log(f"git add failed: {add.stderr.strip()}")
        return 0
    diff = _git(root, "diff", "--cached", "--quiet", "--", *commit_paths)
    if diff.returncode == 0:
        _log(f"No tracked journal changes to commit for {work_id}")
        return 0

    attention = ""
    if needs.is_file():
        attention = " [NEEDS-ATTENTION]"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{work_id}: {phase or 'unknown'} → {next_action or 'unknown'}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase or 'unknown'}\n"
        f"Completed: {last_completed or 'none'}\n"
        f"Next: {next_action or 'unknown'}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _git(root, "commit", "-q", "-m", body, "--", *commit_paths)
    if commit.returncode == 0:
        _log(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}")
    else:
        _log("Failed to commit audit snapshot (may be no changes)")
    return 0


def main() -> int:
    root = Path.cwd()
    work_id = sys.argv[1] if len(sys.argv) > 1 else active_work_id(root)
    return snapshot_work_item(root, work_id)


if __name__ == "__main__":
    raise SystemExit(main())
