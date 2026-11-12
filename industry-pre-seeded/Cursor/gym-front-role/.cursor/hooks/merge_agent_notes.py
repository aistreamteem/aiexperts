"""Deterministic merge of background-agent notes into the active journal node.

The only merge in the system. Run by the stop and subagentStop hooks (via
on_stop.py) and callable by hand. Idempotent, lock-guarded, and always exits 0.

Notes folder:  journals/work-items/<id>/agent-notes/
Merge target:  the active leaf node file named by state.json ("active"[-1])

Two kinds of notes:
  * Loose notes   agent-notes/<label>.md           merged on the next hook fire
  * Shared tasks  agent-notes/tasks/<task-id>/     manifest.json
                  {"task": "...", "subtasks": ["a", "b"], "deadline": "ISO-8601"?}
                  plus one <subtask>.md per subtask. Merged only when every
                  subtask has a note. A note whose Status line contains "fail"
                  makes the merge PARTIAL. Past the deadline with notes missing,
                  one escalation is written (.stall-warned) plus
                  work-items/<id>/NEEDS-ATTENTION.md.

Merged notes are archived under agent-notes/merged/. After any merge the audit
snapshot (journal_snapshot.snapshot) runs.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from journal_fields import _read, active_leaf, node_path  # noqa: E402
import journal_snapshot  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
_FAIL_STATUS = re.compile(r"^\s*\**status\**\s*:.*fail", re.IGNORECASE | re.MULTILINE)
_LOCK_TRIES = 10
_STALE_LOCK_SECONDS = 300


def _log(message: str) -> None:
    print(f"[merge-agent-notes] {message}", file=sys.stderr)


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _acquire(lock: Path) -> bool:
    for attempt in range(_LOCK_TRIES):
        try:
            lock.mkdir()
            return True
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > _STALE_LOCK_SECONDS:
                    lock.rmdir()  # abandoned by a crashed merge
                    continue
            except OSError:
                pass
            if attempt < _LOCK_TRIES - 1:
                time.sleep(1)
        except OSError:
            return False
    return False


def _release(lock: Path) -> None:
    try:
        lock.rmdir()
    except OSError:
        pass


def _archive(note: Path, archive: Path, heading: str, journal: Path) -> None:
    body = _read(note).rstrip("\n")
    _append(journal, f"\n### {heading}\n\n{body}\n\n")
    archive.mkdir(parents=True, exist_ok=True)
    target = archive / note.name
    if target.exists():
        target = archive / f"{note.stem}-{datetime.now().strftime('%Y%m%d%H%M%S')}{note.suffix}"
    shutil.move(str(note), str(target))


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    try:
        when = datetime.fromisoformat(deadline.strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    if when.tzinfo is None:
        when = when.astimezone()
    return datetime.now().astimezone() > when


def _load_manifest(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _merge_tasks(root: Path, wid: str, notes_dir: Path, journal: Path) -> bool:
    tasks_dir = notes_dir / "tasks"
    if not tasks_dir.is_dir():
        return False
    merged_any = False
    archive_root = notes_dir / "merged"
    for task_dir in sorted(p for p in tasks_dir.iterdir() if p.is_dir()):
        if (task_dir / ".merged").exists():
            continue
        manifest = _load_manifest(task_dir / "manifest.json")
        if manifest is None:
            _log(f"task {task_dir.name} has no readable manifest - skip")
            continue
        task_name = str(manifest.get("task") or "unnamed task")
        deadline = str(manifest.get("deadline") or "")
        subtasks = [str(s).strip() for s in manifest.get("subtasks") or [] if str(s).strip()]
        if not subtasks:
            _log(f"task {task_dir.name} lists no subtasks - skip")
            continue
        present = [s for s in subtasks if (task_dir / f"{s}.md").is_file()]
        missing = [s for s in subtasks if s not in present]
        failed = [s for s in present if _FAIL_STATUS.search(_read(task_dir / f"{s}.md"))]
        total, ts = len(subtasks), _now()

        if missing:
            if _past_deadline(deadline) and not (task_dir / ".stall-warned").exists():
                _append(
                    journal,
                    f"\n## ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                    f"Past deadline ({deadline}) with {len(present)}/{total} subtasks reported.\n"
                    f"Never reported (no success or failure note): {' '.join(missing)}\n\n"
                    "**Blockers:** operator action needed - a subtask agent appears to have died "
                    "without reporting. Re-dispatch the missing subtask(s) or investigate.\n",
                )
                attention = root / "work-items" / wid / "NEEDS-ATTENTION.md"
                attention.parent.mkdir(parents=True, exist_ok=True)
                attention.write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n", encoding="utf-8"
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}' (missing: {' '.join(missing)})")
                merged_any = True
            else:
                _log(f"task '{task_name}' not terminal ({len(present)}/{total} reported) - waiting")
            continue

        if failed:
            header = f"## Background Task PARTIAL: {task_name} - {len(failed)} of {total} subtask(s) FAILED (merged {ts})"
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
        task_archive = archive_root / task_dir.name
        for subtask in subtasks:
            _archive(task_dir / f"{subtask}.md", task_archive, f"subtask: {subtask}", journal)
        shutil.copy2(task_dir / "manifest.json", task_archive / "manifest.json")
        (task_dir / ".merged").write_text("", encoding="utf-8")
        if failed:
            attention = root / "work-items" / wid / "NEEDS-ATTENTION.md"
            attention.parent.mkdir(parents=True, exist_ok=True)
            attention.write_text(
                f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{total} FAILED ({' '.join(failed)})\n",
                encoding="utf-8",
            )
            _log(f"merged PARTIAL task '{task_name}' - {len(failed)}/{total} failed")
        else:
            _log(f"merged shared task '{task_name}' into {journal}")
        merged_any = True
    return merged_any


def _merge_loose(notes_dir: Path, journal: Path) -> bool:
    loose = sorted(
        p for p in notes_dir.glob("*.md") if p.is_file() and p.name.lower() != "readme.md"
    )
    if not loose:
        return False
    _append(
        journal,
        f"\n## Background Agent Notes (merged {_now()})\n\n"
        "Consolidated from background agents. Fold into the proper journal sections via journal-keeper.\n",
    )
    for note in loose:
        _archive(note, notes_dir / "merged", note.stem, journal)
    _log(f"merged {len(loose)} loose note(s) into {journal}")
    return True


def process_work_item(root: Path, wid: str, notes_dir: Path) -> bool:
    leaf = active_leaf(root, wid)
    journal = node_path(root, wid, leaf) if leaf else None
    if journal is None or not journal.is_file():
        _log(f"no active leaf node for {wid} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire(lock):
        _log(f"could not acquire lock for {wid} - skip")
        return False
    try:
        merged = _merge_tasks(root, wid, notes_dir, journal)
        merged = _merge_loose(notes_dir, journal) or merged
    finally:
        _release(lock)
    return merged


def main(root: Path | None = None) -> int:
    root = root or ROOT
    try:
        base = root / "journals" / "work-items"
        for notes_dir in sorted(base.glob("*/agent-notes")):
            wid = notes_dir.parent.name
            if wid.lower().startswith("_template") or not notes_dir.is_dir():
                continue
            try:
                if process_work_item(root, wid, notes_dir):
                    journal_snapshot.snapshot(wid, root)
            except Exception as exc:  # one work item must not block the rest
                _log(f"{wid}: {exc}")
    except Exception as exc:
        _log(f"unexpected error: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
