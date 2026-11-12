"""Commit the real journal paths for the audit trail."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from journal_fields import active_leaf, field, read_text  # noqa: E402


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    result = _run(["git", "rev-parse", "--is-inside-work-tree"], root)
    return result.returncode == 0 and result.stdout.strip() == "true"


def _ignored(root: Path, path: Path) -> bool:
    result = _run(["git", "check-ignore", "-q", str(path)], root)
    return result.returncode == 0


def snapshot_work_item(root: Path, work_id: str) -> None:
    if not work_id:
        print("No work item id - skipping audit log")
        return
    if not _inside_git(root):
        print("No enclosing Git repository - skipping audit log")
        return

    journals = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    attention = journals / "NEEDS-ATTENTION.md"
    if not attention.is_file():
        attention = root / "work-items" / work_id / "NEEDS-ATTENTION.md"

    leaf = active_leaf(root, work_id)
    leaf_note = journals / "nodes" / f"{leaf}.md" if leaf else None
    next_action = field(read_text(leaf_note), "Next action") if leaf_note else ""
    phase = leaf or "unknown"
    if not next_action:
        next_action = "unknown"

    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    if journals.is_dir():
        paths.append(journals)
    if status.is_file():
        paths.append(status)
    if attention.is_file():
        paths.append(attention)

    # Skip commit when the journal tree is gitignored; merge stays on disk.
    if journals.is_dir() and _ignored(root, journals / "progress.md"):
        print(f"Session {work_id} is gitignored - merged on disk, skipping git commit")
        return

    rel_paths = [str(path.relative_to(root)).replace("\\", "/") for path in paths]
    if not rel_paths:
        print(f"No journal paths for {work_id} - skipping audit log")
        return

    _run(["git", "add", "--", *rel_paths], root)
    diff = _run(["git", "diff", "--cached", "--quiet", "--", *rel_paths], root)
    if diff.returncode == 0:
        print(f"No tracked journal changes to commit for {work_id}")
        return

    attention_tag = " [NEEDS-ATTENTION]" if attention.is_file() else ""
    subject = f"WI-{work_id}: {phase} → {next_action}{attention_tag}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
    )
    commit = _run(["git", "commit", "-q", "-m", body, "--", *rel_paths], root)
    if commit.returncode == 0:
        print(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}")
    else:
        print("Failed to commit audit snapshot (may be no changes)")


def main() -> int:
    work_id = ""
    if len(sys.argv) > 1:
        arg = Path(sys.argv[1])
        work_id = arg.name if arg.name else str(sys.argv[1])
    else:
        from journal_fields import active_work_id  # noqa: E402

        work_id = active_work_id(Path.cwd())
    snapshot_work_item(Path.cwd(), work_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
