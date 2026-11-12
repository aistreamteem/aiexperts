"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Merge target is the active leaf node from state.json (stdlib JSON, no jq).
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import active_leaf, read_text  # noqa: E402
from journal_snapshot import snapshot_work_item  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _status_failed(text: str) -> bool:
    for line in text.splitlines():
        lower = line.lower().strip()
        if lower.startswith("**status:**") or lower.startswith("status:"):
            return "fail" in lower
    return False


def _append_note(journal: Path, heading: str, body: str) -> None:
    with journal.open("a", encoding="utf-8") as fh:
        fh.write("\n")
        fh.write(f"### {heading}\n\n")
        fh.write(body.rstrip() + "\n\n")


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _acquire_lock(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
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


def _load_state(path: Path) -> dict:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _deadline_passed(deadline: str) -> bool:
    if not deadline:
        return False
    raw = deadline.strip()
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        due = datetime.fromisoformat(raw)
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > due
    except ValueError:
        return False


def process_work_item(wid: str) -> bool:
    notes_dir = ROOT / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state_path = ROOT / "journals" / "work-items" / wid / "state.json"
    state = _load_state(state_path)
    leaf = active_leaf(state)
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

    did_merge = False
    archive = notes_dir / "merged"
    ts = _now()
    session_dir = ROOT / "work-items" / wid
    try:
        tasks_root = notes_dir / "tasks"
        if tasks_root.is_dir():
            for task_dir in sorted(p for p in tasks_root.iterdir() if p.is_dir()):
                if (task_dir / ".merged").is_file():
                    continue
                manifest_path = task_dir / "manifest.json"
                if not manifest_path.is_file():
                    _log(f"task {task_dir.name} has no manifest - skip")
                    continue
                try:
                    manifest = json.loads(read_text(manifest_path))
                except json.JSONDecodeError:
                    _log(f"task {task_dir.name} manifest invalid - skip")
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
                missing_list: list[str] = []
                failed_list: list[str] = []
                for st in subtasks:
                    if not isinstance(st, str) or not st.strip():
                        continue
                    total += 1
                    name = st.strip()
                    nf = task_dir / f"{name}.md"
                    if nf.is_file():
                        present += 1
                        if _status_failed(read_text(nf)):
                            failed += 1
                            failed_list.append(name)
                    else:
                        missing_list.append(name)
                if total == 0:
                    continue
                if present < total:
                    if _deadline_passed(deadline) and not (task_dir / ".stall-warned").is_file():
                        with journal.open("a", encoding="utf-8") as fh:
                            fh.write(
                                f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                                f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                                f"Never reported (no success or failure note): "
                                f"{' '.join(missing_list) or 'none'}\n\n"
                                "**Blockers:** operator action needed - a subtask agent appears to have "
                                "died without reporting. Re-dispatch the missing subtask(s) or investigate.\n"
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
                if failed:
                    header = (
                        f"## △ Background Task PARTIAL: {task_name} - "
                        f"{failed} of {total} subtask(s) FAILED (merged {ts})"
                    )
                    status_note = (
                        f"{failed} subtask(s) failed after their retry budget: "
                        f"**{' '.join(failed_list)}**. Successful work below is still captured. "
                        "**Blockers:** operator must review the failed subtask(s)."
                    )
                else:
                    header = f"## Background Task Complete: {task_name} (merged {ts})"
                    status_note = (
                        f"All {total} subtasks succeeded. Fold into the proper journal sections "
                        "via journal-keeper."
                    )
                with journal.open("a", encoding="utf-8") as fh:
                    fh.write(f"\n{header}\n\n{status_note}\n")
                task_archive = archive / task_dir.name
                for st in subtasks:
                    if not isinstance(st, str) or not st.strip():
                        continue
                    nf = task_dir / f"{st.strip()}.md"
                    if nf.is_file():
                        _append_note(journal, f"subtask: {st.strip()}", read_text(nf))
                        _archive(nf, task_archive)
                try:
                    shutil.copy2(manifest_path, task_archive / "manifest.json")
                except OSError:
                    pass
                (task_dir / ".merged").write_text("", encoding="utf-8")
                if failed:
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

        loose = sorted(
            p
            for p in notes_dir.glob("*.md")
            if p.is_file() and p.name.lower() != "readme.md"
        )
        if loose:
            with journal.open("a", encoding="utf-8") as fh:
                fh.write(
                    f"\n## Background Agent Notes (merged {ts})\n\n"
                    "Consolidated from background agents. Fold into the proper journal "
                    "sections via journal-keeper.\n"
                )
            for note in loose:
                _append_note(journal, note.stem, read_text(note))
                _archive(note, archive)
            _log(f"merged loose notes into {journal}")
            did_merge = True
    finally:
        _release_lock(lock)

    if did_merge:
        snapshot_work_item(ROOT, wid)
    return did_merge


def discover_work_ids() -> list[str]:
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


def main() -> int:
    os.chdir(ROOT)
    for wid in discover_work_ids():
        try:
            process_work_item(wid)
        except Exception as exc:  # noqa: BLE001 - hooks must never fail the agent
            _log(f"error merging {wid}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
