"""Commit an audit snapshot of the real journals for one work item.

Commits only journal paths (never unrelated staged files). Always exits 0.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text, work_id

ROOT = Path(__file__).resolve().parents[2]


def log(msg: str) -> None:
    print(f"[journal-snapshot] {msg}", file=sys.stderr)


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    return _run(["git", "rev-parse", "--is-inside-work-tree"], root).returncode == 0


def _ensure_git(root: Path) -> bool:
    if _inside_git(root):
        return True
    log("No enclosing Git repository - initializing one for audit log...")
    init = _run(["git", "init", "-q"], root)
    if init.returncode != 0:
        log("git init failed")
        return False
    _run(["git", "config", "user.name", "Cursor Expert Agent"], root)
    _run(["git", "config", "user.email", "expert@cursor.local"], root)
    return True


def _active_phase(state_path: Path) -> str:
    if not state_path.is_file():
        return "unknown"
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return "unknown"
    leaf = active[-1]
    return leaf if isinstance(leaf, str) and leaf.strip() else "unknown"


def _gitignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    proc = _run(["git", "check-ignore", "-q", rel], root)
    return proc.returncode == 0


def snapshot_work_item(root: Path, wid: str) -> int:
    if not wid:
        wid = work_id(root)
    if not wid:
        log("No active Work Item - skipping audit log")
        return 0

    journals = root / "journals" / "work-items" / wid
    status = root / "work-items" / wid / "STATUS.md"
    needs = root / "work-items" / wid / "NEEDS-ATTENTION.md"
    expert = root / "journals" / "expert" / "progress.md"
    state_path = journals / "state.json"
    leaf = _active_phase(state_path)
    leaf_note = journals / "nodes" / f"{leaf}.md"
    leaf_text = read_text(leaf_note) if leaf_note.is_file() else ""
    next_action = field(leaf_text, "Next action") or "unknown"
    last_completed = field(leaf_text, "Last completed") or "none"
    phase = leaf

    if not journals.is_dir():
        log(f"Journal folder not found for {wid} - skipping")
        return 0

    if not _ensure_git(root):
        return 0

    if _gitignored(root, journals / "progress.md"):
        log(f"Session {wid} is gitignored - merge is on disk, skipping commit")
        return 0

    paths: list[str] = []
    if expert.is_file():
        paths.append(str(expert.relative_to(root)).replace("\\", "/"))
    # whole journals/work-items/<id>/
    for path in journals.rglob("*"):
        if path.is_file():
            paths.append(str(path.relative_to(root)).replace("\\", "/"))
    if status.is_file():
        paths.append(str(status.relative_to(root)).replace("\\", "/"))
    if needs.is_file():
        paths.append(str(needs.relative_to(root)).replace("\\", "/"))

    if not paths:
        return 0

    _run(["git", "add", "--", *paths], root)
    staged = _run(["git", "diff", "--cached", "--quiet", "--", *paths], root)
    if staged.returncode == 0:
        log(f"No tracked journal changes to commit for {wid}")
        return 0

    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    subject = f"WI-{wid}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Completed: {last_completed}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _run(["git", "commit", "-q", "-m", body, "--", *paths], root)
    if commit.returncode == 0:
        log(f"Audit snapshot committed for WI-{wid}: {phase} → {next_action}")
    else:
        log("Failed to commit audit snapshot (may be no changes)")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    wid = ""
    if argv:
        wid = Path(argv[0]).name
    return snapshot_work_item(ROOT, wid)


if __name__ == "__main__":
    raise SystemExit(main())
