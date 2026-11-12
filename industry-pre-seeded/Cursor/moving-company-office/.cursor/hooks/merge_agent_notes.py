"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/. The merge target is the
active leaf node from state.json. Always exits 0.
"""

from __future__ import annotations

import json
import re
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", flush=True)


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _active_leaf(root: Path, work_id: str) -> tuple[Path | None, str]:
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    if not state_path.is_file():
        return None, ""
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return None, ""
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return None, ""
    leaf = active[-1]
    if not isinstance(leaf, str) or not leaf.strip():
        return None, ""
    if "/" in leaf or "\\" in leaf or ".." in leaf:
        return None, ""
    node = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf.strip()}.md"
    if not node.is_file():
        return None, leaf.strip()
    return node, leaf.strip()


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


def _append(node: Path, text: str) -> None:
    existing = read_text(node)
    sep = "" if existing.endswith("\n") or not existing else "\n"
    node.write_text(existing + sep + text, encoding="utf-8")


def _archive_note(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _status_failed(note_text: str) -> bool:
    status = field(note_text, "Status").lower()
    if "fail" in status:
        return True
    return bool(re.search(r"(?im)^\s*\*{0,2}status\*{0,2}\s*:.*fail", note_text))


def _parse_deadline(raw: str) -> datetime | None:
    if not raw or not raw.strip():
        return None
    text = raw.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _merge_loose(notes_dir: Path, node: Path, archive: Path, ts: str) -> bool:
    loose = [
        p
        for p in notes_dir.glob("*.md")
        if p.is_file() and p.name.lower() != "readme.md"
    ]
    if not loose:
        return False
    parts = [
        "",
        f"## Background Agent Notes (merged {ts})",
        "",
        "Consolidated from background agents. Fold into the proper journal sections via journal-keeper.",
        "",
    ]
    for note in sorted(loose):
        body = read_text(note).rstrip()
        parts.append(f"### {note.stem}")
        parts.append("")
        parts.append(body)
        parts.append("")
        _archive_note(note, archive)
    _append(node, "\n".join(parts))
    _log(f"merged loose notes into {node}")
    return True


def _merge_shared_tasks(
    root: Path,
    work_id: str,
    notes_dir: Path,
    node: Path,
    archive: Path,
    ts: str,
) -> bool:
    tasks_dir = notes_dir / "tasks"
    if not tasks_dir.is_dir():
        return False
    did = False
    session_dir = root / "work-items" / work_id
    for task_dir in sorted(p for p in tasks_dir.iterdir() if p.is_dir()):
        if (task_dir / ".merged").is_file():
            continue
        manifest_path = task_dir / "manifest.json"
        if not manifest_path.is_file():
            _log(f"task {task_dir.name} has no manifest - skip")
            continue
        try:
            manifest = json.loads(read_text(manifest_path))
        except json.JSONDecodeError:
            _log(f"task {task_dir.name} has invalid manifest - skip")
            continue
        task_name = str(manifest.get("task") or "unnamed task")
        subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else None
        if not isinstance(subtasks, list) or not subtasks:
            _log(f"task {task_dir.name} has no subtasks - skip")
            continue
        names = [str(s).strip() for s in subtasks if str(s).strip()]
        total = len(names)
        present = 0
        failed = 0
        missing: list[str] = []
        failed_list: list[str] = []
        for name in names:
            nf = task_dir / f"{name}.md"
            if nf.is_file():
                present += 1
                if _status_failed(read_text(nf)):
                    failed += 1
                    failed_list.append(name)
            else:
                missing.append(name)

        if present < total:
            deadline = _parse_deadline(str(manifest.get("deadline") or ""))
            now = datetime.now(timezone.utc).astimezone()
            stall_marker = task_dir / ".stall-warned"
            if deadline is not None and now > deadline and not stall_marker.is_file():
                block = "\n".join(
                    [
                        "",
                        f"## △ ATTENTION - Background task STALLED: {task_name} ({ts})",
                        "",
                        f"Past deadline ({deadline.isoformat()}) with {present}/{total} subtasks reported.",
                        f"Never reported (no success or failure note): {' '.join(missing) or 'none'}",
                        "",
                        "**Blockers:** operator action needed - a subtask agent appears to have died without reporting. Re-dispatch the missing subtask(s) or investigate.",
                        "",
                    ]
                )
                _append(node, block)
                session_dir.mkdir(parents=True, exist_ok=True)
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                    encoding="utf-8",
                )
                stall_marker.write_text("", encoding="utf-8")
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
                f"{failed} subtask(s) failed after their retry budget: **{' '.join(failed_list)}**. "
                "Successful work below is still captured. **Blockers:** operator must review "
                "the failed subtask(s) and decide to re-dispatch or accept. See NEEDS-ATTENTION.md."
            )
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status_note = (
                f"All {total} subtasks succeeded. Fold into the proper journal sections "
                "(Artifacts, Resolved Q&A, Next action) via journal-keeper."
            )
        parts = ["", header, "", status_note, ""]
        task_archive = archive / task_dir.name
        task_archive.mkdir(parents=True, exist_ok=True)
        for name in names:
            nf = task_dir / f"{name}.md"
            body = read_text(nf).rstrip()
            parts.append(f"### subtask: {name}")
            parts.append("")
            parts.append(body)
            parts.append("")
            _archive_note(nf, task_archive)
        shutil.copy2(manifest_path, task_archive / "manifest.json")
        (task_dir / ".merged").write_text("", encoding="utf-8")
        _append(node, "\n".join(parts))
        if failed:
            session_dir.mkdir(parents=True, exist_ok=True)
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED ({' '.join(failed_list)})\n",
                encoding="utf-8",
            )
            _log(f"merged PARTIAL task '{task_name}' - {failed}/{total} failed")
        else:
            _log(f"merged shared task '{task_name}' into {node}")
        did = True
    return did


def process_work_item(root: Path, work_id: str) -> bool:
    if work_id in {"_TEMPLATE", "_template"}:
        return False
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        # Also accept legacy work-items/<id>/journal/agent-notes for discovery only
        legacy = root / "work-items" / work_id / "journal" / "agent-notes"
        if legacy.is_dir():
            notes_dir = legacy
        else:
            return False
    node, leaf = _active_leaf(root, work_id)
    if node is None:
        _log(f"no branch map or active leaf for {work_id} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    try:
        ts = _now()
        archive = notes_dir / "merged"
        did = False
        did = _merge_shared_tasks(root, work_id, notes_dir, node, archive, ts) or did
        did = _merge_loose(notes_dir, node, archive, ts) or did
        return did
    finally:
        _release_lock(lock)


def discover_work_ids(root: Path) -> list[str]:
    found: set[str] = set()
    journals = root / "journals" / "work-items"
    if journals.is_dir():
        for notes in journals.glob("*/agent-notes"):
            if notes.is_dir():
                found.add(notes.parent.name)
    work_items = root / "work-items"
    if work_items.is_dir():
        for notes in work_items.glob("*/journal/agent-notes"):
            if notes.is_dir():
                # work-items/<id>/journal/agent-notes
                found.add(notes.parents[1].name)
    active = active_work_id(root)
    if active:
        found.add(active)
    return sorted(wid for wid in found if wid and wid not in {"_TEMPLATE", "_template"})


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
