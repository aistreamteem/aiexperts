"""Merge background-agent notes into the active journal leaf node."""

from __future__ import annotations

import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, read_text

ROOT = Path(__file__).resolve().parents[2]


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", flush=True)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _acquire(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
        try:
            lock.mkdir()
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


def _append_note(journal: Path, heading: str, body: str) -> None:
    block = f"\n### {heading}\n\n{body.rstrip()}\n"
    with journal.open("a", encoding="utf-8") as fh:
        fh.write(block)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    try:
        note.replace(dest)
    except OSError:
        shutil.copy2(note, dest)
        note.unlink(missing_ok=True)


def _status_failed(text: str) -> bool:
    for line in text.splitlines():
        low = line.lower()
        if "status" in low and "fail" in low:
            return True
    return False


def _process_shared(task_dir: Path, journal: Path, archive_root: Path, session_dir: Path) -> bool:
    if (task_dir / ".merged").is_file():
        return False
    manifest_path = task_dir / "manifest.json"
    if not manifest_path.is_file():
        _log(f"task {task_dir.name} has no manifest - skip")
        return False
    try:
        manifest = json.loads(read_text(manifest_path) or "{}")
    except json.JSONDecodeError:
        _log(f"task {task_dir.name} manifest invalid - skip")
        return False
    task_name = str(manifest.get("task") or "unnamed task")
    deadline = str(manifest.get("deadline") or "").strip()
    subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
    subtasks = [str(s).strip() for s in subtasks if str(s).strip()]
    if not subtasks:
        return False

    missing: list[str] = []
    failed: list[str] = []
    present = 0
    for st in subtasks:
        nf = task_dir / f"{st}.md"
        if nf.is_file():
            present += 1
            if _status_failed(read_text(nf)):
                failed.append(st)
        else:
            missing.append(st)

    ts = _now()
    if present < len(subtasks):
        stalled = False
        if deadline:
            try:
                # Accept Z or offset ISO timestamps
                dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                stalled = datetime.now(timezone.utc) > dl.astimezone(timezone.utc)
            except ValueError:
                stalled = False
        if stalled and not (task_dir / ".stall-warned").is_file():
            with journal.open("a", encoding="utf-8") as fh:
                fh.write(
                    f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                    f"Past deadline ({deadline}) with {present}/{len(subtasks)} subtasks reported.\n"
                    f"Never reported: {', '.join(missing) or 'none'}\n\n"
                    "**Blockers:** operator action needed — re-dispatch missing subtask(s).\n"
                )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                encoding="utf-8",
            )
            (task_dir / ".stall-warned").write_text(ts + "\n", encoding="utf-8")
            _log(f"escalated STALLED task '{task_name}'")
            return True
        _log(f"task '{task_name}' not terminal ({present}/{len(subtasks)}) - waiting")
        return False

    archive = archive_root / task_dir.name
    archive.mkdir(parents=True, exist_ok=True)
    if failed:
        header = (
            f"## △ Background Task PARTIAL: {task_name} - "
            f"{len(failed)} of {len(subtasks)} subtask(s) FAILED (merged {ts})"
        )
        status_note = (
            f"{len(failed)} subtask(s) failed: **{' '.join(failed)}**. "
            "See NEEDS-ATTENTION.md."
        )
        (session_dir / "NEEDS-ATTENTION.md").write_text(
            f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{len(subtasks)} FAILED\n",
            encoding="utf-8",
        )
    else:
        header = f"## Background Task Complete: {task_name} (merged {ts})"
        status_note = (
            f"All {len(subtasks)} subtasks succeeded. "
            "Fold into journal sections via journal-keeper."
        )

    with journal.open("a", encoding="utf-8") as fh:
        fh.write(f"\n{header}\n\n{status_note}\n")
    for st in subtasks:
        note = task_dir / f"{st}.md"
        if note.is_file():
            _append_note(journal, f"subtask: {st}", read_text(note))
            _archive(note, archive)
    try:
        shutil.copy2(manifest_path, archive / "manifest.json")
    except OSError:
        pass
    (task_dir / ".merged").write_text(ts + "\n", encoding="utf-8")
    _log(f"merged shared task '{task_name}' into {journal}")
    return True


def _process_loose(notes_dir: Path, journal: Path, archive: Path) -> bool:
    loose = []
    for note in sorted(notes_dir.glob("*.md")):
        if note.name.lower() == "readme.md":
            continue
        loose.append(note)
    if not loose:
        return False
    ts = _now()
    with journal.open("a", encoding="utf-8") as fh:
        fh.write(
            f"\n## Background Agent Notes (merged {ts})\n\n"
            "Consolidated from background agents. Fold into journal sections via journal-keeper.\n"
        )
    for note in loose:
        _append_note(journal, note.stem, read_text(note))
        _archive(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, wid: str) -> bool:
    if wid in {"_TEMPLATE", "_template"}:
        return False
    notes_dir = root / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        return False
    leaf = active_leaf(root, wid)
    if not leaf:
        _log(f"no active leaf for {wid} - skip")
        return False
    journal = root / "journals" / "work-items" / wid / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf file for {wid} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire(lock):
        _log(f"could not acquire lock for {wid} - skip")
        return False
    did = False
    try:
        archive = notes_dir / "merged"
        session_dir = root / "work-items" / wid
        tasks = notes_dir / "tasks"
        if tasks.is_dir():
            for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
                if _process_shared(task_dir, journal, archive, session_dir):
                    did = True
        if _process_loose(notes_dir, journal, archive):
            did = True
    finally:
        _release(lock)
    return did


def discover_work_ids(root: Path) -> list[str]:
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[str] = []
    for child in base.iterdir():
        if not child.is_dir() or child.name.startswith("_"):
            continue
        if (child / "agent-notes").is_dir():
            found.append(child.name)
    return sorted(set(found))


def main() -> int:
    root = ROOT
    merged_any = False
    for wid in discover_work_ids(root):
        if process_work_item(root, wid):
            merged_any = True
            try:
                from journal_snapshot import snapshot_work_item

                snapshot_work_item(root, wid)
            except Exception as exc:  # noqa: BLE001 — never fail the stop hook
                _log(f"journal snapshot failed for {wid}: {exc}")
    return 0 if True or merged_any else 0


if __name__ == "__main__":
    raise SystemExit(main())
