"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Merge target is the active leaf node from state.json. No jq.
Always exits 0.
"""

from __future__ import annotations

import json
import re
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text
from journal_snapshot import snapshot_work_item

STATUS_FAIL_RE = re.compile(r"^\*{0,2}status\*{0,2}\s*:\s*.*fail", re.I | re.M)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", flush=True)


def _active_leaf(state_path: Path) -> str:
    try:
        state = json.loads(read_text(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        return ""
    active = state.get("active") if isinstance(state, dict) else []
    if not isinstance(active, list) or not active:
        return ""
    leaf = active[-1]
    return leaf.strip() if isinstance(leaf, str) else ""


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


def _append_note(journal: Path, note: Path, heading: str) -> None:
    body = read_text(note)
    with journal.open("a", encoding="utf-8") as fh:
        fh.write(f"\n### {heading}\n\n")
        fh.write(body)
        if not body.endswith("\n"):
            fh.write("\n")
        fh.write("\n")


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    text = deadline.strip().replace("Z", "+00:00")
    try:
        due = datetime.fromisoformat(text)
    except ValueError:
        return False
    now = datetime.now(due.tzinfo or timezone.utc)
    return now > due


def _process_shared_tasks(
    notes_dir: Path,
    journal: Path,
    archive_root: Path,
    session_dir: Path,
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
        task_name = str(manifest.get("task") or "unnamed task")
        deadline = str(manifest.get("deadline") or "")
        subtasks = manifest.get("subtasks") or []
        if not isinstance(subtasks, list):
            continue
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
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                present += 1
                if STATUS_FAIL_RE.search(read_text(nf)):
                    failed += 1
                    failed_list.append(st)
            else:
                missing.append(st)
        if present < total:
            if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
                with journal.open("a", encoding="utf-8") as fh:
                    fh.write(
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported: {', '.join(missing) or 'none'}\n\n"
                        "**Blockers:** operator action needed — re-dispatch missing subtask(s).\n"
                    )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {', '.join(missing)}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}'")
                did = True
            else:
                _log(f"task '{task_name}' not terminal ({present}/{total}) - waiting")
            continue
        if failed:
            header = (
                f"## △ Background Task PARTIAL: {task_name} - "
                f"{failed} of {total} subtask(s) FAILED (merged {ts})"
            )
            status_note = (
                f"{failed} subtask(s) failed: **{' '.join(failed_list)}**. "
                "See NEEDS-ATTENTION.md."
            )
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status_note = (
                f"All {total} subtasks succeeded. Fold into journal sections via journal-keeper."
            )
        with journal.open("a", encoding="utf-8") as fh:
            fh.write(f"\n{header}\n\n{status_note}\n")
        task_archive = archive_root / task_dir.name
        for raw in subtasks:
            st = str(raw).strip()
            if not st:
                continue
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                _append_note(journal, nf, f"subtask: {st}")
                _archive(nf, task_archive)
        try:
            shutil.copy2(manifest_path, task_archive / "manifest.json")
        except OSError:
            pass
        (task_dir / ".merged").write_text("", encoding="utf-8")
        if failed:
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED "
                f"({' '.join(failed_list)})\n",
                encoding="utf-8",
            )
            _log(f"merged PARTIAL task '{task_name}'")
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
    with journal.open("a", encoding="utf-8") as fh:
        fh.write(f"\n## Background Agent Notes (merged {ts})\n\n")
        fh.write(
            "Consolidated from background agents. Fold into journal sections via journal-keeper.\n"
        )
    for note in loose:
        _append_note(journal, note, note.stem)
        _archive(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    if work_id in {"_TEMPLATE", "_template"}:
        return False
    journal_base = root / "journals" / "work-items" / work_id
    notes_dir = journal_base / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state_path = journal_base / "state.json"
    leaf = _active_leaf(state_path)
    if not leaf:
        _log(f"no active leaf for {work_id} - skip")
        return False
    journal = journal_base / "nodes" / f"{leaf}.md"
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
        session_dir = root / "work-items" / work_id
        did = _process_shared_tasks(notes_dir, journal, archive, session_dir, ts)
        did = _process_loose(notes_dir, journal, archive, ts) or did
        if did:
            snapshot_work_item(root, work_id)
        return did
    finally:
        _release_lock(lock)


def discover_work_ids(root: Path) -> list[str]:
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[str] = []
    for notes in base.glob("*/agent-notes"):
        if notes.is_dir():
            wid = notes.parent.name
            if wid not in {"_TEMPLATE", "_template"}:
                found.append(wid)
    return sorted(set(found))


def main() -> int:
    root = Path.cwd()
    for work_id in discover_work_ids(root):
        try:
            process_work_item(root, work_id)
        except Exception as exc:  # noqa: BLE001 — hooks must never fail the agent
            _log(f"error merging {work_id}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
