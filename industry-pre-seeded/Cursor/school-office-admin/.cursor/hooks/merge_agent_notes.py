"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Merge target is the active leaf node from state.json. No jq required.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import read_text  # noqa: E402
from journal_snapshot import snapshot_work_item  # noqa: E402

STATUS_FAIL = re.compile(r"^\*\*status:\*\*.*fail", re.IGNORECASE)


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def _merge_note_file(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(journal, f"\n### {heading}\n\n{body.rstrip()}\n\n")
    _archive(note, archive)


def _process_shared_task(
    task_dir: Path,
    journal: Path,
    archive_root: Path,
    session_dir: Path,
    ts: str,
) -> bool:
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
    deadline = str(manifest.get("deadline") or "").strip()
    subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
    total = 0
    present = 0
    failed = 0
    missing_list: list[str] = []
    failed_list: list[str] = []
    for st in subtasks:
        if not isinstance(st, str) or not st.strip():
            continue
        name = st.strip()
        total += 1
        note = task_dir / f"{name}.md"
        if note.is_file():
            present += 1
            if STATUS_FAIL.search(read_text(note)):
                failed += 1
                failed_list.append(name)
        else:
            missing_list.append(name)
    if present < total:
        stalled = False
        if deadline:
            try:
                # Accept trailing Z or naive ISO.
                dl = deadline.replace("Z", "+00:00")
                dl_dt = datetime.fromisoformat(dl)
                if dl_dt.tzinfo is None:
                    dl_dt = dl_dt.replace(tzinfo=timezone.utc)
                stalled = datetime.now(timezone.utc) > dl_dt
            except ValueError:
                stalled = False
        if stalled and not (task_dir / ".stall-warned").is_file():
            missing = " ".join(missing_list) or "none"
            _append(
                journal,
                f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                f"Never reported (no success or failure note): {missing}\n\n"
                "**Blockers:** operator action needed - a subtask agent appears to have "
                "died without reporting. Re-dispatch the missing subtask(s) or investigate.\n",
            )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"STALLED task '{task_name}' at {ts}: missing {missing}\n",
                encoding="utf-8",
            )
            (task_dir / ".stall-warned").write_text("", encoding="utf-8")
            _log(f"escalated STALLED task '{task_name}' (missing: {missing})")
            return True
        _log(f"task '{task_name}' not terminal ({present}/{total} reported) - waiting")
        return False

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
    for st in subtasks:
        if not isinstance(st, str) or not st.strip():
            continue
        note = task_dir / f"{st.strip()}.md"
        if note.is_file():
            _merge_note_file(note, journal, archive, f"subtask: {st.strip()}")
    if manifest_path.is_file():
        archive.mkdir(parents=True, exist_ok=True)
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
    return True


def process_work_item(root: Path, work_id: str) -> bool:
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
    if not _acquire(lock):
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    did_merge = False
    ts = _now()
    try:
        archive = notes_dir / "merged"
        tasks = notes_dir / "tasks"
        session_dir = root / "work-items" / work_id
        if tasks.is_dir():
            for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
                if _process_shared_task(task_dir, journal, archive, session_dir, ts):
                    did_merge = True
        loose = [
            p
            for p in notes_dir.glob("*.md")
            if p.name.lower() != "readme.md"
        ]
        if loose:
            _append(
                journal,
                f"\n## Background Agent Notes (merged {ts})\n\n"
                "Consolidated from background agents. Fold into the proper journal "
                "sections via journal-keeper.\n",
            )
            for note in loose:
                _merge_note_file(note, journal, archive, note.stem)
            _log(f"merged loose notes into {journal}")
            did_merge = True
    finally:
        _release(lock)
    if did_merge:
        snapshot_work_item(root, work_id)
    return did_merge


def discover_work_ids(root: Path) -> list[str]:
    found: set[str] = set()
    base = root / "journals" / "work-items"
    if base.is_dir():
        for notes in base.glob("*/agent-notes"):
            wid = notes.parent.name
            if wid.startswith("_"):
                continue
            found.add(wid)
    # Legacy discovery: work-items/<id>/journal/agent-notes
    legacy = root / "work-items"
    if legacy.is_dir():
        for notes in legacy.glob("*/journal/agent-notes"):
            wid = notes.parent.parent.name
            if wid.startswith("_"):
                continue
            found.add(wid)
    return sorted(found)


def main() -> int:
    root = Path.cwd()
    for work_id in discover_work_ids(root):
        process_work_item(root, work_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
