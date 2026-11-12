"""Audit snapshot: commit the journal paths of one work item, and nothing else.

Usage: py -3 .cursor/hooks/journal_snapshot.py [work-items/<id> | journals/work-items/<id> | <id>]

Only these paths are ever staged or committed:
  journals/expert/progress.md
  journals/work-items/<id>/            (whole directory)
  work-items/<id>/STATUS.md
  work-items/<id>/NEEDS-ATTENTION.md
Unrelated staged files are left alone. Never initialises git or changes git
config. Always exits 0.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from journal_fields import _field, _read, _safe_id, active_leaf, active_path, node_path, work_id  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def _log(message: str) -> None:
    print(f"[journal-snapshot] {message}", file=sys.stderr)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def resolve_work_id(root: Path, session: str | Path | None) -> str:
    if session:
        text = str(session).strip().replace("\\", "/").rstrip("/")
        if text:
            return _safe_id(text.rsplit("/", 1)[-1])
    return work_id(root)


def _commit_paths(root: Path, wid: str) -> list[str]:
    candidates = [
        root / "journals" / "expert" / "progress.md",
        root / "journals" / "work-items" / wid,
        root / "work-items" / wid / "STATUS.md",
        root / "work-items" / wid / "NEEDS-ATTENTION.md",
    ]
    return [path.relative_to(root).as_posix() for path in candidates if path.exists()]


def snapshot(session: str | Path | None = None, root: Path | None = None) -> bool:
    """Commit the audit snapshot. Returns True when a commit was made."""
    root = root or ROOT
    wid = resolve_work_id(root, session)
    if not wid:
        _log("no work item - skipping")
        return False
    progress = root / "journals" / "work-items" / wid / "progress.md"
    if not progress.is_file():
        _log(f"no journal for {wid} - skipping")
        return False
    try:
        if _git(root, "rev-parse", "--is-inside-work-tree").returncode != 0:
            _log("not inside a git work tree - skipping commit")
            return False
        rel_progress = progress.relative_to(root).as_posix()
        if _git(root, "check-ignore", "-q", rel_progress).returncode == 0:
            _log(f"journal for {wid} is gitignored - merged on disk, skipping commit")
            return False

        paths = _commit_paths(root, wid)
        add = _git(root, "add", "--", *paths)
        if add.returncode != 0:
            _log(f"git add failed: {add.stderr.strip()}")
            return False
        if _git(root, "diff", "--cached", "--quiet", "--", *paths).returncode == 0:
            _log(f"no journal changes to commit for {wid}")
            return False

        path = active_path(root, wid)
        leaf = path[-1] if path else ""
        phase = leaf or "unknown"
        next_action = _field(_read(node_path(root, wid, leaf)), "Next action") if leaf else ""
        next_action = next_action or "unknown"
        attention = (root / "work-items" / wid / "NEEDS-ATTENTION.md").is_file()
        subject = f"WI-{wid}: {phase} -> {next_action}" + (" [NEEDS-ATTENTION]" if attention else "")
        subject = " ".join(subject.split())
        if len(subject) > 120:
            subject = subject[:117] + "..."
        body = (
            f"Active path: {' -> '.join(path) if path else 'unknown'}\n"
            f"Next action: {next_action}\n"
            f"Timestamp: {datetime.now().astimezone().isoformat(timespec='seconds')}"
        )
        commit = _git(root, "commit", "-q", "-m", subject, "-m", body, "--", *paths)
        if commit.returncode != 0:
            _log(f"git commit failed: {(commit.stderr or commit.stdout).strip()}")
            return False
        _log(f"committed: {subject}")
        return True
    except (OSError, ValueError) as exc:
        _log(f"snapshot failed: {exc}")
        return False


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    try:
        snapshot(args[0] if args else None)
    except Exception as exc:  # never fail a hook
        _log(f"unexpected error: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
