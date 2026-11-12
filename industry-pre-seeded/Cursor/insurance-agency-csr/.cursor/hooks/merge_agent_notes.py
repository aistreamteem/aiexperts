"""Merge background-agent notes into the active leaf node journal."""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import field, read_text  # noqa: E402

STATUS_FAIL = re.compile(r"^\s*\*{0,2}status\*{0,2}\s*:\s*\*{0,2}\s*.*fail", re.I | re.M)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


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


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _merge_note(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note).rstrip()
    _append(
        journal,
        f"\n### {heading}\n\n{body}\n\n" if body else f"\n### {heading}\n\n",
    )
    _archive(note, archive)


def _acquire_lock(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
        try:
            lock.mkdir(parents=False)
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


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    raw = deadline.strip().replace("Z", "+00:00")
    try:
        due = datetime.fromisoformat(raw)
    except ValueError:
        return False
    now = datetime.now(due.tzinfo) if due.tzinfo else datetime.now(timezone.utc)
    return now > due


def _process_shared(task_dir: Path, journal: Path, archive_root: Path, session_dir: Path, ts: str) -> bool:
    if (task_dir / ".merged").is_file():
        return False
    manifest_path = task_dir / "manifest.json"
    if not manifest_path.is_file():
        _log(f"task {task_dir.name} has no manifest - skip")
        return False
    try:
        manifest = json.loads(read_text(manifest_path) or "{}")
    except json.JSONDecodeError:
        _log(f"task {task_dir.name} has invalid manifest - skip")
        return False
    task_name = str(manifest.get("task") or "unnamed task")
    deadline = str(manifest.get("deadline") or "")
    subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
    subtasks = [str(s).strip() for s in subtasks if str(s).strip()]
    if not subtasks:
        return False

    missing: list[str] = []
    failed: list[str] = []
    present = 0
    for name in subtasks:
        note = task_dir / f"{name}.md"
        if note.is_file():
            present += 1
            if STATUS_FAIL.search(read_text(note)):
                failed.append(name)
        else:
            missing.append(name)

    if present < len(subtasks):
        if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
            _append(
                journal,
                (
                    f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                    f"Past deadline ({deadline}) with {present}/{len(subtasks)} subtasks reported.\n"
                    f"Never reported (no success or failure note): {' '.join(missing) or 'none'}\n\n"
                    "**Blockers:** operator action needed - a subtask agent appears to have died "
                    "without reporting. Re-dispatch the missing subtask(s) or investigate.\n"
                ),
            )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                encoding="utf-8",
            )
            (task_dir / ".stall-warned").write_text("", encoding="utf-8")
            _log(f"escalated STALLED task '{task_name}' (missing: {' '.join(missing)})")
            return True
        _log(f"task '{task_name}' not terminal ({present}/{len(subtasks)} reported) - waiting")
        return False

    archive = archive_root / task_dir.name
    if failed:
        header = (
            f"## △ Background Task PARTIAL: {task_name} - {len(failed)} of "
            f"{len(subtasks)} subtask(s) FAILED (merged {ts})"
        )
        status = (
            f"{len(failed)} subtask(s) failed after their retry budget: **{' '.join(failed)}**. "
            "Successful work below is still captured. **Blockers:** operator must review the "
            "failed subtask(s) and decide to re-dispatch or accept. See NEEDS-ATTENTION.md."
        )
        (session_dir / "NEEDS-ATTENTION.md").write_text(
            f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{len(subtasks)} FAILED ({' '.join(failed)})\n",
            encoding="utf-8",
        )
    else:
        header = f"## Background Task Complete: {task_name} (merged {ts})"
        status = (
            f"All {len(subtasks)} subtasks succeeded. Fold into the proper journal sections "
            "(Artifacts, Resolved Q&A, Next action) via journal-keeper."
        )
    _append(journal, f"\n{header}\n\n{status}\n")
    for name in subtasks:
        note = task_dir / f"{name}.md"
        if note.is_file():
            _merge_note(note, journal, archive, f"subtask: {name}")
    try:
        shutil.copy2(manifest_path, archive / "manifest.json")
    except OSError:
        pass
    (task_dir / ".merged").write_text("", encoding="utf-8")
    _log(f"merged shared task '{task_name}' into {journal}")
    return True


def process_work_item(root: Path, wid: str) -> bool:
    notes_dir = root / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        # Also accept legacy notes under work-items/<id>/journal/agent-notes
        legacy = root / "work-items" / wid / "journal" / "agent-notes"
        if legacy.is_dir():
            notes_dir = legacy
        else:
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
        _log(f"could not acquire lock for {wid} - skip")
        return False

    did_merge = False
    ts = _now()
    archive = notes_dir / "merged"
    session_dir = root / "work-items" / wid
    try:
        tasks = notes_dir / "tasks"
        if tasks.is_dir():
            for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
                if _process_shared(task_dir, journal, archive, session_dir, ts):
                    did_merge = True

        loose = [
            p
            for p in sorted(notes_dir.glob("*.md"))
            if p.name.lower() != "readme.md"
        ]
        if loose:
            _append(
                journal,
                (
                    f"\n## Background Agent Notes (merged {ts})\n\n"
                    "Consolidated from background agents. Fold into the proper journal "
                    "sections via journal-keeper.\n"
                ),
            )
            for note in loose:
                _merge_note(note, journal, archive, note.stem)
            _log(f"merged loose notes into {journal}")
            did_merge = True
    finally:
        _release_lock(lock)

    return did_merge


def discover_work_ids(root: Path) -> list[str]:
    found: set[str] = set()
    for base in (
        root / "journals" / "work-items",
        root / "work-items",
    ):
        if not base.is_dir():
            continue
        for path in base.rglob("agent-notes"):
            if not path.is_dir():
                continue
            # journals/work-items/<id>/agent-notes  OR  work-items/<id>/journal/agent-notes
            parts = path.parts
            if "_TEMPLATE" in parts or "_template" in parts:
                continue
            if "journals" in parts and "work-items" in parts:
                idx = parts.index("work-items")
                if idx + 1 < len(parts):
                    found.add(parts[idx + 1])
            elif "work-items" in parts:
                idx = parts.index("work-items")
                if idx + 1 < len(parts):
                    found.add(parts[idx + 1])
    return sorted(found)


def main() -> int:
    root = Path.cwd()
    merged_any = False
    for wid in discover_work_ids(root):
        if process_work_item(root, wid):
            merged_any = True
            try:
                from journal_snapshot import snapshot_work_item

                snapshot_work_item(root, wid)
            except Exception as exc:  # noqa: BLE001 — never fail the merge
                _log(f"post-journal-update failed for {wid}: {exc}")
    return 0 if True else int(merged_any)


if __name__ == "__main__":
    raise SystemExit(main())
