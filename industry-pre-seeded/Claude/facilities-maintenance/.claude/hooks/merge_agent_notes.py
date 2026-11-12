"""Merge background-agent notes into the active leaf node journal file."""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, read_text, work_id

ROOT = Path.cwd()


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _status_failed(note_text: str) -> bool:
    for line in note_text.splitlines():
        low = line.lower().strip()
        if low.startswith("**status:**") and "fail" in low:
            return True
        if low.startswith("status:") and "fail" in low:
            return True
    return False


def _acquire(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
        try:
            lock.mkdir()
            return True
        except FileExistsError:
            time.sleep(1)
    return False


def _release(lock: Path) -> None:
    try:
        lock.rmdir()
    except OSError:
        pass


def _notes_dirs(root: Path) -> list[tuple[str, Path]]:
    """Return (work_item_id, agent-notes dir) under journals/work-items/*/agent-notes."""
    found: list[tuple[str, Path]] = []
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return found
    for notes in base.glob("*/agent-notes"):
        wid = notes.parent.name
        if wid.startswith("_"):
            continue
        found.append((wid, notes))
    return found


def _merge_one_note(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(
        journal,
        f"\n### {heading}\n\n{body.rstrip()}\n\n",
    )
    _archive(note, archive)


def _process_shared(task_dir: Path, journal: Path, archive_root: Path, session_root: Path) -> bool:
    if (task_dir / ".merged").is_file():
        return False
    manifest_path = task_dir / "manifest.json"
    if not manifest_path.is_file():
        _log(f"task {task_dir.name} has no manifest - skip")
        return False
    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError:
        _log(f"task {task_dir.name} bad manifest - skip")
        return False
    task_name = str(manifest.get("task") or "unnamed task")
    deadline = str(manifest.get("deadline") or "").strip()
    subtasks = manifest.get("subtasks") or []
    if not isinstance(subtasks, list):
        return False
    total = 0
    present = 0
    failed = 0
    missing: list[str] = []
    failed_list: list[str] = []
    for st in subtasks:
        if not isinstance(st, str) or not st.strip():
            continue
        total += 1
        nf = task_dir / f"{st.strip()}.md"
        if nf.is_file():
            present += 1
            if _status_failed(read_text(nf)):
                failed += 1
                failed_list.append(st.strip())
        else:
            missing.append(st.strip())
    ts = _now()
    if present < total:
        stalled = False
        if deadline:
            try:
                # Accept Z or offset ISO strings.
                dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                stalled = datetime.now(timezone.utc) > dl.astimezone(timezone.utc)
            except ValueError:
                stalled = False
        warn = task_dir / ".stall-warned"
        if stalled and not warn.is_file():
            _append(
                journal,
                f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                f"Never reported: {', '.join(missing) or 'none'}\n\n"
                "**Blockers:** operator action needed.\n",
            )
            (session_root / "NEEDS-ATTENTION.md").write_text(
                f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                encoding="utf-8",
            )
            warn.write_text("", encoding="utf-8")
            _log(f"escalated STALLED task '{task_name}'")
            return True
        _log(f"task '{task_name}' not terminal ({present}/{total}) - waiting")
        return False

    archive = archive_root / task_dir.name
    if failed:
        header = (
            f"## △ Background Task PARTIAL: {task_name} - "
            f"{failed} of {total} subtask(s) FAILED (merged {ts})"
        )
        status_note = (
            f"{failed} subtask(s) failed: **{' '.join(failed_list)}**. "
            "See NEEDS-ATTENTION.md."
        )
        (session_root / "NEEDS-ATTENTION.md").write_text(
            f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED ({' '.join(failed_list)})\n",
            encoding="utf-8",
        )
    else:
        header = f"## Background Task Complete: {task_name} (merged {ts})"
        status_note = f"All {total} subtasks succeeded. Fold via journal-keeper."
    _append(journal, f"\n{header}\n\n{status_note}\n")
    for st in subtasks:
        if not isinstance(st, str) or not st.strip():
            continue
        nf = task_dir / f"{st.strip()}.md"
        if nf.is_file():
            _merge_one_note(nf, journal, archive, f"subtask: {st.strip()}")
    try:
        shutil.copy2(manifest_path, archive / "manifest.json")
    except OSError:
        pass
    (task_dir / ".merged").write_text("", encoding="utf-8")
    _log(f"merged shared task '{task_name}' into {journal}")
    return True


def process_work_item(root: Path, wid: str, notes_dir: Path) -> bool:
    leaf = active_leaf(root, wid)
    if not leaf:
        _log(f"no active leaf for {wid} - skip")
        return False
    journal = root / "journals" / "work-items" / wid / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf for {wid} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire(lock):
        _log(f"could not acquire lock for {wid} - skip")
        return False
    did = False
    try:
        archive = notes_dir / "merged"
        session_root = root / "work-items" / wid
        tasks = notes_dir / "tasks"
        if tasks.is_dir():
            for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
                if _process_shared(task_dir, journal, archive, session_root):
                    did = True
        loose = []
        for note in sorted(notes_dir.glob("*.md")):
            if note.name.lower() == "readme.md":
                continue
            loose.append(note)
        if loose:
            ts = _now()
            _append(
                journal,
                f"\n## Background Agent Notes (merged {ts})\n\n"
                "Consolidated from background agents. Fold via journal-keeper.\n",
            )
            for note in loose:
                _merge_one_note(note, journal, archive, note.stem)
            _log(f"merged loose notes into {journal}")
            did = True
    finally:
        _release(lock)
    if did:
        try:
            from journal_snapshot import snapshot_work_item

            snapshot_work_item(root, wid)
        except Exception as exc:  # noqa: BLE001
            _log(f"journal snapshot failed for {wid}: {exc}")
    return did


def main() -> int:
    root = ROOT
    # Prefer notes under journals/; also accept an explicit work item from context.
    pairs = _notes_dirs(root)
    active = work_id(root)
    if active:
        notes = root / "journals" / "work-items" / active / "agent-notes"
        if notes.is_dir() and (active, notes) not in pairs:
            pairs.append((active, notes))
    for wid, notes_dir in pairs:
        process_work_item(root, wid, notes_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
