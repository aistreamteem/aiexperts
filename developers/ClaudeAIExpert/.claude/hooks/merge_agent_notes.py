"""Merge background-agent notes into the active leaf node (stdlib only).

Replaces merge-agent-notes.sh. Idempotent, lock-guarded, and it ALWAYS exits 0
so it is safe as a Stop / SubagentStop hook.

Notes live in `journals/work-items/<id>/agent-notes/` (the legacy folder
`work-items/<id>/journal/agent-notes/` is still read). Two kinds:

* Loose notes: `agent-notes/<label>.md` (README.md excluded). Merged at once.
* Shared tasks: `agent-notes/tasks/<task-id>/manifest.json`
  `{"task": "...", "subtasks": ["a", "b"], "deadline": "ISO-8601 (optional)"}`
  plus one `<subtask>.md` per subtask. Merged only when every subtask has a
  note. A note whose Status line says "fail" marks the task partial. A task
  past its deadline with missing notes is escalated once (`.stall-warned`).

Merge target: `journals/work-items/<id>/nodes/<leaf>.md`, where `<leaf>` is the
last entry of `active` in `state.json`. Processed notes move to `merged/`.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

import journal_fields  # noqa: E402

LOCK_NAME = ".merge.lock"
LOCK_TRIES = 10
LOCK_STALE_SECONDS = 300

Log = Callable[[str], None]


def _noop(_message: str) -> None:
    return None


# --- discovery -----------------------------------------------------------


def _is_template(name: str) -> bool:
    return name.lower() == "_template"


def _loose_notes(notes_dir: Path) -> list[Path]:
    if not notes_dir.is_dir():
        return []
    return sorted(
        p for p in notes_dir.glob("*.md") if p.is_file() and p.name.lower() != "readme.md"
    )


def _pending_tasks(notes_dir: Path) -> list[Path]:
    tasks = notes_dir / "tasks"
    if not tasks.is_dir():
        return []
    return sorted(d for d in tasks.iterdir() if d.is_dir() and not (d / ".merged").exists())


def _has_pending(notes_dir: Path) -> bool:
    return bool(_loose_notes(notes_dir) or _pending_tasks(notes_dir))


def discover(root: Path) -> dict[str, list[Path]]:
    """work id -> note folders holding pending work (primary first)."""
    found: dict[str, list[Path]] = {}
    patterns = [
        ("journals/work-items", "agent-notes"),
        ("work-items", "journal/agent-notes"),
    ]
    for base_rel, tail in patterns:
        base = root / base_rel
        if not base.is_dir():
            continue
        for item in sorted(base.iterdir()):
            if not item.is_dir() or _is_template(item.name):
                continue
            notes_dir = item / tail
            if _has_pending(notes_dir):
                found.setdefault(item.name, []).append(notes_dir)
    return found


# --- lock ----------------------------------------------------------------


def _acquire(lock: Path) -> bool:
    lock.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(LOCK_TRIES):
        try:
            lock.mkdir()
            return True
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > LOCK_STALE_SECONDS:
                    lock.rmdir()
                    continue
            except OSError:
                pass
            if attempt < LOCK_TRIES - 1:
                time.sleep(1)
        except OSError:
            return False
    return False


def _release(lock: Path) -> None:
    try:
        lock.rmdir()
    except OSError:
        pass


# --- merge primitives ----------------------------------------------------


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _append(journal: Path, text: str) -> None:
    existing = journal_fields.read(journal)
    prefix = "" if not existing or existing.endswith("\n") else "\n"
    with journal.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(prefix + text)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    target = archive / note.name
    if target.exists():
        target = archive / f"{note.stem}.{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(target))


def _note_block(note: Path, heading: str) -> str:
    body = journal_fields.read(note).replace("\r\n", "\n").rstrip("\n")
    return f"\n### {heading}\n\n{body}\n"


def _needs_attention(root: Path, work_id: str, message: str) -> None:
    path = root / "work-items" / work_id / "NEEDS-ATTENTION.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(message + "\n", encoding="utf-8")


def _is_failed(note: Path) -> bool:
    return "fail" in journal_fields.field(journal_fields.read(note), "Status").lower()


def _deadline_passed(value: str) -> bool:
    if not value:
        return False
    try:
        moment = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    if moment.tzinfo is None:
        moment = moment.astimezone()
    return datetime.now().astimezone() > moment


def _safe_name(name: object) -> bool:
    return isinstance(name, str) and bool(name.strip()) and not any(
        bad in name for bad in ("/", "\\", "..")
    )


def _load_manifest(path: Path) -> dict | None:
    try:
        data = json.loads(journal_fields.read(path))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _merge_task(root: Path, work_id: str, notes_dir: Path, task_dir: Path, journal: Path, log: Log) -> bool:
    manifest = _load_manifest(task_dir / "manifest.json")
    if manifest is None:
        log(f"task {task_dir.name} has no usable manifest - skip")
        return False
    task_name = str(manifest.get("task") or "unnamed task")
    deadline = str(manifest.get("deadline") or "")
    subtasks = [s.strip() for s in manifest.get("subtasks") or [] if _safe_name(s)]
    total = len(subtasks)
    present = [s for s in subtasks if (task_dir / f"{s}.md").is_file()]
    missing = [s for s in subtasks if s not in present]
    failed = [s for s in present if _is_failed(task_dir / f"{s}.md")]
    ts = _now()

    if missing:
        if _deadline_passed(deadline) and not (task_dir / ".stall-warned").exists():
            _append(
                journal,
                f"\n## \u25b3 ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                f"Past deadline ({deadline}) with {len(present)}/{total} subtasks reported.\n"
                f"Never reported (no success or failure note): {' '.join(missing) or 'none'}\n\n"
                "**Blockers:** operator action needed - a subtask agent appears to have died "
                "without reporting. Re-dispatch the missing subtask(s) or investigate.\n",
            )
            _needs_attention(
                root, work_id, f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}"
            )
            (task_dir / ".stall-warned").touch()
            log(f"escalated STALLED task '{task_name}' (missing: {' '.join(missing)})")
            return True
        log(f"task '{task_name}' not terminal ({len(present)}/{total} reported) - waiting")
        return False

    if not subtasks:
        log(f"task '{task_name}' lists no subtasks - skip")
        return False

    if failed:
        header = (
            f"## \u25b3 Background Task PARTIAL: {task_name} - {len(failed)} of {total} "
            f"subtask(s) FAILED (merged {ts})"
        )
        status = (
            f"{len(failed)} subtask(s) failed after their retry budget: **{' '.join(failed)}**. "
            "Successful work below is still captured. **Blockers:** operator must review the "
            "failed subtask(s) and decide to re-dispatch or accept. See NEEDS-ATTENTION.md."
        )
    else:
        header = f"## Background Task Complete: {task_name} (merged {ts})"
        status = (
            f"All {total} subtasks succeeded. Fold into the proper journal sections "
            "(Artifacts, Resolved Q&A, Next action) via journal-keeper."
        )
    _append(journal, f"\n{header}\n\n{status}\n")
    archive = notes_dir / "merged" / task_dir.name
    for name in subtasks:
        note = task_dir / f"{name}.md"
        _append(journal, _note_block(note, f"subtask: {name}"))
        _archive(note, archive)
    shutil.copy2(task_dir / "manifest.json", archive / "manifest.json")
    (task_dir / ".merged").touch()
    if failed:
        _needs_attention(
            root,
            work_id,
            f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{total} FAILED ({' '.join(failed)})",
        )
        log(f"merged PARTIAL task '{task_name}' - {len(failed)}/{total} failed")
    else:
        log(f"merged shared task '{task_name}' into {journal}")
    return True


def _merge_loose(notes_dir: Path, journal: Path, log: Log) -> bool:
    notes = _loose_notes(notes_dir)
    if not notes:
        return False
    _append(
        journal,
        f"\n## Background Agent Notes (merged {_now()})\n\n"
        "Consolidated from background agents. Fold into the proper journal sections "
        "via journal-keeper.\n",
    )
    for note in notes:
        _append(journal, _note_block(note, note.stem))
        _archive(note, notes_dir / "merged")
    log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, work_id: str, notes_dirs: list[Path], log: Log = _noop) -> bool:
    """Merge all pending notes for one work item. True when anything merged."""
    leaf = journal_fields.active_leaf(root, work_id)
    journal = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf}.md"
    if not leaf or not journal.is_file():
        log(f"no active leaf node for {work_id} - skip")
        return False

    lock = root / "journals" / "work-items" / work_id / "agent-notes" / LOCK_NAME
    if not _acquire(lock):
        log(f"could not acquire lock for {work_id} - skip")
        return False
    did_merge = False
    try:
        for notes_dir in notes_dirs:
            for task_dir in _pending_tasks(notes_dir):
                did_merge |= _merge_task(root, work_id, notes_dir, task_dir, journal, log)
            did_merge |= _merge_loose(notes_dir, journal, log)
    finally:
        _release(lock)
    return did_merge


def merge_all(root: Path, log: Log = _noop) -> list[str]:
    """Merge every work item's pending notes; returns ids that merged."""
    root = Path(root)
    merged: list[str] = []
    for work_id, notes_dirs in discover(root).items():
        try:
            if process_work_item(root, work_id, notes_dirs, log):
                merged.append(work_id)
        except Exception as exc:  # one bad work item must not stop the others
            log(f"error merging {work_id}: {exc}")
    for work_id in merged:
        try:
            import journal_snapshot
        except ImportError:
            break
        try:
            journal_snapshot.snapshot(root, work_id)
        except Exception as exc:
            log(f"snapshot failed for {work_id}: {exc} (merge is on disk)")
    return merged


def main(root: Path | None = None, log: Log | None = None) -> int:
    """Run the merge. Always returns 0."""
    base = Path(root) if root else Path(__file__).resolve().parents[2]
    emit = log or (lambda message: print(f"[merge-agent-notes] {message}", file=sys.stderr))
    try:
        merge_all(base, emit)
    except Exception as exc:
        emit(f"error: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
