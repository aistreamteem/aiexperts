"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Loose notes merge immediately; shared tasks merge when every subtask has a note.
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import field, read_text

ROOT = Path(__file__).resolve().parents[2]
STATUS_FAIL = re.compile(r"(?im)^\s*\*{0,2}status\*{0,2}\s*:\s*.*fail")


def log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    note.replace(dest)


def _merge_note(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(
        journal,
        f"\n### {heading}\n\n{body.rstrip()}\n\n",
    )
    _archive(note, archive)


def _parse_deadline(raw: str) -> float | None:
    text = (raw or "").strip()
    if not text:
        return None
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text).timestamp()
    except ValueError:
        return None


def process_work_item(wid: str) -> bool:
    notes_dir = ROOT / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state_path = ROOT / "journals" / "work-items" / wid / "state.json"
    leaf = _active_leaf(state_path)
    if not leaf:
        log(f"no active leaf for {wid} - skip")
        return False
    journal = ROOT / "journals" / "work-items" / wid / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        log(f"no active leaf for {wid} - skip")
        return False

    lock = notes_dir / ".merge.lock"
    if not _acquire(lock):
        log(f"could not acquire lock for {wid} - skip")
        return False

    did_merge = False
    ts = _now()
    archive = notes_dir / "merged"
    session_dir = ROOT / "work-items" / wid
    try:
        tasks_dir = notes_dir / "tasks"
        if tasks_dir.is_dir():
            for task_dir in sorted(p for p in tasks_dir.iterdir() if p.is_dir()):
                if (task_dir / ".merged").exists():
                    continue
                manifest_path = task_dir / "manifest.json"
                if not manifest_path.is_file():
                    log(f"task {task_dir.name} has no manifest - skip")
                    continue
                try:
                    manifest = json.loads(read_text(manifest_path) or "{}")
                except json.JSONDecodeError:
                    log(f"task {task_dir.name} has invalid manifest - skip")
                    continue
                task_name = str(manifest.get("task") or "unnamed task")
                subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else None
                if not isinstance(subtasks, list) or not subtasks:
                    log(f"task {task_dir.name} has no subtasks - skip")
                    continue
                names = [str(s).strip() for s in subtasks if str(s).strip()]
                missing: list[str] = []
                failed: list[str] = []
                present = 0
                for name in names:
                    note = task_dir / f"{name}.md"
                    if not note.is_file():
                        missing.append(name)
                        continue
                    present += 1
                    if STATUS_FAIL.search(read_text(note) or ""):
                        failed.append(name)
                total = len(names)
                if present < total:
                    deadline = _parse_deadline(str(manifest.get("deadline") or ""))
                    stall_marker = task_dir / ".stall-warned"
                    if (
                        deadline is not None
                        and time.time() > deadline
                        and not stall_marker.exists()
                    ):
                        _append(
                            journal,
                            (
                                f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                                f"Past deadline ({manifest.get('deadline')}) with "
                                f"{present}/{total} subtasks reported.\n"
                                f"Never reported (no success or failure note): "
                                f"{' '.join(missing) or 'none'}\n\n"
                                "**Blockers:** operator action needed - a subtask agent "
                                "appears to have died without reporting. Re-dispatch the "
                                "missing subtask(s) or investigate.\n"
                            ),
                        )
                        attention = session_dir / "NEEDS-ATTENTION.md"
                        attention.parent.mkdir(parents=True, exist_ok=True)
                        attention.write_text(
                            f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                            encoding="utf-8",
                        )
                        stall_marker.write_text("", encoding="utf-8")
                        log(f"escalated STALLED task '{task_name}' (missing: {' '.join(missing)})")
                        did_merge = True
                    else:
                        log(f"task '{task_name}' not terminal ({present}/{total} reported) - waiting")
                    continue

                if failed:
                    header = (
                        f"## △ Background Task PARTIAL: {task_name} - "
                        f"{len(failed)} of {total} subtask(s) FAILED (merged {ts})"
                    )
                    status_note = (
                        f"{len(failed)} subtask(s) failed after their retry budget: "
                        f"**{' '.join(failed)}**. Successful work below is still captured. "
                        "**Blockers:** operator must review the failed subtask(s) and decide "
                        "to re-dispatch or accept. See NEEDS-ATTENTION.md."
                    )
                else:
                    header = f"## Background Task Complete: {task_name} (merged {ts})"
                    status_note = (
                        f"All {total} subtasks succeeded. Fold into the proper journal "
                        "sections via journal-keeper."
                    )
                _append(journal, f"\n{header}\n\n{status_note}\n")
                task_archive = archive / task_dir.name
                for name in names:
                    note = task_dir / f"{name}.md"
                    if note.is_file():
                        _merge_note(note, journal, task_archive, f"subtask: {name}")
                try:
                    (task_archive / "manifest.json").write_text(
                        read_text(manifest_path), encoding="utf-8"
                    )
                except OSError:
                    pass
                (task_dir / ".merged").write_text("", encoding="utf-8")
                if failed:
                    attention = session_dir / "NEEDS-ATTENTION.md"
                    attention.parent.mkdir(parents=True, exist_ok=True)
                    attention.write_text(
                        f"PARTIAL task '{task_name}' at {ts}: "
                        f"{len(failed)}/{total} FAILED ({' '.join(failed)})\n",
                        encoding="utf-8",
                    )
                    log(
                        f"merged PARTIAL task '{task_name}' - "
                        f"{len(failed)}/{total} failed ({' '.join(failed)})"
                    )
                else:
                    log(f"merged shared task '{task_name}' into {journal}")
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
                    "Consolidated from background agents. Fold into the proper "
                    "journal sections via journal-keeper.\n"
                ),
            )
            for note in loose:
                _merge_note(note, journal, archive, note.stem)
            log(f"merged loose notes into {journal}")
            did_merge = True
    finally:
        _release(lock)

    if did_merge:
        from journal_snapshot import snapshot_work_item

        snapshot_work_item(wid)
    return did_merge


def discover_work_ids() -> list[str]:
    base = ROOT / "journals" / "work-items"
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
    for wid in discover_work_ids():
        try:
            process_work_item(wid)
        except Exception as exc:  # noqa: BLE001 — stop hooks must not fail the agent
            log(f"error merging {wid}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
