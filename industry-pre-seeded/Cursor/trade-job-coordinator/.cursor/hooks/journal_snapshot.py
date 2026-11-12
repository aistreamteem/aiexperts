"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from journal_fields import active_leaf, active_work_id, field, read_text


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    result = _run(["git", "rev-parse", "--is-inside-work-tree"], root)
    return result.returncode == 0 and result.stdout.strip() == "true"


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    result = _run(["git", "check-ignore", "-q", rel], root)
    return result.returncode == 0


def snapshot(root: Path | None = None, work_id: str | None = None) -> int:
    root = root or Path.cwd()
    work_id = work_id or active_work_id(root)
    if not work_id:
        print("No active Work Item - skipping audit log")
        return 0
    if not _inside_git(root):
        print("No enclosing Git repository - skipping audit commit")
        return 0

    journals_wi = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    attention = root / "work-items" / work_id / "NEEDS-ATTENTION.md"
    flat = journals_wi / "progress.md"
    state_path = journals_wi / "state.json"
    try:
        state = json.loads(read_text(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        state = {}
    leaf = active_leaf(state)
    node = journals_wi / "nodes" / f"{leaf}.md" if leaf else None
    phase = leaf or "unknown"
    next_action = field(read_text(node), "Next action") if node and node.is_file() else "unknown"
    last_completed = (
        field(read_text(node), "Last completed") if node and node.is_file() else "none"
    )

    commit_paths: list[Path] = []
    if expert.is_file():
        commit_paths.append(expert)
    if journals_wi.is_dir():
        commit_paths.append(journals_wi)
    if status.is_file():
        commit_paths.append(status)
    if attention.is_file():
        commit_paths.append(attention)

    # If the whole journals tree is ignored, merge stays on disk only.
    sample = flat if flat.is_file() else expert
    if sample.is_file() and _ignored(root, sample):
        print(f"Session {work_id} is gitignored - skipping git commit (by design)")
        return 0

    rels = [p.as_posix() for p in commit_paths]
    if not rels:
        print(f"No journal paths for {work_id}")
        return 0

    _run(["git", "add", "--", *rels], root)
    staged = _run(["git", "diff", "--cached", "--quiet", "--", *rels], root)
    if staged.returncode == 0:
        print(f"No tracked journal changes to commit for {work_id}")
        return 0

    attention_tag = " [NEEDS-ATTENTION]" if attention.is_file() else ""
    subject = f"WI-{work_id}: {phase} → {next_action}{attention_tag}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Completed: {last_completed}\n"
        f"Next: {next_action}\n"
    )
    result = _run(["git", "commit", "-q", "-m", body, "--", *rels], root)
    if result.returncode == 0:
        print(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}")
    else:
        print("Failed to commit audit snapshot (may be no changes)")
    return 0


def main() -> int:
    return snapshot(Path.cwd())


if __name__ == "__main__":
    raise SystemExit(main())
