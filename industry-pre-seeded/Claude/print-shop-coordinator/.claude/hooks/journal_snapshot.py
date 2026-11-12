"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_phase, field, read_text, work_id


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


def snapshot_work_item(root: Path, wid: str) -> int:
    if not wid:
        print("No work item - skipping audit log", file=sys.stderr)
        return 0
    if not _inside_git(root):
        print("No enclosing Git repository - skipping audit commit", file=sys.stderr)
        return 0

    journals = root / "journals" / "work-items" / wid
    status = root / "work-items" / wid / "STATUS.md"
    needs = root / "work-items" / wid / "NEEDS-ATTENTION.md"
    expert = root / "journals" / "expert" / "progress.md"
    leaf_name = active_phase(root, wid)
    leaf = journals / "nodes" / f"{leaf_name}.md" if leaf_name else None
    leaf_text = read_text(leaf) if leaf and leaf.is_file() else ""
    next_action = field(leaf_text, "Next action") or "unknown"
    phase = leaf_name or "unknown"
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    paths: list[str] = []
    for path in (
        expert,
        journals,
        status,
        needs,
    ):
        if path is None:
            continue
        if path.exists():
            rel = path.relative_to(root).as_posix()
            paths.append(rel)

    # Skip commit when the journal tree is gitignored.
    sample = journals / "progress.md"
    if sample.is_file():
        ignored = _run(root, ["git", "check-ignore", "-q", str(sample)])
        if ignored.returncode == 0:
            print(
                f"Work item {wid} journal is gitignored - merged on disk, skip commit",
                file=sys.stderr,
            )
            return 0

    if not paths:
        return 0

    _run(root, ["git", "add", "--", *paths])
    staged = _run(root, ["git", "diff", "--cached", "--quiet", "--", *paths])
    if staged.returncode == 0:
        print(f"No tracked journal changes to commit for {wid}", file=sys.stderr)
        return 0

    msg = (
        f"WI-{wid}: {phase} → {next_action}{attention}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}"
    )
    commit = _run(root, ["git", "commit", "-q", "-m", msg, "--", *paths])
    if commit.returncode == 0:
        print(f"Audit snapshot committed for WI-{wid}: {phase} → {next_action}", file=sys.stderr)
    else:
        print("Failed to commit audit snapshot (may be no changes)", file=sys.stderr)
    return 0


def main() -> int:
    root = Path.cwd()
    wid = ""
    if len(sys.argv) > 1 and sys.argv[1].strip():
        arg = sys.argv[1].strip().replace("\\", "/")
        if arg.startswith("work-items/"):
            wid = Path(arg).name
        else:
            wid = Path(arg).name
    if not wid:
        wid = work_id(root)
    return snapshot_work_item(root, wid)


if __name__ == "__main__":
    raise SystemExit(main())
