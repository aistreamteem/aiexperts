"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Loose notes merge immediately; shared tasks wait until every subtask reports.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _active_leaf(state_path: Path) -> str:
    if not state_path.is_file():
        return ""
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        return ""
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return ""
    leaf = active[-1]
    return leaf.strip() if isinstance(leaf, str) else ""


def _acquire_lock(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
        try:
            lock.mkdir()
            return True
        except FileExistsError:
            time.sleep(1)
    return False


def _release_lock(lock: Path) -> None:
    try:
        lock.rmdir()
    except OSError:
        pass


def _archive_note(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _append(journal: Path, text: str) -> None:
    with journal.open("a", encoding="utf-8") as fh:
        fh.write(text)


def _status_failed(note_text: str) -> bool:
    status = field(note_text, "Status").lower()
    if "fail" in status:
        return True
    for line in note_text.splitlines():
        if line.lower().startswith("**status:**") and "fail" in line.lower():
            return True
    return False


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    raw = deadline.strip()
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        due = datetime.fromisoformat(raw)
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > due
    except ValueError:
        return False


def _merge_loose(notes_dir: Path, journal: Path, archive: Path) -> bool:
    loose = [
        p
        for p in notes_dir.glob("*.md")
        if p.is_file() and p.name.lower() != "readme.md"
    ]
    if not loose:
        return False
    ts = _now()
    _append(
        journal,
        f"\n## Background Agent Notes (merged {ts})\n\n"
        "Consolidated from background agents. Fold into the proper journal "
        "sections via journal-keeper.\n\n",
    )
    for note in sorted(loose):
        body = read_text(note)
        _append(journal, f"### {note.stem}\n\n{body.rstrip()}\n\n")
        _archive_note(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def _merge_shared_tasks(
    notes_dir: Path, journal: Path, archive: Path, session_dir: Path
) -> bool:
    tasks = notes_dir / "tasks"
    if not tasks.is_dir():
        return False
    did = False
    for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
        if (task_dir / ".merged").is_file():
            continue
        manifest_path = task_dir / "manifest.json"
        if not manifest_path.is_file():
            _log(f"task {task_dir.name} has no manifest - skip")
            continue
        try:
            manifest = json.loads(read_text(manifest_path) or "{}")
        except json.JSONDecodeError:
            _log(f"task {task_dir.name} has invalid manifest - skip")
            continue
        task_name = str(manifest.get("task") or "unnamed task")
        deadline = str(manifest.get("deadline") or "")
        subtasks = manifest.get("subtasks") or []
        if not isinstance(subtasks, list):
            continue
        total = 0
        present = 0
        failed = 0
        missing_list: list[str] = []
        failed_list: list[str] = []
        for st in subtasks:
            if not isinstance(st, str) or not st.strip():
                continue
            total += 1
            note = task_dir / f"{st}.md"
            if note.is_file():
                present += 1
                if _status_failed(read_text(note)):
                    failed += 1
                    failed_list.append(st)
            else:
                missing_list.append(st)
        ts = _now()
        if present < total:
            if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
                _append(
                    journal,
                    f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                    f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                    f"Never reported (no success or failure note): "
                    f"{' '.join(missing_list) or 'none'}\n\n"
                    "**Blockers:** operator action needed - a subtask agent appears "
                    "to have died without reporting. Re-dispatch the missing "
                    "subtask(s) or investigate.\n",
                )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing_list)}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}'")
                did = True
            else:
                _log(f"task '{task_name}' not terminal ({present}/{total} reported) - waiting")
            continue
        if failed:
            header = (
                f"## △ Background Task PARTIAL: {task_name} - {failed} of {total} "
                f"subtask(s) FAILED (merged {ts})"
            )
            status_note = (
                f"{failed} subtask(s) failed after their retry budget: "
                f"**{' '.join(failed_list)}**. Successful work below is still captured. "
                "**Blockers:** operator must review the failed subtask(s) and decide "
                "to re-dispatch or accept. See NEEDS-ATTENTION.md."
            )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED "
                f"({' '.join(failed_list)})\n",
                encoding="utf-8",
            )
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status_note = (
                f"All {total} subtasks succeeded. Fold into the proper journal "
                "sections (Artifacts, Resolved Q&A, Next action) via journal-keeper."
            )
        _append(journal, f"\n{header}\n\n{status_note}\n\n")
        task_archive = archive / task_dir.name
        task_archive.mkdir(parents=True, exist_ok=True)
        for st in subtasks:
            if not isinstance(st, str) or not st.strip():
                continue
            note = task_dir / f"{st}.md"
            if note.is_file():
                body = read_text(note)
                _append(journal, f"### subtask: {st}\n\n{body.rstrip()}\n\n")
                _archive_note(note, task_archive)
        try:
            shutil.copy2(manifest_path, task_archive / "manifest.json")
        except OSError:
            pass
        (task_dir / ".merged").write_text("", encoding="utf-8")
        _log(f"merged shared task '{task_name}' into {journal}")
        did = True
    return did


def process_work_item(root: Path, work_id: str) -> bool:
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    leaf = _active_leaf(state_path)
    if not leaf:
        _log(f"no active leaf for {work_id} - skip")
        return False
    journal = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf for {work_id} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    try:
        archive = notes_dir / "merged"
        session_dir = root / "work-items" / work_id
        did = False
        did = _merge_shared_tasks(notes_dir, journal, archive, session_dir) or did
        did = _merge_loose(notes_dir, journal, archive) or did
        return did
    finally:
        _release_lock(lock)


def discover_work_ids(root: Path) -> list[str]:
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[str] = []
    for path in base.iterdir():
        if not path.is_dir() or path.name.startswith("_"):
            continue
        if (path / "agent-notes").is_dir():
            found.append(path.name)
    return sorted(set(found))


def merge_all(root: Path | None = None) -> list[str]:
    root = root or Path.cwd()
    merged: list[str] = []
    for work_id in discover_work_ids(root):
        if process_work_item(root, work_id):
            merged.append(work_id)
    return merged


def main() -> int:
    merge_all(Path.cwd())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
