"""Merge background-agent notes into the active journal leaf node.

Notes live under journals/work-items/<id>/agent-notes/.
Loose notes merge immediately; shared tasks merge when every subtask has a note.
Always exits 0.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import field, read_text  # noqa: E402


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _active_leaf(root: Path, wid: str) -> Path | None:
    state_path = root / "journals" / "work-items" / wid / "state.json"
    if not state_path.is_file():
        _log(f"no branch map for {wid} - skip")
        return None
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        _log(f"invalid branch map for {wid} - skip")
        return None
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        _log(f"no active leaf for {wid} - skip")
        return None
    leaf = active[-1]
    if not isinstance(leaf, str) or not leaf.strip():
        return None
    if "/" in leaf or "\\" in leaf or ".." in leaf:
        return None
    note = root / "journals" / "work-items" / wid / "nodes" / f"{leaf.strip()}.md"
    if not note.is_file():
        _log(f"no active leaf for {wid} - skip")
        return None
    return note


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


def _append_note(journal: Path, heading: str, body: str) -> None:
    with journal.open("a", encoding="utf-8") as fh:
        fh.write("\n")
        fh.write(f"### {heading}\n\n")
        fh.write(body.rstrip() + "\n\n")


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    try:
        note.replace(dest)
    except OSError:
        shutil.move(str(note), str(dest))


def _note_failed(text: str) -> bool:
    status = field(text, "Status").lower()
    return "fail" in status


def _process_shared_task(
    task_dir: Path,
    journal: Path,
    archive_root: Path,
    session_dir: Path,
    ts: str,
) -> bool:
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
    deadline = str(manifest.get("deadline") or "").strip()
    subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
    total = 0
    present = 0
    failed = 0
    missing: list[str] = []
    failed_list: list[str] = []
    for raw in subtasks:
        st = str(raw).strip()
        if not st:
            continue
        total += 1
        nf = task_dir / f"{st}.md"
        if nf.is_file():
            present += 1
            if _note_failed(read_text(nf)):
                failed += 1
                failed_list.append(st)
        else:
            missing.append(st)
    if total == 0:
        return False
    if present < total:
        stalled = False
        if deadline:
            try:
                # Accept Z or offset; treat naive as UTC.
                dl = deadline.replace("Z", "+00:00")
                dl_dt = datetime.fromisoformat(dl)
                if dl_dt.tzinfo is None:
                    dl_dt = dl_dt.replace(tzinfo=timezone.utc)
                stalled = datetime.now(timezone.utc) > dl_dt
            except ValueError:
                stalled = False
        warn = task_dir / ".stall-warned"
        if stalled and not warn.is_file():
            with journal.open("a", encoding="utf-8") as fh:
                fh.write("\n")
                fh.write(f"## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n")
                fh.write(
                    f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                )
                fh.write(
                    f"Never reported (no success or failure note): "
                    f"{' '.join(missing) if missing else 'none'}\n\n"
                )
                fh.write(
                    "**Blockers:** operator action needed - a subtask agent appears to have "
                    "died without reporting. Re-dispatch the missing subtask(s) or investigate.\n"
                )
            (session_dir / "NEEDS-ATTENTION.md").write_text(
                f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                encoding="utf-8",
            )
            warn.write_text("", encoding="utf-8")
            _log(f"escalated STALLED task '{task_name}' (missing: {' '.join(missing)})")
            return True
        _log(f"task '{task_name}' not terminal ({present}/{total} reported) - waiting")
        return False

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
    with journal.open("a", encoding="utf-8") as fh:
        fh.write("\n")
        fh.write(header + "\n\n")
        fh.write(status_note + "\n")
    archive = archive_root / task_dir.name
    for raw in subtasks:
        st = str(raw).strip()
        if not st:
            continue
        note = task_dir / f"{st}.md"
        if note.is_file():
            _append_note(journal, f"subtask: {st}", read_text(note))
            _archive(note, archive)
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
    return True


def process_work_item(root: Path, wid: str) -> bool:
    notes_dir = root / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        return False
    journal = _active_leaf(root, wid)
    if journal is None:
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {wid} (another merge in progress) - skip")
        return False
    did_merge = False
    ts = _now()
    archive = notes_dir / "merged"
    session_dir = root / "work-items" / wid
    try:
        tasks = notes_dir / "tasks"
        if tasks.is_dir():
            for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
                if _process_shared_task(task_dir, journal, archive, session_dir, ts):
                    did_merge = True
        loose = []
        for note in sorted(notes_dir.glob("*.md")):
            if note.name.lower() == "readme.md":
                continue
            loose.append(note)
        if loose:
            with journal.open("a", encoding="utf-8") as fh:
                fh.write("\n")
                fh.write(f"## Background Agent Notes (merged {ts})\n\n")
                fh.write(
                    "Consolidated from background agents. Fold into the proper "
                    "journal sections via journal-keeper.\n"
                )
            for note in loose:
                _append_note(journal, note.stem, read_text(note))
                _archive(note, archive)
            _log(f"merged loose notes into {journal}")
            did_merge = True
    finally:
        _release_lock(lock)
    return did_merge


def discover_work_ids(root: Path) -> list[str]:
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
    merged_any = False
    for wid in discover_work_ids(root):
        if process_work_item(root, wid):
            merged_any = True
            try:
                from journal_snapshot import snapshot_work_item

                snapshot_work_item(root, wid)
            except Exception as exc:  # noqa: BLE001 - never block stop hooks
                _log(f"post-journal-update failed for {wid}: {exc}")
    return 0 if True else int(merged_any)


if __name__ == "__main__":
    raise SystemExit(main())
