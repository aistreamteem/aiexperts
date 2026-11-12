"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/ (loose *.md or tasks/).
Merge target is the active leaf node from state.json. No jq required.
"""

from __future__ import annotations

import json
import re
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text

STATUS_FAIL = re.compile(r"(?i)^\s*\*{0,2}status\*{0,2}\s*:\s*.*fail")


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


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
    if not isinstance(leaf, str):
        return ""
    leaf = leaf.strip()
    if not leaf or "/" in leaf or "\\" in leaf or ".." in leaf:
        return ""
    return leaf


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


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _merge_note_body(note: Path, heading: str) -> str:
    body = read_text(note).rstrip()
    return f"\n### {heading}\n\n{body}\n\n"


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
        return False
    try:
        manifest = json.loads(read_text(manifest_path) or "{}")
    except json.JSONDecodeError:
        return False
    subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else None
    if not isinstance(subtasks, list) or not subtasks:
        return False
    names = [str(s).strip() for s in subtasks if str(s).strip()]
    task_name = str(manifest.get("task") or "unnamed task")
    deadline = str(manifest.get("deadline") or "").strip()

    present: list[str] = []
    missing: list[str] = []
    failed: list[str] = []
    for name in names:
        note = task_dir / f"{name}.md"
        if note.is_file():
            present.append(name)
            if STATUS_FAIL.search(read_text(note)):
                failed.append(name)
        else:
            missing.append(name)

    if missing:
        stalled = False
        if deadline:
            try:
                dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                stalled = datetime.now(timezone.utc) > dl.astimezone(timezone.utc)
            except ValueError:
                stalled = False
        if stalled and not (task_dir / ".stall-warned").is_file():
            _append(
                journal,
                (
                    f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                    f"Past deadline ({deadline}) with {len(present)}/{len(names)} "
                    f"subtasks reported.\n"
                    f"Never reported: {', '.join(missing) or 'none'}\n\n"
                    "**Blockers:** operator action needed — re-dispatch missing "
                    "subtask(s) or investigate.\n"
                ),
            )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"STALLED task '{task_name}' at {ts}: missing {', '.join(missing)}\n",
                encoding="utf-8",
            )
            (task_dir / ".stall-warned").write_text("", encoding="utf-8")
            return True
        return False

    if failed:
        header = (
            f"## △ Background Task PARTIAL: {task_name} - {len(failed)} of "
            f"{len(names)} subtask(s) FAILED (merged {ts})"
        )
        status = (
            f"{len(failed)} subtask(s) failed after their retry budget: "
            f"**{' '.join(failed)}**. Successful work below is still captured. "
            "**Blockers:** operator must review failed subtask(s)."
        )
        (session_dir / "NEEDS-ATTENTION.md").write_text(
            f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{len(names)} "
            f"FAILED ({' '.join(failed)})\n",
            encoding="utf-8",
        )
    else:
        header = f"## Background Task Complete: {task_name} (merged {ts})"
        status = (
            f"All {len(names)} subtasks succeeded. Fold into the proper journal "
            "sections via journal-keeper."
        )

    _append(journal, f"\n{header}\n\n{status}\n")
    archive = archive_root / task_dir.name
    for name in names:
        note = task_dir / f"{name}.md"
        if note.is_file():
            _append(journal, _merge_note_body(note, f"subtask: {name}"))
            _archive(note, archive)
    shutil.copy2(manifest_path, archive / "manifest.json")
    (task_dir / ".merged").write_text("", encoding="utf-8")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        # Also accept notes left under the work-item artifact tree (legacy).
        legacy = root / "work-items" / work_id / "journal" / "agent-notes"
        if legacy.is_dir():
            notes_dir = legacy
        else:
            return False

    state_path = root / "journals" / "work-items" / work_id / "state.json"
    leaf = _active_leaf(state_path)
    if not leaf:
        return False
    journal = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        return False

    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        return False
    did_merge = False
    try:
        ts = _now()
        archive = notes_dir / "merged"
        session_dir = root / "work-items" / work_id
        tasks_root = notes_dir / "tasks"
        if tasks_root.is_dir():
            for task_dir in sorted(p for p in tasks_root.iterdir() if p.is_dir()):
                if _process_shared_task(task_dir, journal, archive, session_dir, ts):
                    did_merge = True

        loose = [
            p
            for p in sorted(notes_dir.glob("*.md"))
            if p.name.lower() != "readme.md"
        ]
        if loose:
            _append(
                journal,
                (
                    f"\n## Background Agent Notes (merged {ts})\n\n"
                    "Consolidated from background agents. Fold into the proper "
                    "journal sections via journal-keeper.\n"
                ),
            )
            for note in loose:
                _append(journal, _merge_note_body(note, note.stem))
                _archive(note, archive)
            did_merge = True
    finally:
        _release_lock(lock)
    return did_merge


def discover_work_ids(root: Path) -> list[str]:
    found: set[str] = set()
    for pattern in (
        "journals/work-items/*/agent-notes",
        "work-items/*/journal/agent-notes",
    ):
        for notes in root.glob(pattern):
            if not notes.is_dir():
                continue
            wid = notes.parent.name if notes.parent.name != "journal" else notes.parent.parent.name
            if wid.startswith("_"):
                continue
            found.add(wid)
    return sorted(found)


def merge_all(root: Path) -> list[str]:
    merged: list[str] = []
    for wid in discover_work_ids(root):
        if process_work_item(root, wid):
            merged.append(wid)
    return merged


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    merge_all(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
