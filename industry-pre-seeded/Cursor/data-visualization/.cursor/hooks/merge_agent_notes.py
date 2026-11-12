"""Merge background-agent notes into the active Work Item journal node."""

from __future__ import annotations

import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _active_leaf(root: Path, work_id: str) -> Path | None:
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    if not state_path.is_file():
        return None
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return None
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return None
    leaf = active[-1]
    if not isinstance(leaf, str) or not leaf.strip():
        return None
    if "/" in leaf or "\\" in leaf or ".." in leaf:
        return None
    note = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf.strip()}.md"
    return note if note.is_file() else note


def _acquire_lock(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
        try:
            lock.mkdir(parents=False)
            return True
        except FileExistsError:
            time.sleep(1)
        except OSError:
            try:
                lock.mkdir(parents=True)
                return True
            except FileExistsError:
                time.sleep(1)
    return False


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    target = archive / note.name
    if target.exists():
        target = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(target))


def _status_failed(text: str) -> bool:
    value = field(text, "Status").lower()
    return "fail" in value


def _merge_loose(notes_dir: Path, journal: Path, archive: Path) -> bool:
    loose = [
        path
        for path in sorted(notes_dir.glob("*.md"))
        if path.is_file() and path.name.lower() != "readme.md"
    ]
    if not loose:
        return False
    ts = _now()
    chunks = [
        "",
        f"## Background Agent Notes (merged {ts})",
        "",
        "Consolidated from background agents. Fold into the proper journal sections via journal-keeper.",
        "",
    ]
    for note in loose:
        chunks.extend([f"### {note.stem}", "", read_text(note).rstrip(), ""])
        _archive(note, archive)
    _append(journal, "\n".join(chunks) + "\n")
    return True


def _parse_deadline(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _merge_shared(notes_dir: Path, journal: Path, archive: Path, session_dir: Path) -> bool:
    tasks = notes_dir / "tasks"
    if not tasks.is_dir():
        return False
    did = False
    for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
        if (task_dir / ".merged").is_file():
            continue
        manifest_path = task_dir / "manifest.json"
        if not manifest_path.is_file():
            continue
        try:
            manifest = json.loads(read_text(manifest_path))
        except json.JSONDecodeError:
            continue
        subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else None
        if not isinstance(subtasks, list) or not subtasks:
            continue
        names = [str(item).strip() for item in subtasks if str(item).strip()]
        present: list[str] = []
        missing: list[str] = []
        failed: list[str] = []
        for name in names:
            note = task_dir / f"{name}.md"
            if note.is_file():
                present.append(name)
                if _status_failed(read_text(note)):
                    failed.append(name)
            else:
                missing.append(name)
        ts = _now()
        task_name = str(manifest.get("task") or "unnamed task")
        if missing:
            deadline = _parse_deadline(str(manifest.get("deadline") or ""))
            if (
                deadline is not None
                and time.time() > deadline
                and not (task_dir / ".stall-warned").is_file()
            ):
                _append(
                    journal,
                    "\n".join(
                        [
                            "",
                            f"## △ ATTENTION - Background task STALLED: {task_name} ({ts})",
                            "",
                            f"Past deadline with {len(present)}/{len(names)} subtasks reported.",
                            f"Never reported: {', '.join(missing) or 'none'}",
                            "",
                            "**Blockers:** operator action needed - re-dispatch missing subtask(s).",
                            "",
                        ]
                    ),
                )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {', '.join(missing)}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                did = True
            continue
        if failed:
            header = (
                f"## △ Background Task PARTIAL: {task_name} - "
                f"{len(failed)} of {len(names)} subtask(s) FAILED (merged {ts})"
            )
            status = (
                f"{len(failed)} subtask(s) failed: **{' '.join(failed)}**. "
                "See NEEDS-ATTENTION.md."
            )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{len(names)} FAILED "
                f"({', '.join(failed)})\n",
                encoding="utf-8",
            )
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status = f"All {len(names)} subtasks succeeded. Fold via journal-keeper."
        chunks = ["", header, "", status, ""]
        task_archive = archive / task_dir.name
        for name in names:
            note = task_dir / f"{name}.md"
            chunks.extend([f"### subtask: {name}", "", read_text(note).rstrip(), ""])
            _archive(note, task_archive)
        _append(journal, "\n".join(chunks) + "\n")
        try:
            shutil.copy2(manifest_path, task_archive / "manifest.json")
        except OSError:
            pass
        (task_dir / ".merged").write_text("", encoding="utf-8")
        did = True
    return did


def process_work_item(root: Path, work_id: str) -> bool:
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        return False
    journal = _active_leaf(root, work_id)
    if journal is None:
        return False
    journal.parent.mkdir(parents=True, exist_ok=True)
    if not journal.is_file():
        journal.write_text("", encoding="utf-8")
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        return False
    try:
        archive = notes_dir / "merged"
        session_dir = root / "work-items" / work_id
        session_dir.mkdir(parents=True, exist_ok=True)
        did = _merge_shared(notes_dir, journal, archive, session_dir)
        did = _merge_loose(notes_dir, journal, archive) or did
        return did
    finally:
        try:
            lock.rmdir()
        except OSError:
            pass


def discover_work_ids(root: Path) -> list[str]:
    found: set[str] = set()
    base = root / "journals" / "work-items"
    if base.is_dir():
        for notes in base.glob("*/agent-notes"):
            wid = notes.parent.name
            if wid.upper() == "_TEMPLATE":
                continue
            found.add(wid)
    active = active_work_id(root)
    if active:
        found.add(active)
    return sorted(found)


def merge_all(root: Path | None = None) -> list[str]:
    root = root or Path.cwd()
    merged: list[str] = []
    for work_id in discover_work_ids(root):
        if process_work_item(root, work_id):
            merged.append(work_id)
    return merged


def main() -> int:
    merge_all(Path.cwd())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
