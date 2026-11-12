"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text


def _log(message: str) -> None:
    print(f"[journal-snapshot] {message}", file=sys.stderr)


def _run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    result = _run(root, ["git", "rev-parse", "--is-inside-work-tree"])
    return result.returncode == 0 and result.stdout.strip() == "true"


def _ensure_git(root: Path) -> bool:
    if _inside_git(root):
        return True
    _log("No enclosing Git repository - initializing one for audit log...")
    init = _run(root, ["git", "init", "-q"])
    if init.returncode != 0:
        _log("git init failed")
        return False
    _run(root, ["git", "config", "user.name", "Cursor Expert Agent"])
    _run(root, ["git", "config", "user.email", "expert@cursor.local"])
    ignore = root / ".gitignore"
    if not ignore.is_file():
        ignore.write_text(
            "\n".join(
                [
                    "__pycache__/",
                    "*.pyc",
                    "*.tmp",
                    "*.temp",
                    "*.log",
                    ".cursor/plans/",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    _run(root, ["git", "add", "."])
    _run(root, ["git", "commit", "-q", "-m", "Initial commit: Expert template baseline"])
    return True


def _phase_from_state(state_path: Path) -> str:
    if not state_path.is_file():
        return "unknown"
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else []
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            return leaf.strip()
    return "unknown"


def _ignored(root: Path, path: Path) -> bool:
    result = _run(root, ["git", "check-ignore", "-q", str(path)])
    return result.returncode == 0


def snapshot_work_item(root: Path, work_id: str) -> int:
    if not work_id:
        _log("Empty Work Item ID - skipping audit log")
        return 0
    if not _ensure_git(root):
        return 0

    journals = root / "journals" / "work-items" / work_id
    session = root / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = session / "STATUS.md"
    needs = session / "NEEDS-ATTENTION.md"
    leaf = _phase_from_state(journals / "state.json")
    leaf_note = journals / "nodes" / f"{leaf}.md"
    next_action = field(read_text(leaf_note), "Next action") if leaf_note.is_file() else "unknown"
    last_completed = (
        field(read_text(leaf_note), "Last completed") if leaf_note.is_file() else "none"
    )
    if not next_action:
        next_action = "unknown"
    if not last_completed:
        last_completed = "none"

    commit_paths: list[Path] = []
    if expert.is_file():
        commit_paths.append(expert)
    if journals.is_dir():
        commit_paths.append(journals)
    if status.is_file():
        commit_paths.append(status)
    if needs.is_file():
        commit_paths.append(needs)

    if not commit_paths:
        _log(f"No journal paths for {work_id} - skipping")
        return 0

    # If the journal tree is gitignored, merge stays on disk only.
    sample = journals / "progress.md"
    if sample.is_file() and _ignored(root, sample):
        _log(f"Session {work_id} is gitignored - merged on disk, skipping git commit")
        return 0

    rel_paths = [str(path.relative_to(root)).replace("\\", "/") for path in commit_paths]
    _run(root, ["git", "add", "--", *rel_paths])
    staged = _run(root, ["git", "diff", "--cached", "--quiet", "--", *rel_paths])
    if staged.returncode == 0:
        _log(f"No tracked journal changes to commit for {work_id}")
        return 0

    attention = ""
    if needs.is_file():
        attention = " [NEEDS-ATTENTION]"
    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    subject = f"WI-{work_id}: {leaf} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{leaf}\n"
        f"Completed: {last_completed}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _run(root, ["git", "commit", "-q", "-m", body, "--", *rel_paths])
    if commit.returncode == 0:
        _log(f"Audit snapshot committed for WI-{work_id}: {leaf} → {next_action}")
    else:
        _log("Failed to commit audit snapshot (may be no changes)")
    return 0


def main() -> int:
    root = Path.cwd()
    work_id = ""
    if len(sys.argv) > 1:
        arg = Path(sys.argv[1])
        work_id = arg.name if arg.name else str(sys.argv[1])
        if work_id.startswith("WID-") is False and arg.parts:
            # Accept work-items/<id> session dirs
            work_id = arg.name
    if not work_id:
        work_id = active_work_id(root)
    return snapshot_work_item(root, work_id)


if __name__ == "__main__":
    raise SystemExit(main())
