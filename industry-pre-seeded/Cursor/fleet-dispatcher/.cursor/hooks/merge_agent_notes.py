"""Merge background-agent notes into the active journal leaf node."""

from __future__ import annotations

import json
import re
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, read_text

STATUS_FAIL = re.compile(r"^\s*\*{0,2}status\*{0,2}\s*:\s*.*fail", re.I | re.M)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _lock(notes_dir: Path) -> Path | None:
    lock = notes_dir / ".merge.lock"
    for _ in range(10):
        try:
            lock.mkdir()
            return lock
        except FileExistsError:
            time.sleep(1)
        except OSError:
            return None
    return None


def _unlock(lock: Path | None) -> None:
    if lock is None:
        return
    try:
        lock.rmdir()
    except OSError:
        pass


def _append_note(target: Path, heading: str, body: str) -> None:
    with target.open("a", encoding="utf-8") as fh:
        fh.write("\n")
        fh.write(f"### {heading}\n\n")
        fh.write(body.rstrip() + "\n\n")


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _parse_deadline(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _process_shared(task_dir: Path, journal: Path, archive_root: Path, session_dir: Path) -> bool:
    if (task_dir / ".merged").is_file():
        return False
    manifest_path = task_dir / "manifest.json"
    if not manifest_path.is_file():
        return False
    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError:
        return False
    subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else None
    if not isinstance(subtasks, list) or not subtasks:
        return False
    task_name = str(manifest.get("task") or "unnamed task")
    deadline = _parse_deadline(str(manifest.get("deadline") or ""))
    present = 0
    failed = 0
    missing: list[str] = []
    failed_list: list[str] = []
    for st in subtasks:
        name = str(st).strip()
        if not name:
            continue
        nf = task_dir / f"{name}.md"
        if nf.is_file():
            present += 1
            body = read_text(nf)
            if STATUS_FAIL.search(body):
                failed += 1
                failed_list.append(name)
        else:
            missing.append(name)
    total = len([str(s).strip() for s in subtasks if str(s).strip()])
    ts = _now()
    if present < total:
        if (
            deadline is not None
            and time.time() > deadline
            and not (task_dir / ".stall-warned").is_file()
        ):
            with journal.open("a", encoding="utf-8") as fh:
                fh.write(
                    f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                    f"Past deadline ({manifest.get('deadline')}) with {present}/{total} "
                    f"subtasks reported.\n"
                    f"Never reported: {', '.join(missing) or 'none'}\n\n"
                    "**Blockers:** operator action needed.\n"
                )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"STALLED task '{task_name}' at {ts}: missing {', '.join(missing)}\n",
                encoding="utf-8",
            )
            (task_dir / ".stall-warned").write_text("", encoding="utf-8")
            return True
        return False
    archive = archive_root / task_dir.name
    if failed:
        header = (
            f"## △ Background Task PARTIAL: {task_name} - {failed} of {total} "
            f"subtask(s) FAILED (merged {ts})"
        )
        status_note = (
            f"{failed} subtask(s) failed: **{' '.join(failed_list)}**. "
            "See NEEDS-ATTENTION.md."
        )
        (session_dir / "NEEDS-ATTENTION.md").write_text(
            f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED "
            f"({', '.join(failed_list)})\n",
            encoding="utf-8",
        )
    else:
        header = f"## Background Task Complete: {task_name} (merged {ts})"
        status_note = (
            f"All {total} subtasks succeeded. Fold into journal sections via journal-keeper."
        )
    with journal.open("a", encoding="utf-8") as fh:
        fh.write(f"\n{header}\n\n{status_note}\n")
    for st in subtasks:
        name = str(st).strip()
        if not name:
            continue
        nf = task_dir / f"{name}.md"
        if nf.is_file():
            _append_note(journal, f"subtask: {name}", read_text(nf))
            _archive(nf, archive)
    try:
        shutil.copy2(manifest_path, archive / "manifest.json")
    except OSError:
        pass
    (task_dir / ".merged").write_text("", encoding="utf-8")
    return True


def _process_loose(notes_dir: Path, journal: Path, archive: Path) -> bool:
    loose = []
    for note in notes_dir.glob("*.md"):
        if note.name.lower() == "readme.md":
            continue
        loose.append(note)
    if not loose:
        return False
    ts = _now()
    with journal.open("a", encoding="utf-8") as fh:
        fh.write(
            f"\n## Background Agent Notes (merged {ts})\n\n"
            "Consolidated from background agents. Fold into journal sections "
            "via journal-keeper.\n"
        )
    for note in loose:
        _append_note(journal, note.stem, read_text(note))
        _archive(note, archive)
    return True


def process_work_item(root: Path, wid: str) -> bool:
    notes_dir = root / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        # Legacy location during transition
        legacy = root / "work-items" / wid / "journal" / "agent-notes"
        if legacy.is_dir():
            notes_dir = legacy
        else:
            return False
    leaf = active_leaf(root, wid)
    if not leaf:
        return False
    journal = root / "journals" / "work-items" / wid / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        return False
    lock = _lock(notes_dir)
    if lock is None:
        return False
    try:
        archive = notes_dir / "merged"
        session_dir = root / "work-items" / wid
        did = False
        tasks = notes_dir / "tasks"
        if tasks.is_dir():
            for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
                if _process_shared(task_dir, journal, archive, session_dir):
                    did = True
        if _process_loose(notes_dir, journal, archive):
            did = True
        return did
    finally:
        _unlock(lock)


def discover_work_ids(root: Path) -> list[str]:
    found: set[str] = set()
    modern = root / "journals" / "work-items"
    if modern.is_dir():
        for path in modern.glob("*/agent-notes"):
            wid = path.parent.name
            if wid.startswith("_"):
                continue
            found.add(wid)
    legacy = root / "work-items"
    if legacy.is_dir():
        for path in legacy.glob("*/journal/agent-notes"):
            wid = path.parent.parent.name
            if wid.startswith("_"):
                continue
            found.add(wid)
    return sorted(found)


def merge_all(root: Path | None = None) -> list[str]:
    root = root or Path.cwd()
    merged: list[str] = []
    for wid in discover_work_ids(root):
        if process_work_item(root, wid):
            merged.append(wid)
    return merged


def main() -> int:
    merge_all(Path.cwd())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
