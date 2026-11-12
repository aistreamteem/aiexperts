"""Merge background-agent notes into the active journal leaf node.

Notes live under journals/work-items/<id>/agent-notes/. Merge target is the
active leaf node from state.json. Always exits 0.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text
from journal_snapshot import snapshot_work_item


def _log(message: str) -> None:
    print(f"[merge-agent-notes] {message}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _active_leaf(state_path: Path) -> str:
    if not state_path.is_file():
        return ""
    try:
        state = json.loads(read_text(state_path))
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


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _archive_note(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


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
    try:
        raw = deadline.strip().replace("Z", "+00:00")
        due = datetime.fromisoformat(raw)
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > due.astimezone(timezone.utc)
    except ValueError:
        return False


def _merge_one_note(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(
        journal,
        f"\n### {heading}\n\n{body.rstrip()}\n\n",
    )
    _archive_note(note, archive)


def _process_shared_tasks(
    task_root: Path,
    journal: Path,
    archive_root: Path,
    session_dir: Path,
    ts: str,
) -> bool:
    did_merge = False
    if not task_root.is_dir():
        return False
    for task_dir in sorted(p for p in task_root.iterdir() if p.is_dir()):
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
        names = [str(st).strip() for st in subtasks if str(st).strip()]
        total = len(names)
        present = 0
        failed = 0
        missing: list[str] = []
        failed_list: list[str] = []
        for name in names:
            note = task_dir / f"{name}.md"
            if note.is_file():
                present += 1
                if _status_failed(read_text(note)):
                    failed += 1
                    failed_list.append(name)
            else:
                missing.append(name)
        if present < total:
            if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
                _append(
                    journal,
                    (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported (no success or failure note): "
                        f"{' '.join(missing) if missing else 'none'}\n\n"
                        "**Blockers:** operator action needed - a subtask agent appears to have "
                        "died without reporting. Re-dispatch the missing subtask(s) or investigate.\n"
                    ),
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
        archive = archive_root / task_dir.name
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
        for name in names:
            note = task_dir / f"{name}.md"
            if note.is_file():
                _merge_one_note(note, journal, archive, f"subtask: {name}")
        shutil.copy2(manifest_path, archive / "manifest.json")
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
    if work_id in {"_TEMPLATE", "_template"}:
        return False
    journals = root / "journals" / "work-items" / work_id
    session_dir = root / "work-items" / work_id
    notes_dir = journals / "agent-notes"
    if not notes_dir.is_dir():
        return False
    leaf = _active_leaf(journals / "state.json")
    if not leaf:
        _log(f"no branch map / active leaf for {work_id} - skip")
        return False
    journal = journals / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf for {work_id} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    did_merge = False
    ts = _now()
    try:
        archive = notes_dir / "merged"
        did_merge = _process_shared_tasks(
            notes_dir / "tasks", journal, archive, session_dir, ts
        ) or did_merge
        loose = [
            path
            for path in sorted(notes_dir.glob("*.md"))
            if path.name.lower() != "readme.md"
        ]
        if loose:
            _append(
                journal,
                (
                    f"\n## Background Agent Notes (merged {ts})\n\n"
                    "Consolidated from background agents. Fold into the proper journal "
                    "sections via journal-keeper.\n"
                ),
            )
            for note in loose:
                _merge_one_note(note, journal, archive, note.stem)
            _log(f"merged loose notes into {journal}")
            did_merge = True
    finally:
        _release_lock(lock)
    if did_merge:
        snapshot_work_item(root, work_id)
    return did_merge


def discover_work_ids(root: Path) -> list[str]:
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: set[str] = set()
    for notes in base.glob("*/agent-notes"):
        if notes.is_dir():
            found.add(notes.parent.name)
    # Also accept legacy notes under work-items/<id>/journal/agent-notes
    legacy = root / "work-items"
    if legacy.is_dir():
        for notes in legacy.glob("*/journal/agent-notes"):
            if notes.is_dir():
                found.add(notes.parent.parent.name)
    return sorted(wid for wid in found if wid not in {"_TEMPLATE", "_template"})


def main() -> int:
    root = Path.cwd()
    for work_id in discover_work_ids(root):
        try:
            process_work_item(root, work_id)
        except Exception as exc:  # noqa: BLE001 - hooks must never fail the agent
            _log(f"error processing {work_id}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
