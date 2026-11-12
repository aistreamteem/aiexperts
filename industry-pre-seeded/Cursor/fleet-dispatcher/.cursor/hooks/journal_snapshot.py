"""Commit an audit snapshot of the real journal paths for a work item."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, field, read_text, work_id


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


def _ignored(root: Path, path: Path) -> bool:
    rel = path.relative_to(root).as_posix() if path.is_absolute() else str(path)
    return _run(["git", "check-ignore", "-q", rel], root).returncode == 0


def snapshot(root: Path, wid: str | None = None) -> int:
    if not _inside_git(root):
        return 0
    wid = wid or work_id(root)
    if not wid:
        return 0
    journals = root / "journals" / "work-items" / wid
    if not journals.is_dir():
        return 0
    leaf = active_leaf(root, wid)
    leaf_path = journals / "nodes" / f"{leaf}.md" if leaf else None
    next_action = "unknown"
    last_completed = "none"
    if leaf_path and leaf_path.is_file():
        body = read_text(leaf_path)
        next_action = field(body, "Next action") or "unknown"
        last_completed = field(body, "Last completed") or "none"
    state_path = journals / "state.json"
    phase = leaf or "unknown"
    if state_path.is_file():
        try:
            state = json.loads(read_text(state_path))
            active = state.get("active") if isinstance(state, dict) else []
            if isinstance(active, list) and active:
                phase = str(active[-1])
        except json.JSONDecodeError:
            pass
    status = root / "work-items" / wid / "STATUS.md"
    needs = root / "work-items" / wid / "NEEDS-ATTENTION.md"
    expert = root / "journals" / "expert" / "progress.md"
    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    paths.append(journals)
    if status.is_file():
        paths.append(status)
    if needs.is_file():
        paths.append(needs)
    # Skip commit when the journals tree is gitignored
    if _ignored(root, journals / "progress.md"):
        return 0
    rels = []
    for path in paths:
        try:
            rels.append(path.relative_to(root).as_posix())
        except ValueError:
            rels.append(str(path))
    _run(["git", "add", "--", *rels], root)
    diff = _run(["git", "diff", "--cached", "--quiet", "--", *rels], root)
    if diff.returncode == 0:
        return 0
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{wid}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Completed: {last_completed}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    result = _run(["git", "commit", "-q", "-m", body, "--", *rels], root)
    return 0 if result.returncode == 0 else 0


def main() -> int:
    root = Path.cwd()
    wid = work_id(root)
    if wid:
        snapshot(root, wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
