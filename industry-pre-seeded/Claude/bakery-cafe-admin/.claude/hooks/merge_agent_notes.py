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

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import read_text  # noqa: E402

STATUS_FAIL_RE = re.compile(r"^\*{0,2}status\*{0,2}\s*:\s*.*fail", re.IGNORECASE)


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _safe_leaf(state: dict) -> str:
    active = state.get("active")
    if not isinstance(active, list) or not active:
        return ""
    leaf = active[-1]
    if not isinstance(leaf, str):
        return ""
    leaf = leaf.strip()
    if not leaf or "/" in leaf or "\\" in leaf or ".." in leaf:
        return ""
    return leaf


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _archive_note(note: Path, archive_dir: Path) -> None:
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / note.name
    if dest.exists():
        dest = archive_dir / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _merge_note_file(note: Path, journal: Path, archive_dir: Path, heading: str) -> None:
    body = read_text(note)
    _append(
        journal,
        f"\n### {heading}\n\n{body.rstrip()}\n\n",
    )
    _archive_note(note, archive_dir)


def _status_failed(note: Path) -> bool:
    for line in read_text(note).splitlines():
        if STATUS_FAIL_RE.match(line.strip()):
            return True
    return False


def _deadline_passed(deadline: str) -> bool:
    if not deadline or not isinstance(deadline, str):
        return False
    raw = deadline.strip()
    if not raw:
        return False
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        due = datetime.fromisoformat(raw)
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > due
    except ValueError:
        return False


def _acquire_lock(lock: Path, attempts: int = 10) -> bool:
    for _ in range(attempts):
        try:
            lock.mkdir()
            return True
        except FileExistsError:
            time.sleep(1)
    return False


def _release_lock(lock: Path) -> None:
    try:
        lock.rmdir()
    except OSError:
        pass


def _candidate_note_dirs(root: Path) -> list[Path]:
    base = root / "journals" / "work-items"
    if not base.is_dir():
        return []
    found: list[Path] = []
    for path in base.glob("*/agent-notes"):
        if not path.is_dir():
            continue
        wid = path.parent.name
        if wid in {"_TEMPLATE", "_template"}:
            continue
        found.append(path)
    return found


def process_work_item(root: Path, notes_dir: Path) -> bool:
    wid = notes_dir.parent.name
    state_path = notes_dir.parent / "state.json"
    if not state_path.is_file():
        _log(f"no branch map for {wid} - skip")
        return False
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        _log(f"invalid branch map for {wid} - skip")
        return False
    leaf = _safe_leaf(state if isinstance(state, dict) else {})
    journal = notes_dir.parent / "nodes" / f"{leaf}.md"
    if not leaf or not journal.is_file():
        _log(f"no active leaf for {wid} - skip")
        return False

    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {wid} - skip")
        return False

    did_merge = False
    archive = notes_dir / "merged"
    session_dir = root / "work-items" / wid
    ts = _now()
    try:
        tasks_dir = notes_dir / "tasks"
        if tasks_dir.is_dir():
            for task_dir in sorted(p for p in tasks_dir.iterdir() if p.is_dir()):
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
                if not isinstance(manifest, dict):
                    continue
                task_name = str(manifest.get("task") or "unnamed task")
                deadline = str(manifest.get("deadline") or "")
                subtasks = manifest.get("subtasks") or []
                if not isinstance(subtasks, list):
                    subtasks = []
                total = 0
                present = 0
                failed = 0
                missing_list: list[str] = []
                failed_list: list[str] = []
                for st in subtasks:
                    if not isinstance(st, str) or not st.strip():
                        continue
                    total += 1
                    nf = task_dir / f"{st.strip()}.md"
                    if nf.is_file():
                        present += 1
                        if _status_failed(nf):
                            failed += 1
                            failed_list.append(st.strip())
                    else:
                        missing_list.append(st.strip())

                if present < total:
                    if (
                        _deadline_passed(deadline)
                        and not (task_dir / ".stall-warned").is_file()
                    ):
                        _append(
                            journal,
                            (
                                f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                                f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                                f"Never reported (no success or failure note): "
                                f"{' '.join(missing_list) or 'none'}\n\n"
                                "**Blockers:** operator action needed - a subtask agent appears "
                                "to have died without reporting. Re-dispatch the missing "
                                "subtask(s) or investigate.\n"
                            ),
                        )
                        session_dir.mkdir(parents=True, exist_ok=True)
                        (session_dir / "NEEDS-ATTENTION.md").write_text(
                            f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing_list)}\n",
                            encoding="utf-8",
                        )
                        (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                        _log(f"escalated STALLED task '{task_name}'")
                        did_merge = True
                    else:
                        _log(
                            f"task '{task_name}' not terminal ({present}/{total} reported) - waiting"
                        )
                    continue

                if failed > 0:
                    header = (
                        f"## △ Background Task PARTIAL: {task_name} - "
                        f"{failed} of {total} subtask(s) FAILED (merged {ts})"
                    )
                    status_note = (
                        f"{failed} subtask(s) failed after their retry budget: "
                        f"**{' '.join(failed_list)}**. Successful work below is still captured. "
                        "**Blockers:** operator must review the failed subtask(s) and decide "
                        "to re-dispatch or accept. See NEEDS-ATTENTION.md."
                    )
                else:
                    header = f"## Background Task Complete: {task_name} (merged {ts})"
                    status_note = (
                        f"All {total} subtasks succeeded. Fold into the proper journal "
                        "sections (Artifacts, Resolved Q&A, Next action) via journal-keeper."
                    )
                _append(journal, f"\n{header}\n\n{status_note}\n")
                task_archive = archive / task_dir.name
                for st in subtasks:
                    if not isinstance(st, str) or not st.strip():
                        continue
                    note = task_dir / f"{st.strip()}.md"
                    if note.is_file():
                        _merge_note_file(note, journal, task_archive, f"subtask: {st.strip()}")
                if manifest_path.is_file():
                    task_archive.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(manifest_path, task_archive / "manifest.json")
                (task_dir / ".merged").write_text("", encoding="utf-8")
                if failed > 0:
                    session_dir.mkdir(parents=True, exist_ok=True)
                    (session_dir / "NEEDS-ATTENTION.md").write_text(
                        f"PARTIAL task '{task_name}' at {ts}: {failed}/{total} FAILED "
                        f"({' '.join(failed_list)})\n",
                        encoding="utf-8",
                    )
                    _log(f"merged PARTIAL task '{task_name}'")
                else:
                    _log(f"merged shared task '{task_name}' into {journal}")
                did_merge = True

        loose = []
        for note in sorted(notes_dir.glob("*.md")):
            if note.name.lower() == "readme.md":
                continue
            loose.append(note)
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
                _merge_note_file(note, journal, archive, note.stem)
            _log(f"merged loose notes into {journal}")
            did_merge = True
    finally:
        _release_lock(lock)

    if did_merge:
        from journal_snapshot import snapshot_work_item

        snapshot_work_item(root, wid)
    return did_merge


def merge_all(root: Path | None = None) -> int:
    root = root or Path.cwd()
    for notes_dir in _candidate_note_dirs(root):
        try:
            process_work_item(root, notes_dir)
        except Exception as exc:  # noqa: BLE001 - stop hooks must never raise
            _log(f"error processing {notes_dir}: {exc}")
    return 0


def main() -> int:
    return merge_all(Path.cwd())


if __name__ == "__main__":
    raise SystemExit(main())
