"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text


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
    init = _run(["git", "init", "-q"], root)
    if init.returncode != 0:
        return False
    _run(["git", "config", "user.name", "Claude Expert Agent"], root)
    _run(["git", "config", "user.email", "expert@claude.local"], root)
    return True


def _phase_from_state(state_path: Path) -> str:
    if not state_path.is_file():
        return "unknown"
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else None
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            return leaf.strip()
    return "unknown"


def snapshot(root: Path, work_id: str | None = None) -> int:
    work_id = (work_id or active_work_id(root) or "").strip()
    if not work_id:
        print("No active Work Item - skipping audit log", file=sys.stderr)
        return 0
    if not _ensure_git(root):
        print("Git unavailable - skipping audit log", file=sys.stderr)
        return 0

    journals = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    needs = root / "work-items" / work_id / "NEEDS-ATTENTION.md"
    state_path = journals / "state.json"
    leaf = _phase_from_state(state_path)
    leaf_note = journals / "nodes" / f"{leaf}.md"
    next_action = field(read_text(leaf_note), "Next action") if leaf_note.is_file() else "unknown"
    if not next_action:
        next_action = "unknown"

    paths: list[str] = []
    if expert.is_file():
        paths.append(str(expert.relative_to(root)).replace("\\", "/"))
    if journals.is_dir():
        paths.append(str(journals.relative_to(root)).replace("\\", "/"))
    if status.is_file():
        paths.append(str(status.relative_to(root)).replace("\\", "/"))
    if needs.is_file():
        paths.append(str(needs.relative_to(root)).replace("\\", "/"))

    if not paths:
        print(f"No journal paths for {work_id}", file=sys.stderr)
        return 0

    ignored = _run(["git", "check-ignore", "-q", paths[0]], root).returncode == 0
    if ignored:
        print(
            f"Work item {work_id} is gitignored - merged on disk, skipping commit",
            file=sys.stderr,
        )
        return 0

    _run(["git", "add", "--", *paths], root)
    staged = _run(["git", "diff", "--cached", "--quiet", "--", *paths], root)
    if staged.returncode == 0:
        print(f"No tracked journal changes to commit for {work_id}", file=sys.stderr)
        return 0

    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    subject = f"WI-{work_id}: {leaf} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{leaf}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _run(["git", "commit", "-q", "-m", body, "--", *paths], root)
    if commit.returncode == 0:
        print(f"Audit snapshot committed for WI-{work_id}: {leaf} → {next_action}", file=sys.stderr)
    else:
        print("Failed to commit audit snapshot (may be no changes)", file=sys.stderr)
    return 0


def main() -> int:
    work_id = sys.argv[1] if len(sys.argv) > 1 else None
    return snapshot(Path.cwd(), work_id)


if __name__ == "__main__":
    raise SystemExit(main())
