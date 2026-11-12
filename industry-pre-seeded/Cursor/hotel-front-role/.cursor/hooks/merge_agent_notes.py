"""Merge background-agent notes into the active leaf node journal.

Notes live under journals/work-items/<id>/agent-notes/.
Merge target is the active leaf in state.json (stdlib JSON; no jq).
Always exits 0.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import active_work_id, field, read_text  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _active_leaf(wid: str) -> Path | None:
    state_path = ROOT / "journals" / "work-items" / wid / "state.json"
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
    note = ROOT / "journals" / "work-items" / wid / "nodes" / f"{leaf.strip()}.md"
    return note if note.is_file() else None


def _append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _status_failed(note_text: str) -> bool:
    status = field(note_text, "Status").lower()
    return "fail" in status


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


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    try:
        # Accept Z or offset; fall back to naive compare via fromisoformat
        cleaned = deadline.replace("Z", "+00:00")
        dl = datetime.fromisoformat(cleaned)
        now = datetime.now(dl.tzinfo) if dl.tzinfo else datetime.now()
        return now > dl
    except ValueError:
        return False


def _process_shared(task_dir: Path, journal: Path, archive: Path, session_dir: Path, ts: str) -> bool:
    if (task_dir / ".merged").is_file():
        return False
    manifest_path = task_dir / "manifest.json"
    if not manifest_path.is_file():
        _log(f"task {task_dir.name} has no manifest - skip")
        return False
    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError:
        _log(f"task {task_dir.name} manifest invalid - skip")
        return False
    task_name = str(manifest.get("task") or "unnamed task")
    deadline = str(manifest.get("deadline") or "")
    subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
    total = 0
    present = 0
    failed = 0
    missing_list: list[str] = []
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
            missing_list.append(st.strip())
    if present < total:
        if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
            _append(
                journal,
                (
                    f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                    f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                    f"Never reported: {', '.join(missing_list) or 'none'}\n\n"
                    "**Blockers:** operator action needed — re-dispatch missing subtask(s).\n"
                ),
            )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"STALLED task '{task_name}' at {ts}: missing {', '.join(missing_list)}\n",
                encoding="utf-8",
            )
            (task_dir / ".stall-warned").write_text("", encoding="utf-8")
            _log(f"escalated STALLED task '{task_name}'")
            return True
        _log(f"task '{task_name}' not terminal ({present}/{total}) - waiting")
        return False
    if failed:
        header = (
            f"## △ Background Task PARTIAL: {task_name} - {failed} of {total} "
            f"subtask(s) FAILED (merged {ts})"
        )
        status_note = (
            f"{failed} subtask(s) failed: **{', '.join(failed_list)}**. "
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
    _append(journal, f"\n{header}\n\n{status_note}\n")
    task_archive = archive / task_dir.name
    for st in subtasks:
        if not isinstance(st, str) or not st.strip():
            continue
        nf = task_dir / f"{st.strip()}.md"
        if nf.is_file():
            _append(journal, f"\n### subtask: {st.strip()}\n\n{read_text(nf).rstrip()}\n\n")
            _archive(nf, task_archive)
    if manifest_path.is_file():
        task_archive.mkdir(parents=True, exist_ok=True)
        shutil.copy2(manifest_path, task_archive / "manifest.json")
    (task_dir / ".merged").write_text("", encoding="utf-8")
    _log(f"merged shared task '{task_name}' into {journal}")
    return True


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
            "Consolidated from background agents. Fold into journal sections via journal-keeper.\n"
        ),
    )
    for note in loose:
        _append(journal, f"\n### {note.stem}\n\n{read_text(note).rstrip()}\n\n")
        _archive(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(wid: str) -> bool:
    if wid in {"_TEMPLATE", "_template"}:
        return False
    notes_dir = ROOT / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        return False
    journal = _active_leaf(wid)
    if journal is None:
        _log(f"no branch map / active leaf for {wid} - skip")
        return False
    archive = notes_dir / "merged"
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {wid} - skip")
        return False
    did_merge = False
    try:
        ts = _now()
        session_dir = ROOT / "work-items" / wid
        tasks_dir = notes_dir / "tasks"
        if tasks_dir.is_dir():
            for task_dir in sorted(p for p in tasks_dir.iterdir() if p.is_dir()):
                if _process_shared(task_dir, journal, archive, session_dir, ts):
                    did_merge = True
        if _process_loose(notes_dir, journal, archive, ts):
            did_merge = True
    finally:
        _release_lock(lock)
    if did_merge:
        try:
            from journal_snapshot import snapshot_work_item

            snapshot_work_item(wid)
        except Exception as exc:  # noqa: BLE001 — never fail the stop hook
            _log(f"journal snapshot failed for {wid}: {exc}")
    return did_merge


def discover_work_ids() -> list[str]:
    base = ROOT / "journals" / "work-items"
    found: set[str] = set()
    if base.is_dir():
        for notes in base.glob("*/agent-notes"):
            if notes.is_dir():
                found.add(notes.parent.name)
    # Also accept legacy notes under work-items/<id>/journal/agent-notes
    legacy = ROOT / "work-items"
    if legacy.is_dir():
        for notes in legacy.glob("*/journal/agent-notes"):
            if notes.is_dir():
                found.add(notes.parent.parent.name)
    wid = active_work_id(ROOT)
    if wid:
        found.add(wid)
    return sorted(found)


def main() -> int:
    for wid in discover_work_ids():
        try:
            process_work_item(wid)
        except Exception as exc:  # noqa: BLE001
            _log(f"error processing {wid}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
