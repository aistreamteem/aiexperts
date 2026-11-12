"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/. Merged notes move to
merged/. Shared tasks wait until every subtask has a note. Always exits 0.
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text

ROOT = Path(__file__).resolve().parents[2]
STATUS_FAIL = re.compile(r"(?im)^\s*\*{0,2}status\*{0,2}\s*:\s*.*fail")


def _log(message: str) -> None:
    print(f"[merge-agent-notes] {message}", flush=True)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _active_leaf(work_id: str) -> Path | None:
    state_path = ROOT / "journals" / "work-items" / work_id / "state.json"
    if not state_path.is_file():
        return None
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return None
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return None
    leaf = active[-1]
    if not isinstance(leaf, str) or not leaf.strip():
        return None
    if "/" in leaf or "\\" in leaf or ".." in leaf:
        return None
    note = ROOT / "journals" / "work-items" / work_id / "nodes" / f"{leaf.strip()}.md"
    return note if note.is_file() else None


def _append(path: Path, text: str) -> None:
    existing = read_text(path)
    path.write_text(existing.rstrip() + "\n" + text + "\n", encoding="utf-8")


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    note.replace(dest)


def _merge_note(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note).rstrip()
    block = f"\n### {heading}\n\n{body}\n"
    _append(journal, block)
    _archive(note, archive)


def _acquire(lock: Path) -> bool:
    for _ in range(10):
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


def _needs_attention(work_id: str, message: str) -> None:
    path = ROOT / "work-items" / work_id / "NEEDS-ATTENTION.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(message.rstrip() + "\n", encoding="utf-8")


def _process_shared(task_dir: Path, journal: Path, archive: Path, work_id: str, ts: str) -> bool:
    if (task_dir / ".merged").is_file():
        return False
    manifest_path = task_dir / "manifest.json"
    if not manifest_path.is_file():
        _log(f"task {task_dir.name} has no manifest - skip")
        return False
    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError:
        _log(f"task {task_dir.name} has bad manifest - skip")
        return False
    subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else None
    if not isinstance(subtasks, list) or not subtasks:
        return False
    task_name = str(manifest.get("task") or "unnamed task")
    deadline = str(manifest.get("deadline") or "").strip()
    missing: list[str] = []
    failed: list[str] = []
    present = 0
    for raw in subtasks:
        name = str(raw).strip()
        if not name:
            continue
        note = task_dir / f"{name}.md"
        if note.is_file():
            present += 1
            if STATUS_FAIL.search(read_text(note)):
                failed.append(name)
        else:
            missing.append(name)
    total = len([str(s).strip() for s in subtasks if str(s).strip()])
    if present < total:
        if deadline and not (task_dir / ".stall-warned").is_file():
            try:
                dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                if datetime.now(timezone.utc) > dl.astimezone(timezone.utc):
                    block = (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported: {', '.join(missing) or 'none'}\n"
                    )
                    _append(journal, block)
                    _needs_attention(
                        work_id,
                        f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}",
                    )
                    (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                    _log(f"escalated STALLED task '{task_name}'")
                    return True
            except ValueError:
                pass
        _log(f"task '{task_name}' not terminal ({present}/{total}) - waiting")
        return False
    if failed:
        header = (
            f"## △ Background Task PARTIAL: {task_name} - "
            f"{len(failed)} of {total} subtask(s) FAILED (merged {ts})"
        )
        status = (
            f"{len(failed)} subtask(s) failed: **{' '.join(failed)}**. "
            "See NEEDS-ATTENTION.md."
        )
        _needs_attention(
            work_id,
            f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{total} FAILED ({' '.join(failed)})",
        )
    else:
        header = f"## Background Task Complete: {task_name} (merged {ts})"
        status = f"All {total} subtasks succeeded. Fold via journal-keeper."
    _append(journal, f"\n{header}\n\n{status}\n")
    task_archive = archive / task_dir.name
    for raw in subtasks:
        name = str(raw).strip()
        note = task_dir / f"{name}.md"
        if note.is_file():
            _merge_note(note, journal, task_archive, f"subtask: {name}")
    try:
        (task_archive / "manifest.json").write_text(
            manifest_path.read_text(encoding="utf-8"), encoding="utf-8"
        )
    except OSError:
        pass
    (task_dir / ".merged").write_text("", encoding="utf-8")
    _log(f"merged shared task '{task_name}' into {journal}")
    return True


def process_work_item(work_id: str) -> bool:
    notes_dir = ROOT / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        return False
    journal = _active_leaf(work_id)
    if journal is None:
        _log(f"no active leaf for {work_id} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire(lock):
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    did_merge = False
    try:
        ts = _now()
        archive = notes_dir / "merged"
        tasks = notes_dir / "tasks"
        if tasks.is_dir():
            for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
                if _process_shared(task_dir, journal, archive, work_id, ts):
                    did_merge = True
        loose = [
            p
            for p in notes_dir.glob("*.md")
            if p.is_file() and p.name.lower() != "readme.md"
        ]
        if loose:
            _append(
                journal,
                f"\n## Background Agent Notes (merged {ts})\n\n"
                "Consolidated from background agents. Fold via journal-keeper.\n",
            )
            for note in loose:
                _merge_note(note, journal, archive, note.stem)
            _log(f"merged loose notes into {journal}")
            did_merge = True
    finally:
        _release(lock)
    return did_merge


def discover_work_ids() -> list[str]:
    found: set[str] = set()
    base = ROOT / "journals" / "work-items"
    if base.is_dir():
        for notes in base.glob("*/agent-notes"):
            wid = notes.parent.name
            if wid.upper() == "_TEMPLATE":
                continue
            found.add(wid)
    # Legacy location during transition
    legacy = ROOT / "work-items"
    if legacy.is_dir():
        for notes in legacy.glob("*/journal/agent-notes"):
            wid = notes.parent.parent.name
            if wid.startswith("_"):
                continue
            found.add(wid)
    return sorted(found)


def main() -> int:
    from journal_snapshot import snapshot_work_item

    for work_id in discover_work_ids():
        if process_work_item(work_id):
            snapshot_work_item(work_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
