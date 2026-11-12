"""Commit an audit snapshot of the real journal paths for one work item.

Commits only known paths; never sweeps unrelated staged files.
Always exits 0.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, active_work_id, field, journals_base, read_text


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
    return True


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    check = _git(root, "check-ignore", "-q", rel)
    return check.returncode == 0


def snapshot_work_item(root: Path, work_id: str | None = None) -> int:
    if not _ensure_repo(root):
        return 0
    wid = work_id or active_work_id(root)
    if not wid:
        _log("No active Work Item - skipping audit log")
        return 0
    base = journals_base(root, wid)
    if not base.is_dir():
        _log(f"Journal folder missing for {wid} - skip")
        return 0

    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / wid / "STATUS.md"
    needs = root / "work-items" / wid / "NEEDS-ATTENTION.md"

    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    paths.append(base)
    if status.is_file():
        paths.append(status)
    if needs.is_file():
        paths.append(needs)

    # Skip commit when the journal tree is outside / ignored
    sample = base / "progress.md"
    if sample.is_file() and _ignored(root, sample):
        _log(f"Session {wid} is gitignored - merged on disk, skipping git commit")
        return 0

    state_raw = read_text(base / "state.json")
    try:
        state = json.loads(state_raw) if state_raw.strip() else {}
    except json.JSONDecodeError:
        state = {}
    leaf = active_leaf(state if isinstance(state, dict) else {})
    phase = leaf or "unknown"
    next_action = "unknown"
    last_completed = "none"
    if leaf:
        node_text = read_text(base / "nodes" / f"{leaf}.md")
        next_action = field(node_text, "Next action") or "unknown"
        last_completed = field(node_text, "Last completed") or "none"

    rels: list[str] = []
    for path in paths:
        try:
            rels.append(str(path.relative_to(root)).replace("\\", "/"))
        except ValueError:
            continue
    if not rels:
        return 0

    add = _git(root, "add", "--", *rels)
    if add.returncode != 0:
        _log("git add failed (merge is on disk)")
        return 0

    diff = _git(root, "diff", "--cached", "--quiet", "--", *rels)
    if diff.returncode == 0:
        _log(f"No tracked journal changes to commit for {wid}")
        return 0

    attention = ""
    if needs.is_file():
        attention = " [NEEDS-ATTENTION]"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{wid}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Completed: {last_completed}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _git(root, "commit", "-q", "-m", body, "--", *rels)
    if commit.returncode == 0:
        _log(f"Audit snapshot committed for WI-{wid}: {phase} → {next_action}")
    else:
        _log("Failed to commit audit snapshot (may be no changes)")
    return 0


def main() -> int:
    root = Path.cwd()
    wid = sys.argv[1] if len(sys.argv) > 1 else None
    return snapshot_work_item(root, wid)


if __name__ == "__main__":
    raise SystemExit(main())
