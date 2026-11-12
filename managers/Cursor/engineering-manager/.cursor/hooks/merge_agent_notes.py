"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
The merge target is the active leaf node from state.json.
Always exits 0.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from journal_fields import active_leaf, read_text  # noqa: E402

ROOT = Path.cwd()
HOOKS = Path(__file__).resolve().parent


def _log(message: str) -> None:
    print(f"[merge-agent-notes] {message}")


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    target = archive / note.name
    try:
        note.replace(target)
    except OSError:
        shutil.move(str(note), str(target))


def _status_failed(note: Path) -> bool:
    return bool(re.search(r"(?im)^\*\*status:\*\*.*fail", read_text(note)))


def _acquire_lock(lock: Path, attempts: int = 10) -> bool:
    for _ in range(attempts):
        try:
            lock.mkdir()
            return True
        except FileExistsError:
            time.sleep(1)
        except OSError:
            return False
    return False


def _release_lock(lock: Path) -> None:
    try:
        lock.rmdir()
    except OSError:
        pass


def _parse_deadline(value: str):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _candidate_sessions() -> list[Path]:
    base = ROOT / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[Path] = []
    for notes_dir in base.glob("*/agent-notes"):
        session = notes_dir.parent
        if session.name.startswith("_"):
            continue
        found.append(session)
    return sorted({path.resolve() for path in found})


def _merge_note_file(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(journal, f"\n### {heading}\n\n{body}\n")
    _archive(note, archive)


def _process_shared_tasks(session: Path, journal: Path, notes_dir: Path, archive: Path) -> bool:
    tasks_dir = notes_dir / "tasks"
    if not tasks_dir.is_dir():
        return False
    did_merge = False
    ts = _now()
    for task_dir in sorted(p for p in tasks_dir.iterdir() if p.is_dir()):
        if (task_dir / ".merged").is_file():
            continue
        manifest_path = task_dir / "manifest.json"
        if not manifest_path.is_file():
            _log(f"task {task_dir.name} has no manifest - skip")
            continue
        try:
            manifest = json.loads(read_text(manifest_path))
        except json.JSONDecodeError:
            _log(f"task {task_dir.name} has invalid manifest - skip")
            continue
        task_name = str(manifest.get("task") or "unnamed task")
        deadline = str(manifest.get("deadline") or "")
        subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
        total = 0
        present = 0
        failed = 0
        missing: list[str] = []
        failed_list: list[str] = []
        for raw in subtasks:
            st = str(raw).strip()
            if not st:
                continue
            total += 1
            note = task_dir / f"{st}.md"
            if note.is_file():
                present += 1
                if _status_failed(note):
                    failed += 1
                    failed_list.append(st)
            else:
                missing.append(st)
        if present < total:
            deadline_ts = _parse_deadline(deadline)
            stalled = deadline_ts is not None and time.time() > deadline_ts
            warn_marker = task_dir / ".stall-warned"
            if stalled and not warn_marker.is_file():
                missing_text = " ".join(missing) if missing else "none"
                _append(
                    journal,
                    (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported (no success or failure note): {missing_text}\n\n"
                        "**Blockers:** operator action needed - a subtask agent appears to have "
                        "died without reporting. Re-dispatch the missing subtask(s) or investigate.\n"
                    ),
                )
                (session / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {missing_text}\n",
                    encoding="utf-8",
                )
                warn_marker.write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}' (missing: {missing_text})")
                did_merge = True
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
                "**Blockers:** operator must review the failed subtask(s) and decide to "
                "re-dispatch or accept. See NEEDS-ATTENTION.md."
            )
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status_note = (
                f"All {total} subtasks succeeded. Fold into the proper journal sections "
                "(Artifacts, Resolved Q&A, Next action) via journal-keeper."
            )
        _append(journal, f"\n{header}\n\n{status_note}\n")
        task_archive = archive / task_dir.name
        for raw in subtasks:
            st = str(raw).strip()
            if not st:
                continue
            note = task_dir / f"{st}.md"
            if note.is_file():
                _merge_note_file(note, journal, task_archive, f"subtask: {st}")
        if manifest_path.is_file():
            task_archive.mkdir(parents=True, exist_ok=True)
            shutil.copy2(manifest_path, task_archive / "manifest.json")
        (task_dir / ".merged").write_text("", encoding="utf-8")
        if failed:
            (session / "NEEDS-ATTENTION.md").write_text(
                f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED "
                f"({' '.join(failed_list)})\n",
                encoding="utf-8",
            )
            _log(f"merged PARTIAL task '{task_name}' - {failed}/{total} failed")
        else:
            _log(f"merged shared task '{task_name}' into {journal}")
        did_merge = True
    return did_merge


def _process_loose_notes(journal: Path, notes_dir: Path, archive: Path) -> bool:
    loose = [
        note
        for note in sorted(notes_dir.glob("*.md"))
        if note.name.lower() != "readme.md"
    ]
    if not loose:
        return False
    ts = _now()
    _append(
        journal,
        (
            f"\n## Background Agent Notes (merged {ts})\n\n"
            "Consolidated from background agents. Fold into the proper journal sections "
            "via journal-keeper.\n"
        ),
    )
    for note in loose:
        _merge_note_file(note, journal, archive, note.stem)
    _log(f"merged loose notes into {journal}")
    return True


def process_session(session: Path) -> bool:
    wid = session.name
    leaf = active_leaf(ROOT, wid)
    if not leaf:
        _log(f"no active leaf for {wid} - skip")
        return False
    journal = session / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf for {wid} - skip")
        return False
    notes_dir = session / "agent-notes"
    archive = notes_dir / "merged"
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {session} (another merge in progress) - skip")
        return False
    try:
        did_merge = False
        did_merge = _process_shared_tasks(session, journal, notes_dir, archive) or did_merge
        did_merge = _process_loose_notes(journal, notes_dir, archive) or did_merge
    finally:
        _release_lock(lock)
    if did_merge:
        from journal_snapshot import snapshot_work_item  # noqa: E402

        snapshot_work_item(ROOT, wid)
    return did_merge


def main() -> int:
    for session in _candidate_sessions():
        try:
            process_session(session)
        except Exception as exc:  # noqa: BLE001 - stop hooks must never fail the turn
            _log(f"error processing {session}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
