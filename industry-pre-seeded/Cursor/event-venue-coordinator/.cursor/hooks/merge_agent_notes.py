"""Merge background-agent notes into the active journal leaf node."""

from __future__ import annotations

import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text


def _log(message: str) -> None:
    print(f"[merge-agent-notes] {message}", flush=True)


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _active_leaf(root: Path, work_id: str) -> tuple[Path, str] | tuple[None, str]:
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    if not state_path.is_file():
        return None, ""
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return None, ""
    active = state.get("active") if isinstance(state, dict) else []
    if not isinstance(active, list) or not active:
        return None, ""
    leaf = active[-1]
    if not isinstance(leaf, str) or not leaf.strip():
        return None, ""
    if "/" in leaf or "\\" in leaf or ".." in leaf:
        return None, ""
    note = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf.strip()}.md"
    if not note.is_file():
        return None, leaf.strip()
    return note, leaf.strip()


def _append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _archive_note(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    target = archive / note.name
    if target.exists():
        target = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(target))


def _status_failed(note: Path) -> bool:
    for line in read_text(note).splitlines():
        lower = line.lower()
        if lower.startswith("**status:**") and "fail" in lower:
            return True
        if lower.startswith("status:") and "fail" in lower:
            return True
    return False


def _acquire_lock(lock: Path, attempts: int = 10) -> bool:
    for _ in range(attempts):
        try:
            lock.mkdir(parents=False)
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


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    raw = deadline.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        when = datetime.fromisoformat(raw)
    except ValueError:
        return False
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) > when.astimezone(timezone.utc)


def _merge_loose(notes_dir: Path, journal: Path, archive: Path, ts: str) -> bool:
    loose = sorted(
        path
        for path in notes_dir.glob("*.md")
        if path.is_file() and path.name.lower() != "readme.md"
    )
    if not loose:
        return False
    _append(
        journal,
        f"\n## Background Agent Notes (merged {ts})\n\n"
        "Consolidated from background agents. Fold into the proper journal "
        "sections via journal-keeper.\n\n",
    )
    for note in loose:
        _append(journal, f"### {note.stem}\n\n{read_text(note).rstrip()}\n\n")
        _archive_note(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def _merge_shared_tasks(
    notes_dir: Path,
    journal: Path,
    archive: Path,
    session_dir: Path,
    ts: str,
) -> bool:
    tasks_dir = notes_dir / "tasks"
    if not tasks_dir.is_dir():
        return False
    did_merge = False
    for task_dir in sorted(path for path in tasks_dir.iterdir() if path.is_dir()):
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
        subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else []
        if not isinstance(subtasks, list):
            subtasks = []
        names = [str(item).strip() for item in subtasks if str(item).strip()]
        total = len(names)
        present = 0
        failed = 0
        missing: list[str] = []
        failed_list: list[str] = []
        for name in names:
            note = task_dir / f"{name}.md"
            if note.is_file():
                present += 1
                if _status_failed(note):
                    failed += 1
                    failed_list.append(name)
            else:
                missing.append(name)
        if present < total:
            if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
                _append(
                    journal,
                    f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                    f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                    f"Never reported (no success or failure note): "
                    f"{' '.join(missing) if missing else 'none'}\n\n"
                    "**Blockers:** operator action needed - a subtask agent appears to "
                    "have died without reporting. Re-dispatch the missing subtask(s) "
                    "or investigate.\n",
                )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}' (missing: {' '.join(missing)})")
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
        for name in names:
            note = task_dir / f"{name}.md"
            if note.is_file():
                _append(journal, f"### subtask: {name}\n\n{read_text(note).rstrip()}\n\n")
                _archive_note(note, task_archive)
        task_archive.mkdir(parents=True, exist_ok=True)
        shutil.copy2(manifest_path, task_archive / "manifest.json")
        (task_dir / ".merged").write_text("", encoding="utf-8")
        if failed:
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED "
                f"({' '.join(failed_list)})\n",
                encoding="utf-8",
            )
            _log(f"merged PARTIAL task '{task_name}' - {failed}/{total} failed")
        else:
            _log(f"merged shared task '{task_name}' into {journal}")
        did_merge = True
    return did_merge


def process_work_item(root: Path, work_id: str) -> bool:
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        return False
    journal, leaf = _active_leaf(root, work_id)
    if journal is None:
        _log(f"no branch map or active leaf for {work_id} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    try:
        ts = _now()
        archive = notes_dir / "merged"
        session_dir = root / "work-items" / work_id
        did = _merge_shared_tasks(notes_dir, journal, archive, session_dir, ts)
        did = _merge_loose(notes_dir, journal, archive, ts) or did
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
