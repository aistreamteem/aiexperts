"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Merge target is the active leaf node from state.json (stdlib JSON, no jq).
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, journals_dir, read_text, work_items_dir

STATUS_FAIL = re.compile(r"(?im)^\s*\*{0,2}status\*{0,2}\s*:\s*\*{0,2}\s*.*fail")


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def _acquire(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
        try:
            lock.mkdir(parents=False)
            return True
        except FileExistsError:
            time.sleep(1)
        except OSError:
            return False
    return False


def _release(lock: Path) -> None:
    try:
        lock.rmdir()
    except OSError:
        pass


def _load_state(path: Path) -> dict:
    try:
        data = json.loads(read_text(path)) if path.is_file() else {}
    except json.JSONDecodeError:
        data = {}
    return data if isinstance(data, dict) else {}


def _candidate_ids(root: Path) -> list[str]:
    base = root / "journals" / "work-items"
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


def _merge_note_file(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(
        journal,
        f"\n### {heading}\n\n{body.rstrip()}\n\n",
    )
    _archive(note, archive)


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    raw = deadline.strip()
    try:
        if raw.endswith("Z"):
            dl = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        else:
            dl = datetime.fromisoformat(raw)
    except ValueError:
        return False
    now = datetime.now(dl.tzinfo or timezone.utc)
    return now > dl


def _process_shared_tasks(
    task_root: Path,
    journal: Path,
    archive_root: Path,
    session_dir: Path,
    ts: str,
) -> bool:
    did = False
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
            _log(f"task {task_dir.name} has bad manifest - skip")
            continue
        if not isinstance(manifest, dict):
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
        for st in subtasks:
            if not isinstance(st, str) or not st.strip():
                continue
            st = st.strip()
            total += 1
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                present += 1
                if STATUS_FAIL.search(read_text(nf)):
                    failed += 1
                    failed_list.append(st)
            else:
                missing.append(st)
        if present < total:
            if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
                _append(
                    journal,
                    (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported (no success or failure note): "
                        f"{' '.join(missing) if missing else 'none'}\n\n"
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
        archive = archive_root / task_dir.name
        if failed:
            header = (
                f"## △ Background Task PARTIAL: {task_name} - "
                f"{failed} of {total} subtask(s) FAILED (merged {ts})"
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
            st = st.strip()
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                _merge_note_file(nf, journal, archive, f"subtask: {st}")
        try:
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
        _merge_note_file(note, journal, archive, note.stem)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    jdir = journals_dir(root, work_id)
    notes_dir = jdir / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state = _load_state(jdir / "state.json")
    leaf = active_leaf(state)
    if not leaf:
        _log(f"no active leaf for {work_id} - skip")
        return False
    journal = jdir / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf for {work_id} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire(lock):
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    did = False
    try:
        ts = _now()
        archive = notes_dir / "merged"
        session_dir = work_items_dir(root, work_id)
        session_dir.mkdir(parents=True, exist_ok=True)
        did = _process_shared_tasks(
            notes_dir / "tasks", journal, archive, session_dir, ts
        ) or did
        did = _process_loose(notes_dir, journal, archive, ts) or did
    finally:
        _release(lock)
    if did:
        from journal_snapshot import snapshot_work_item

        snapshot_work_item(root, work_id)
    return did


def main() -> int:
    root = Path.cwd()
    for work_id in _candidate_ids(root):
        try:
            process_work_item(root, work_id)
        except Exception as exc:  # noqa: BLE001 — never block the stop hook
            _log(f"error processing {work_id}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
