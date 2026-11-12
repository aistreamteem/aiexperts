"""Merge background-agent notes into the active journal node. No jq required."""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, read_text

ROOT = Path(__file__).resolve().parents[2]


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _lock(notes_dir: Path) -> Path | None:
    lock = notes_dir / ".merge.lock"
    for _ in range(10):
        try:
            lock.mkdir()
            return lock
        except FileExistsError:
            time.sleep(1)
        except OSError:
            return None
    return None


def _unlock(lock: Path | None) -> None:
    if lock is None:
        return
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


def _failed_status(text: str) -> bool:
    for line in text.splitlines():
        low = line.lower()
        if "status" in low and "fail" in low:
            return True
    return False


def _merge_note_body(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note).rstrip()
    _append(
        journal,
        f"\n### {heading}\n\n{body}\n\n" if body else f"\n### {heading}\n\n",
    )
    _archive(note, archive)


def _process_shared(task_dir: Path, journal: Path, archive_root: Path, artifact_dir: Path) -> bool:
    if (task_dir / ".merged").is_file():
        return False
    manifest_path = task_dir / "manifest.json"
    if not manifest_path.is_file():
        _log(f"task {task_dir.name} has no manifest - skip")
        return False
    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError:
        _log(f"task {task_dir.name} has bad manifest - skip")
        return False
    task_name = str(manifest.get("task") or "unnamed task")
    subtasks = manifest.get("subtasks") or []
    if not isinstance(subtasks, list) or not subtasks:
        return False
    deadline = str(manifest.get("deadline") or "").strip()
    missing: list[str] = []
    failed: list[str] = []
    present = 0
    for st in subtasks:
        if not isinstance(st, str) or not st.strip():
            continue
        name = st.strip()
        nf = task_dir / f"{name}.md"
        if nf.is_file():
            present += 1
            if _failed_status(read_text(nf)):
                failed.append(name)
        else:
            missing.append(name)
    total = len([s for s in subtasks if isinstance(s, str) and s.strip()])
    ts = _now()
    if present < total:
        if deadline and not (task_dir / ".stall-warned").is_file():
            try:
                dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                if datetime.now(timezone.utc) > dl.astimezone(timezone.utc):
                    _append(
                        journal,
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported: {', '.join(missing) or 'none'}\n\n"
                        "**Blockers:** operator action needed.\n",
                    )
                    (artifact_dir / "NEEDS-ATTENTION.md").write_text(
                        f"STALLED task '{task_name}' at {ts}: missing {', '.join(missing)}\n",
                        encoding="utf-8",
                    )
                    (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                    _log(f"escalated STALLED task '{task_name}'")
                    return True
            except ValueError:
                pass
        _log(f"task '{task_name}' not terminal ({present}/{total}) - waiting")
        return False

    archive = archive_root / task_dir.name
    if failed:
        header = (
            f"## △ Background Task PARTIAL: {task_name} - "
            f"{len(failed)} of {total} subtask(s) FAILED (merged {ts})"
        )
        note = (
            f"{len(failed)} subtask(s) failed: **{' '.join(failed)}**. "
            "See NEEDS-ATTENTION.md."
        )
        (artifact_dir / "NEEDS-ATTENTION.md").write_text(
            f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{total} FAILED ({' '.join(failed)})\n",
            encoding="utf-8",
        )
    else:
        header = f"## Background Task Complete: {task_name} (merged {ts})"
        note = f"All {total} subtasks succeeded. Fold into journal sections via journal-keeper."
    _append(journal, f"\n{header}\n\n{note}\n")
    for st in subtasks:
        if not isinstance(st, str) or not st.strip():
            continue
        name = st.strip()
        nf = task_dir / f"{name}.md"
        if nf.is_file():
            _merge_note_body(nf, journal, archive, f"subtask: {name}")
    shutil.copy2(manifest_path, archive / "manifest.json")
    (task_dir / ".merged").write_text("", encoding="utf-8")
    _log(f"merged shared task '{task_name}'")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        return False
    leaf = active_leaf(root, work_id)
    if not leaf:
        _log(f"no active leaf for {work_id} - skip")
        return False
    journal = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf file for {work_id} - skip")
        return False
    artifact_dir = root / "work-items" / work_id
    archive = notes_dir / "merged"
    lock = _lock(notes_dir)
    if lock is None:
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    did = False
    try:
        tasks = notes_dir / "tasks"
        if tasks.is_dir():
            for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
                if _process_shared(task_dir, journal, archive, artifact_dir):
                    did = True
        loose = [
            p
            for p in notes_dir.glob("*.md")
            if p.name.lower() != "readme.md"
        ]
        if loose:
            ts = _now()
            _append(
                journal,
                f"\n## Background Agent Notes (merged {ts})\n\n"
                "Consolidated from background agents. Fold into journal sections via journal-keeper.\n",
            )
            for note in loose:
                _merge_note_body(note, journal, archive, note.stem)
            did = True
            _log(f"merged loose notes into {journal}")
    finally:
        _unlock(lock)
    return did


def candidate_ids(root: Path) -> list[str]:
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
    root = Path.cwd()
    if not (root / ".cursor").is_dir():
        root = ROOT
    merged_any = False
    for wid in candidate_ids(root):
        if process_work_item(root, wid):
            merged_any = True
            from journal_snapshot import snapshot_work_item

            snapshot_work_item(root, wid)
    return 0 if True else int(merged_any)


if __name__ == "__main__":
    raise SystemExit(main())
