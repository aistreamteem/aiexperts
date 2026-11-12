"""Audit-commit the real journal paths for a work item. Always exits 0."""

from __future__ import annotations

import json
import subprocess
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


def _git_ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    return _run(["git", "check-ignore", "-q", rel], root).returncode == 0


def _phase_from_state(root: Path, work_id: str) -> str:
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    if not state_path.is_file():
        return "unknown"
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else None
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            return leaf.strip()
    return "unknown"


def _next_action(root: Path, work_id: str, phase: str) -> str:
    node = root / "journals" / "work-items" / work_id / "nodes" / f"{phase}.md"
    if node.is_file():
        value = field(read_text(node), "Next action")
        if value:
            return value
    return "unknown"


def snapshot(root: Path, work_id: str | None = None) -> bool:
    work_id = (work_id or active_work_id(root) or "").strip()
    if not work_id:
        print("No active Work Item - skipping audit log")
        return False
    if not _inside_git(root):
        print("No enclosing Git repository - skipping audit commit")
        return False

    journal_root = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    needs = root / "work-items" / work_id / "NEEDS-ATTENTION.md"

    commit_paths: list[Path] = []
    if expert.is_file():
        commit_paths.append(expert)
    if journal_root.is_dir():
        commit_paths.append(journal_root)
    if status.is_file():
        commit_paths.append(status)
    if needs.is_file():
        commit_paths.append(needs)

    if not commit_paths:
        print(f"No journal paths for {work_id} - skipping audit log")
        return False

    # If the whole journal tree is ignored, merge stays on disk only.
    sample = journal_root / "progress.md"
    if sample.is_file() and _git_ignored(root, sample):
        print(f"Session {work_id} is gitignored - skipping git commit (by design)")
        return False

    phase = _phase_from_state(root, work_id)
    next_action = _next_action(root, work_id, phase)
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    subject = f"WI-{work_id}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )

    rels: list[str] = []
    for path in commit_paths:
        try:
            rels.append(str(path.relative_to(root)).replace("\\", "/"))
        except ValueError:
            continue
    if not rels:
        return False

    _run(["git", "add", "--", *rels], root)
    cached = _run(["git", "diff", "--cached", "--quiet", "--", *rels], root)
    if cached.returncode == 0:
        print(f"No tracked journal changes to commit for {work_id}")
        return False

    result = _run(["git", "commit", "-q", "-m", body, "--", *rels], root)
    if result.returncode == 0:
        print(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}")
        return True
    print("Failed to commit audit snapshot (may be no changes)")
    return False


def main() -> int:
    import sys

    root = Path.cwd()
    work_id = None
    if len(sys.argv) > 1:
        arg = Path(sys.argv[1])
        work_id = arg.name if arg.name else sys.argv[1]
        if str(arg).replace("\\", "/").startswith("work-items/"):
            work_id = arg.name
    snapshot(root, work_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
