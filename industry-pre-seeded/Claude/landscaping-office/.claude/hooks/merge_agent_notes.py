"""Merge background-agent notes into the active leaf journal node."""

from __future__ import annotations

import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, read_text


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", flush=True)


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


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


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def _archive_note(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest.unlink()
    shutil.move(str(note), str(dest))


def _merge_note_file(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(
        journal,
        f"\n### {heading}\n\n{body.rstrip()}\n\n",
    )
    _archive_note(note, archive)


def _status_failed(note: Path) -> bool:
    for line in read_text(note).splitlines():
        lower = line.lower().strip()
        if lower.startswith("**status:**") and "fail" in lower:
            return True
        if lower.startswith("status:") and "fail" in lower:
            return True
    return False


def _deadline_passed(deadline: str) -> bool:
    if not deadline:
        return False
    try:
        raw = deadline.strip().replace("Z", "+00:00")
        when = datetime.fromisoformat(raw)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > when.astimezone(timezone.utc)
    except ValueError:
        return False


def _process_shared_tasks(
    notes_dir: Path,
    journal: Path,
    archive: Path,
    attention: Path,
    ts: str,
) -> bool:
    tasks_dir = notes_dir / "tasks"
    if not tasks_dir.is_dir():
        return False
    did = False
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
        if not isinstance(manifest, dict):
            continue
        task_name = str(manifest.get("task") or "unnamed task")
        deadline = str(manifest.get("deadline") or "")
        subtasks = manifest.get("subtasks") or []
        if not isinstance(subtasks, list):
            continue
        names = [str(s).strip() for s in subtasks if str(s).strip()]
        total = len(names)
        present = 0
        failed = 0
        missing: list[str] = []
        failed_list: list[str] = []
        for name in names:
            nf = task_dir / f"{name}.md"
            if nf.is_file():
                present += 1
                if _status_failed(nf):
                    failed += 1
                    failed_list.append(name)
            else:
                missing.append(name)
        if present < total:
            if (
                _deadline_passed(deadline)
                and not (task_dir / ".stall-warned").is_file()
            ):
                _append(
                    journal,
                    (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported (no success or failure note): "
                        f"{' '.join(missing) if missing else 'none'}\n\n"
                        "**Blockers:** operator action needed - a subtask agent appears to "
                        "have died without reporting. Re-dispatch the missing subtask(s) "
                        "or investigate.\n"
                    ),
                )
                attention.write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}' (missing: {' '.join(missing)})")
                did = True
            else:
                _log(f"task '{task_name}' not terminal ({present}/{total} reported) - waiting")
            continue
        if failed:
            header = (
                f"## △ Background Task PARTIAL: {task_name} - "
                f"{failed} of {total} subtask(s) FAILED (merged {ts})"
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
        for name in names:
            _merge_note_file(task_dir / f"{name}.md", journal, task_archive, f"subtask: {name}")
        try:
            shutil.copy2(manifest_path, task_archive / "manifest.json")
        except OSError:
            pass
        (task_dir / ".merged").write_text("", encoding="utf-8")
        if failed:
            attention.write_text(
                f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED "
                f"({' '.join(failed_list)})\n",
                encoding="utf-8",
            )
            _log(f"merged PARTIAL task '{task_name}' - {failed}/{total} failed")
        else:
            _log(f"merged shared task '{task_name}' into {journal}")
        did = True
    return did


def _process_loose(notes_dir: Path, journal: Path, archive: Path, ts: str) -> bool:
    loose = []
    for note in sorted(notes_dir.glob("*.md")):
        if note.name.lower() == "readme.md":
            continue
        loose.append(note)
    if not loose:
        return False
    _append(
        journal,
        (
            f"\n## Background Agent Notes (merged {ts})\n\n"
            "Consolidated from background agents. Fold into the proper journal "
            "sections via journal-keeper.\n"
        ),
    )
    for note in loose:
        _merge_note_file(note, journal, archive, note.stem)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    try:
        state = json.loads(read_text(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        state = {}
    leaf = active_leaf(state)
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
        ts = _now()
        archive = notes_dir / "merged"
        attention = root / "work-items" / work_id / "NEEDS-ATTENTION.md"
        did = _process_shared_tasks(notes_dir, journal, archive, attention, ts)
        did = _process_loose(notes_dir, journal, archive, ts) or did
        return did
    finally:
        _release_lock(lock)


def discover_work_ids(root: Path) -> list[str]:
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[str] = []
    for path in base.iterdir():
        if not path.is_dir():
            continue
        if path.name.startswith("_"):
            continue
        notes = path / "agent-notes"
        if notes.is_dir():
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
