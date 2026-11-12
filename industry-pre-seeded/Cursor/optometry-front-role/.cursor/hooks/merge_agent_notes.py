"""Merge background-agent notes into the active journal leaf node.

Notes live under journals/work-items/<id>/agent-notes/.
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

from journal_fields import field, read_text  # noqa: E402


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")


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
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _archive_note(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    try:
        shutil.move(str(note), str(dest))
    except OSError:
        pass


def _status_failed(note_text: str) -> bool:
    status = field(note_text, "Status").lower()
    return "fail" in status


def _parse_deadline(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        # Support trailing Z
        cleaned = raw.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned).timestamp()
    except ValueError:
        return None


def _merge_one(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(
        journal,
        f"\n### {heading}\n\n{body.rstrip()}\n\n",
    )
    _archive_note(note, archive)


def _process_shared_tasks(
    notes_dir: Path,
    journal: Path,
    session_dir: Path,
    ts: str,
) -> bool:
    tasks_root = notes_dir / "tasks"
    if not tasks_root.is_dir():
        return False
    did = False
    archive_root = notes_dir / "merged"
    for task_dir in sorted(p for p in tasks_root.iterdir() if p.is_dir()):
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
        subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else None
        if not isinstance(subtasks, list) or not subtasks:
            _log(f"task {task_dir.name} has no subtasks - skip")
            continue
        deadline = _parse_deadline(str(manifest.get("deadline") or ""))
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
                if _status_failed(read_text(nf)):
                    failed += 1
                    failed_list.append(st)
            else:
                missing.append(st)
        if present < total:
            stalled = False
            if deadline is not None and time.time() > deadline:
                stalled = True
            if stalled and not (task_dir / ".stall-warned").is_file():
                missing_txt = " ".join(missing) if missing else "none"
                _append(
                    journal,
                    (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({manifest.get('deadline')}) with "
                        f"{present}/{total} subtasks reported.\n"
                        f"Never reported (no success or failure note): {missing_txt}\n\n"
                        "**Blockers:** operator action needed - a subtask agent appears "
                        "to have died without reporting. Re-dispatch the missing "
                        "subtask(s) or investigate.\n"
                    ),
                )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {missing_txt}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}' (missing: {missing_txt})")
                did = True
            else:
                _log(
                    f"task '{task_name}' not terminal ({present}/{total} reported) - waiting"
                )
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
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status_note = (
                f"All {total} subtasks succeeded. Fold into the proper journal "
                "sections (Artifacts, Resolved Q&A, Next action) via journal-keeper."
            )
        _append(journal, f"\n{header}\n\n{status_note}\n")
        task_archive = archive_root / task_dir.name
        for raw in subtasks:
            st = str(raw).strip()
            if not st:
                continue
            note = task_dir / f"{st}.md"
            if note.is_file():
                _merge_one(note, journal, task_archive, f"subtask: {st}")
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
            _log(
                f"merged PARTIAL task '{task_name}' - {failed}/{total} failed "
                f"({' '.join(failed_list)})"
            )
        else:
            _log(f"merged shared task '{task_name}' into {journal}")
        did = True
    return did


def _process_loose(notes_dir: Path, journal: Path, ts: str) -> bool:
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
    archive = notes_dir / "merged"
    for note in loose:
        _merge_one(note, journal, archive, note.stem)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, wid: str) -> bool:
    notes_dir = root / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state_path = root / "journals" / "work-items" / wid / "state.json"
    leaf = _active_leaf(state_path)
    if not leaf:
        _log(f"no active leaf for {wid} - skip")
        return False
    journal = root / "journals" / "work-items" / wid / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf for {wid} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {wid} (another merge in progress) - skip")
        return False
    session_dir = root / "work-items" / wid
    ts = _now()
    try:
        did = False
        did = _process_shared_tasks(notes_dir, journal, session_dir, ts) or did
        did = _process_loose(notes_dir, journal, ts) or did
        return did
    finally:
        _release_lock(lock)


def discover_work_ids(root: Path) -> list[str]:
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[str] = []
    for notes in base.glob("*/agent-notes"):
        wid = notes.parent.name
        if wid.startswith("_"):
            continue
        found.append(wid)
    return sorted(set(found))


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    from journal_snapshot import snapshot_work_item

    for wid in discover_work_ids(root):
        if process_work_item(root, wid):
            snapshot_work_item(root, wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
