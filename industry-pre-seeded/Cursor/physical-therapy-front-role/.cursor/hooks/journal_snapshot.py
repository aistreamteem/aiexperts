"""Commit an audit snapshot of the real journal paths for one Work Item."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, field, read_text

ROOT = Path(__file__).resolve().parents[2]


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


def snapshot_work_item(root: Path, work_id: str) -> None:
    if not work_id or work_id.startswith("_"):
        return
    if not _inside_git(root):
        print("No enclosing Git repository - skipping audit commit", file=sys.stderr)
        return

    journals = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    needs = root / "work-items" / work_id / "NEEDS-ATTENTION.md"

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
        return

    # Skip commit when the journal tree is gitignored
    check = _run(root, ["git", "check-ignore", "-q", paths[0]])
    if check.returncode == 0:
        print(
            f"Work item {work_id} journal is gitignored - merged on disk, skip commit",
            file=sys.stderr,
        )
        return

    leaf = active_leaf(root, work_id)
    node_text = ""
    if leaf:
        node_text = read_text(journals / "nodes" / f"{leaf}.md")
    next_action = field(node_text, "Next action") or "unknown"
    phase = leaf or "unknown"
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{work_id}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )

    _run(root, ["git", "add", "--"] + paths)
    # Commit only these paths so unrelated staged files stay untouched
    result = _run(root, ["git", "commit", "-q", "-m", body, "--"] + paths)
    if result.returncode == 0:
        print(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}", file=sys.stderr)
    else:
        print(
            f"No tracked journal changes to commit for {work_id} (merge, if any, is on disk)",
            file=sys.stderr,
        )


def main() -> int:
    root = Path.cwd()
    if not (root / ".cursor").is_dir():
        root = ROOT
    wid = ""
    if len(sys.argv) > 1:
        arg = Path(sys.argv[1])
        wid = arg.name if arg.name else sys.argv[1]
    if not wid:
        from journal_fields import active_work_id

        wid = active_work_id(root)
    if wid:
        snapshot_work_item(root, wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
