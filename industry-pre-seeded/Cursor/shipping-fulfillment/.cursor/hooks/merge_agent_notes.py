"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Merge target is the active leaf node from state.json (stdlib JSON, no jq).
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text

ROOT = Path(__file__).resolve().parents[2]


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
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def _archive_note(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    try:
        shutil.move(str(note), str(dest))
    except OSError:
        pass


def _status_failed(note_text: str) -> bool:
    status = field(note_text, "Status").lower()
    if "fail" in status:
        return True
    for line in note_text.splitlines():
        low = line.lower().strip()
        if low.startswith("**status:**") and "fail" in low:
            return True
    return False


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    raw = deadline.strip()
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        dl = datetime.fromisoformat(raw)
        if dl.tzinfo is None:
            dl = dl.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > dl.astimezone(timezone.utc)
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
    notes_dir: Path,
    journal: Path,
    archive_root: Path,
    session_dir: Path,
    ts: str,
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
        deadline = str(manifest.get("deadline") or "")
        subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
        subtasks = [str(s) for s in subtasks]
        total = len(subtasks)
        present = 0
        failed = 0
        missing_list: list[str] = []
        failed_list: list[str] = []
        for st in subtasks:
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                present += 1
                if _status_failed(read_text(nf)):
                    failed += 1
                    failed_list.append(st)
            else:
                missing_list.append(st)
        if present < total:
            if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
                missing = " ".join(missing_list) or "none"
                _append(
                    journal,
                    (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported (no success or failure note): {missing}\n\n"
                        "**Blockers:** operator action needed - a subtask agent appears to have "
                        "died without reporting. Re-dispatch the missing subtask(s) or investigate.\n"
                    ),
                )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {missing}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}' (missing: {missing})")
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
        archive = archive_root / task_dir.name
        for st in subtasks:
            note = task_dir / f"{st}.md"
            if note.is_file():
                _merge_one_note(note, journal, archive, f"subtask: {st}")
        try:
            archive.mkdir(parents=True, exist_ok=True)
            shutil.copy2(manifest_path, archive / "manifest.json")
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
        for p in notes_dir.glob("*.md")
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
    for note in sorted(loose):
        _merge_one_note(note, journal, archive, note.stem)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(wid: str) -> bool:
    notes_dir = ROOT / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state_path = ROOT / "journals" / "work-items" / wid / "state.json"
    leaf = _active_leaf(state_path)
    if not leaf:
        _log(f"no branch map for {wid} - skip")
        return False
    journal = ROOT / "journals" / "work-items" / wid / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf for {wid} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {wid} - skip")
        return False
    try:
        ts = _now()
        archive = notes_dir / "merged"
        session_dir = ROOT / "work-items" / wid
        did = False
        did = _process_shared_tasks(notes_dir, journal, archive, session_dir, ts) or did
        did = _process_loose(notes_dir, journal, archive, ts) or did
        return did
    finally:
        _release_lock(lock)


def candidate_ids() -> list[str]:
    base = ROOT / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[str] = []
    for notes in base.glob("*/agent-notes"):
        if not notes.is_dir():
            continue
        wid = notes.parent.name
        if wid.startswith("_"):
            continue
        found.append(wid)
    return sorted(set(found))


def merge_all() -> list[str]:
    merged: list[str] = []
    for wid in candidate_ids():
        if process_work_item(wid):
            merged.append(wid)
    return merged


def main() -> int:
    merge_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
