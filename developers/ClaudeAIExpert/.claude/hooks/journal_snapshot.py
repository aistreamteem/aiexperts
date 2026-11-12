"""Audit snapshot: commit the journal paths for one work item (stdlib only).

Usage: py -3 .claude/hooks/journal_snapshot.py [work-id]

Commits ONLY the journal paths (never anything else that is staged), skips the
commit when git ignores the journal or there is no repository, never runs
`git init` or `git config`, and always exits 0.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import journal_fields  # noqa: E402

_MAX_NEXT = 120


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _in_repo(root: Path) -> bool:
    try:
        return _git(root, "rev-parse", "--is-inside-work-tree").stdout.strip() == "true"
    except OSError:
        return False


def _ignored(root: Path, rel: str) -> bool:
    return _git(root, "check-ignore", "-q", "--", rel).returncode == 0


def candidate_paths(root: Path, work_id: str) -> list[str]:
    """Existing, non-ignored paths this snapshot is allowed to commit."""
    wanted = [
        "journals/expert/progress.md",
        f"journals/work-items/{work_id}",
        f"work-items/{work_id}/STATUS.md",
        f"work-items/{work_id}/NEEDS-ATTENTION.md",
    ]
    paths = []
    for rel in wanted:
        target = root / rel
        if not target.exists():
            continue
        probe = rel
        if target.is_dir():
            files = sorted(p for p in target.rglob("*") if p.is_file())
            if not files:
                continue
            probe = files[0].relative_to(root).as_posix()
        if _ignored(root, probe):
            continue
        paths.append(rel)
    return paths


def commit_subject(root: Path, work_id: str) -> str:
    path = journal_fields.active_path(root, work_id)
    phase = "/".join(path) or "unknown"
    leaf_text = ""
    if path:
        leaf_text = journal_fields.read(
            root / "journals" / "work-items" / work_id / "nodes" / f"{path[-1]}.md"
        )
    next_action = " ".join(journal_fields.field(leaf_text, "Next action").split()) or "unknown"
    if len(next_action) > _MAX_NEXT:
        next_action = next_action[: _MAX_NEXT - 3] + "..."
    tag = ""
    if (root / "work-items" / work_id / "NEEDS-ATTENTION.md").is_file():
        tag = " [NEEDS-ATTENTION]"
    return f"WI-{work_id}: {phase} \u2192 {next_action}{tag}"


def snapshot(root: Path, work_id: str | None = None) -> bool:
    """Commit the journal paths. Returns True when a commit was made."""
    root = Path(root)
    work_id = (work_id or journal_fields.active_work_id(root)).strip()
    if not work_id or not (root / "journals" / "work-items" / work_id).is_dir():
        return False
    if not _in_repo(root):
        return False
    paths = candidate_paths(root, work_id)
    if not paths:
        return False
    _git(root, "add", "--", *paths)
    if _git(root, "diff", "--cached", "--quiet", "--", *paths).returncode == 0:
        return False
    subject = commit_subject(root, work_id)
    body = f"Work item: {work_id}\nTimestamp: {datetime.now().astimezone().isoformat(timespec='seconds')}"
    result = _git(root, "commit", "-q", "-m", subject, "-m", body, "--", *paths)
    return result.returncode == 0


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(__file__).resolve().parents[2]
    work_id = args[0] if args else None
    try:
        snapshot(root, work_id)
    except Exception as exc:  # never fail a hook
        print(f"[journal_snapshot] {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
