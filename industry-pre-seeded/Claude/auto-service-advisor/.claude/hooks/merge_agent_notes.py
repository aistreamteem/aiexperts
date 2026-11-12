"""Merge background-agent notes into the active leaf node journal file.

Notes live under journals/work-items/<id>/agent-notes/.
Loose notes merge immediately; shared tasks merge when every subtask has a note.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, read_text

ROOT = Path(__file__).resolve().parents[2]


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")


def _status_failed(note_text: str) -> bool:
    for line in note_text.splitlines():
        low = line.lower().strip()
        if low.startswith("**status:**") or low.startswith("status:"):
            return "fail" in low
    return False


def _acquire_lock(lock: Path, attempts: int = 10) -> bool:
    for _ in range(attempts):
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


def _append_note(journal: Path, heading: str, body: str) -> None:
    with journal.open("a", encoding="utf-8") as fh:
        fh.write("\n")
        fh.write(f"### {heading}\n\n")
        fh.write(body.rstrip() + "\n\n")


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _candidate_ids(root: Path) -> list[str]:
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[str] = []
    for notes in base.glob("*/agent-notes"):
        if not notes.is_dir():
            continue
        wid = notes.parent.name
        if wid.startswith("_"):
            continue
        found.append(wid)
    return sorted(set(found))


def _process_shared_tasks(
    root: Path,
    work_id: str,
    notes_dir: Path,
    journal: Path,
    archive: Path,
    session_dir: Path,
) -> bool:
    tasks = notes_dir / "tasks"
    if not tasks.is_dir():
        return False
    did = False
    ts = _now()
    for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
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
            st = st.strip()
            total += 1
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                present += 1
                if _status_failed(read_text(nf)):
                    failed += 1
                    failed_list.append(st)
            else:
                missing_list.append(st)
        if present < total:
            deadline = str(manifest.get("deadline") or "").strip()
            stalled = False
            if deadline:
                try:
                    # Accept Z or offset ISO
                    dl = deadline.replace("Z", "+00:00")
                    dl_dt = datetime.fromisoformat(dl)
                    if dl_dt.tzinfo is None:
                        dl_dt = dl_dt.replace(tzinfo=timezone.utc)
                    stalled = datetime.now(timezone.utc) > dl_dt
                except ValueError:
                    stalled = False
            warn = task_dir / ".stall-warned"
            if stalled and not warn.is_file():
                with journal.open("a", encoding="utf-8") as fh:
                    fh.write("\n")
                    fh.write(f"## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n")
                    fh.write(
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                    )
                    fh.write(
                        f"Never reported (no success or failure note): "
                        f"{' '.join(missing_list) or 'none'}\n\n"
                    )
                    fh.write(
                        "**Blockers:** operator action needed - a subtask agent appears "
                        "to have died without reporting. Re-dispatch the missing "
                        "subtask(s) or investigate.\n"
                    )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing_list)}\n",
                    encoding="utf-8",
                )
                warn.write_text("", encoding="utf-8")
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
                "**Blockers:** operator must review the failed subtask(s)."
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
                "sections via journal-keeper."
            )
        with journal.open("a", encoding="utf-8") as fh:
            fh.write("\n")
            fh.write(header + "\n\n")
            fh.write(status_note + "\n")
        task_archive = archive / task_dir.name
        for st in subtasks:
            if not isinstance(st, str) or not st.strip():
                continue
            nf = task_dir / f"{st.strip()}.md"
            if nf.is_file():
                _append_note(journal, f"subtask: {st.strip()}", read_text(nf))
                _archive(nf, task_archive)
        try:
            shutil.copy2(manifest_path, task_archive / "manifest.json")
        except OSError:
            pass
        (task_dir / ".merged").write_text("", encoding="utf-8")
        _log(f"merged shared task '{task_name}' into {journal}")
        did = True
    return did


def _process_loose(
    notes_dir: Path, journal: Path, archive: Path
) -> bool:
    loose = []
    for note in sorted(notes_dir.glob("*.md")):
        if note.name.lower() == "readme.md":
            continue
        loose.append(note)
    if not loose:
        return False
    ts = _now()
    with journal.open("a", encoding="utf-8") as fh:
        fh.write("\n")
        fh.write(f"## Background Agent Notes (merged {ts})\n\n")
        fh.write(
            "Consolidated from background agents. Fold into the proper journal "
            "sections via journal-keeper.\n"
        )
    for note in loose:
        _append_note(journal, note.stem, read_text(note))
        _archive(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        return False
    leaf, journal = active_leaf(root, work_id)
    if not leaf or journal is None:
        _log(f"no active leaf for {work_id} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    try:
        archive = notes_dir / "merged"
        session_dir = root / "work-items" / work_id
        session_dir.mkdir(parents=True, exist_ok=True)
        did = _process_shared_tasks(
            root, work_id, notes_dir, journal, archive, session_dir
        )
        did = _process_loose(notes_dir, journal, archive) or did
        return did
    finally:
        _release_lock(lock)


def main() -> int:
    root = ROOT
    merged_any = False
    for work_id in _candidate_ids(root):
        if process_work_item(root, work_id):
            merged_any = True
            try:
                from journal_snapshot import snapshot_work_item

                snapshot_work_item(root, work_id)
            except Exception as exc:  # noqa: BLE001
                _log(f"journal snapshot failed for {work_id}: {exc}")
    return 0 if not merged_any or True else 0


if __name__ == "__main__":
    raise SystemExit(main())
