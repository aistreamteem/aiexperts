"""Commit an audit snapshot of the real journal after a merge."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text

ROOT = Path(__file__).resolve().parents[2]


def _log(msg: str) -> None:
    print(f"[journal-snapshot] {msg}", file=sys.stderr)


def _git(args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=check,
    )


def _inside_git() -> bool:
    return _git(["rev-parse", "--is-inside-work-tree"]).returncode == 0


def _ensure_git() -> bool:
    if _inside_git():
        return True
    _log("No enclosing Git repository - initializing one for audit log...")
    init = _git(["init", "-q"])
    if init.returncode != 0:
        return False
    _git(["config", "user.name", "Claude Expert Agent"])
    _git(["config", "user.email", "expert@claude.local"])
    return True


def _active_phase(wid: str) -> str:
    state_path = ROOT / "journals" / "work-items" / wid / "state.json"
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return "unknown"
    leaf = active[-1]
    return str(leaf) if leaf else "unknown"


def _leaf_next_action(wid: str, phase: str) -> str:
    note = ROOT / "journals" / "work-items" / wid / "nodes" / f"{phase}.md"
    if not note.is_file():
        return "unknown"
    value = field(read_text(note), "Next action")
    return value or "unknown"


def snapshot(wid: str | None = None) -> int:
    work_id = (wid or "").strip() or active_work_id(ROOT)
    if not work_id:
        _log("No active Work Item - skipping audit log")
        return 0

    journals = ROOT / "journals" / "work-items" / work_id
    if not journals.is_dir():
        _log(f"Journal folder missing for {work_id} - skip")
        return 0

    if not _ensure_git():
        return 0

    status_path = ROOT / "work-items" / work_id / "STATUS.md"
    needs = ROOT / "work-items" / work_id / "NEEDS-ATTENTION.md"
    expert = ROOT / "journals" / "expert" / "progress.md"

    paths: list[str] = []
    if expert.is_file():
        paths.append(str(expert.relative_to(ROOT)).replace("\\", "/"))
    # Whole journals/work-items/<id>/
    for path in journals.rglob("*"):
        if path.is_file():
            paths.append(str(path.relative_to(ROOT)).replace("\\", "/"))
    if status_path.is_file():
        paths.append(str(status_path.relative_to(ROOT)).replace("\\", "/"))
    if needs.is_file():
        paths.append(str(needs.relative_to(ROOT)).replace("\\", "/"))

    # External / gitignored journals: merge stays on disk, skip commit
    ignored = False
    for rel in paths:
        check = _git(["check-ignore", "-q", rel])
        if check.returncode == 0:
            ignored = True
            break
    if ignored:
        _log(f"Session {work_id} is gitignored - merged on disk, skipping git commit")
        return 0

    phase = _active_phase(work_id)
    next_action = _leaf_next_action(work_id, phase)
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    subject = f"WI-{work_id}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )

    add = _git(["add", "--", *paths])
    if add.returncode != 0:
        _log("git add failed")
        return 0

    staged = _git(["diff", "--cached", "--quiet", "--", *paths])
    if staged.returncode == 0:
        _log(f"No tracked journal changes to commit for {work_id}")
        return 0

    commit = _git(["commit", "-q", "-m", body, "--", *paths])
    if commit.returncode == 0:
        _log(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}")
    else:
        _log("Failed to commit audit snapshot (may be no changes)")
    return 0


def main() -> int:
    wid = sys.argv[1] if len(sys.argv) > 1 else None
    return snapshot(wid)


if __name__ == "__main__":
    raise SystemExit(main())
