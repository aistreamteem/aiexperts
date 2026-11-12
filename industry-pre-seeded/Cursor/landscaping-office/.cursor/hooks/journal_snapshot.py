"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text


def _run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    return _run(root, ["git", "rev-parse", "--is-inside-work-tree"]).returncode == 0


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    return _run(root, ["git", "check-ignore", "-q", rel]).returncode == 0


def _active_phase(state_path: Path) -> str:
    try:
        state = json.loads(read_text(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else []
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            return leaf.strip()
    return "unknown"


def snapshot_work_item(root: Path, work_id: str) -> None:
    if not work_id or not _inside_git(root):
        return
    journal_base = root / "journals" / "work-items" / work_id
    if not journal_base.is_dir():
        return
    session_dir = root / "work-items" / work_id
    status_path = session_dir / "STATUS.md"
    needs = session_dir / "NEEDS-ATTENTION.md"
    expert = root / "journals" / "expert" / "progress.md"
    leaf = _active_phase(journal_base / "state.json")
    node = journal_base / "nodes" / f"{leaf}.md"
    next_action = field(read_text(node), "Next action") if node.is_file() else ""
    phase = leaf or "unknown"
    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    paths.append(journal_base)
    if status_path.is_file():
        paths.append(status_path)
    if needs.is_file():
        paths.append(needs)
    # Skip commit when the journal tree is gitignored
    if _ignored(root, journal_base / "progress.md"):
        return
    rels: list[str] = []
    for path in paths:
        try:
            rels.append(str(path.relative_to(root)).replace("\\", "/"))
        except ValueError:
            continue
    if not rels:
        return
    _run(root, ["git", "add", "--", *rels])
    diff = _run(root, ["git", "diff", "--cached", "--quiet", "--", *rels])
    if diff.returncode == 0:
        return
    tag = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{work_id}: {phase} → {next_action or 'unknown'}{tag}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action or 'unknown'}\n"
        f"Timestamp: {ts}\n"
    )
    _run(root, ["git", "commit", "-q", "-m", body, "--", *rels])


def main() -> int:
    root = Path.cwd()
    work_id = active_work_id(root)
    if work_id:
        snapshot_work_item(root, work_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
