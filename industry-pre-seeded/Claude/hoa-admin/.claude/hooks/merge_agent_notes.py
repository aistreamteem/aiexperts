"""Merge background-agent notes into the active journal leaf node."""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import read_text  # noqa: E402
from journal_snapshot import snapshot_work_item  # noqa: E402


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", flush=True)


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _active_leaf(state_path: Path) -> str:
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        return ""
    active = state.get("active") if isinstance(state, dict) else None
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
    note.replace(dest)


def _note_failed(note: Path) -> bool:
    for line in read_text(note).splitlines():
        lower = line.lower()
        if lower.startswith("**status:**") and "fail" in lower:
            return True
        if lower.startswith("status:") and "fail" in lower:
            return True
    return False


def _acquire_lock(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
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


def _process_shared_tasks(
    notes_dir: Path, journal: Path, archive_root: Path, session_dir: Path, ts: str
) -> bool:
    tasks = notes_dir / "tasks"
    if not tasks.is_dir():
        return False
    did = False
    for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
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
        deadline = str(manifest.get("deadline") or "").strip()
        subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
        subtasks = [str(s).strip() for s in subtasks if str(s).strip()]
        total = len(subtasks)
        present = 0
        failed = 0
        missing: list[str] = []
        failed_list: list[str] = []
        for st in subtasks:
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                present += 1
                if _note_failed(nf):
                    failed += 1
                    failed_list.append(st)
            else:
                missing.append(st)
        if present < total:
            stalled = False
            if deadline:
                try:
                    dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                    now = datetime.now(timezone.utc) if dl.tzinfo else datetime.now()
                    if dl.tzinfo and now.tzinfo is None:
                        now = now.replace(tzinfo=timezone.utc)
                    stalled = now > dl
                except ValueError:
                    stalled = False
            if stalled and not (task_dir / ".stall-warned").is_file():
                _append(
                    journal,
                    (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported (no success or failure note): "
                        f"{' '.join(missing) or 'none'}\n\n"
                        "**Blockers:** operator action needed - a subtask agent appears to "
                        "have died without reporting. Re-dispatch the missing subtask(s) "
                        "or investigate.\n"
                    ),
                )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
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
        task_archive = archive_root / task_dir.name
        for st in subtasks:
            note = task_dir / f"{st}.md"
            if note.is_file():
                _append(journal, f"\n### subtask: {st}\n\n{read_text(note)}\n")
                _archive(note, task_archive)
        try:
            (task_archive / "manifest.json").write_text(
                read_text(manifest_path), encoding="utf-8"
            )
        except OSError:
            pass
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
        did = True
    return did


def _process_loose(notes_dir: Path, journal: Path, archive: Path, ts: str) -> bool:
    loose = [
        p
        for p in sorted(notes_dir.glob("*.md"))
        if p.is_file() and p.name.lower() != "readme.md"
    ]
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
        _append(journal, f"\n### {note.stem}\n\n{read_text(note)}\n")
        _archive(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    if not work_id or work_id.upper() == "_TEMPLATE":
        return False
    session_dir = root / "work-items" / work_id
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    # Also accept legacy notes under work-items/<id>/journal/agent-notes/
    legacy_notes = session_dir / "journal" / "agent-notes"
    if not notes_dir.is_dir() and legacy_notes.is_dir():
        notes_dir = legacy_notes
    if not notes_dir.is_dir():
        return False
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    leaf = _active_leaf(state_path)
    if not leaf:
        _log(f"no branch map for {work_id} - skip")
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
        did = _process_shared_tasks(notes_dir, journal, archive, session_dir, ts)
        did = _process_loose(notes_dir, journal, archive, ts) or did
        if did:
            snapshot_work_item(root, work_id)
        return did
    finally:
        _release_lock(lock)


def discover_work_ids(root: Path) -> list[str]:
    found: set[str] = set()
    primary = root / "journals" / "work-items"
    if primary.is_dir():
        for notes in primary.glob("*/agent-notes"):
            wid = notes.parent.name
            if wid.upper() != "_TEMPLATE":
                found.add(wid)
    work_items = root / "work-items"
    if work_items.is_dir():
        for notes in work_items.glob("*/journal/agent-notes"):
            wid = notes.parent.parent.name
            if wid.upper() != "_TEMPLATE":
                found.add(wid)
    return sorted(found)


def merge_all(root: Path | None = None) -> int:
    root = root or Path.cwd()
    for wid in discover_work_ids(root):
        try:
            process_work_item(root, wid)
        except Exception as exc:  # noqa: BLE001 — never fail the stop hook
            _log(f"error merging {wid}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(merge_all())
