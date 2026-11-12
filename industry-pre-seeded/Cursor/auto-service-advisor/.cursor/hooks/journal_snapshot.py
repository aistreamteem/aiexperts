"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, field, read_text


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
    init = _git(root, "init", "-q")
    if init.returncode != 0:
        _log("git init failed")
        return False
    return True


def _ignored(root: Path, path: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    result = _git(root, "check-ignore", "-q", rel)
    return result.returncode == 0


def snapshot_work_item(root: Path, work_id: str) -> None:
    if not _ensure_repo(root):
        return

    journals_wi = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    needs = root / "work-items" / work_id / "NEEDS-ATTENTION.md"

    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    if journals_wi.is_dir():
        paths.append(journals_wi)
    if status.is_file():
        paths.append(status)
    if needs.is_file():
        paths.append(needs)

    # Skip commit when the journal tree is gitignored (merge stays on disk).
    if journals_wi.is_dir() and _ignored(root, journals_wi / "progress.md"):
        _log(f"{work_id} journal is gitignored - merged on disk, skip commit")
        return

    rels = []
    for path in paths:
        try:
            rels.append(path.relative_to(root).as_posix())
        except ValueError:
            continue
    if not rels:
        return

    add = _git(root, "add", "--", *rels)
    if add.returncode != 0:
        _log(f"git add failed: {add.stderr.strip()}")
        return

    diff = _git(root, "diff", "--cached", "--quiet", "--", *rels)
    if diff.returncode == 0:
        _log(f"No tracked journal changes to commit for {work_id}")
        return

    leaf, node = active_leaf(root, work_id)
    phase = leaf or "unknown"
    # Prefer phase from active path; next action from leaf node
    next_action = "unknown"
    last_completed = "none"
    if node is not None:
        body = read_text(node)
        next_action = field(body, "Next action") or "unknown"
        last_completed = field(body, "Last completed") or "none"

    attention = ""
    if needs.is_file():
        attention = " [NEEDS-ATTENTION]"

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    subject = f"WI-{work_id}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Completed: {last_completed}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _git(root, "commit", "-q", "-m", body, "--", *rels)
    if commit.returncode == 0:
        _log(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}")
    else:
        _log(f"Failed to commit audit snapshot: {commit.stderr.strip()}")


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    work_id = ""
    if len(sys.argv) > 1:
        work_id = sys.argv[1].strip()
    if not work_id:
        from journal_fields import active_work_id

        work_id = active_work_id(root)
    if not work_id:
        _log("No work item id - skip")
        return 0
    snapshot_work_item(root, work_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
