"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Merged notes are archived under agent-notes/merged/.
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

ROOT = Path(__file__).resolve().parents[2]


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _active_leaf(wid: str) -> tuple[Path, str] | tuple[None, str]:
    state_path = ROOT / "journals" / "work-items" / wid / "state.json"
    if not state_path.is_file():
        return None, "no branch map"
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        return None, "bad branch map"
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return None, "no active leaf"
    leaf = active[-1]
    if not isinstance(leaf, str) or not leaf.strip():
        return None, "no active leaf"
    leaf = leaf.strip()
    if "/" in leaf or "\\" in leaf or ".." in leaf:
        return None, "invalid leaf"
    note = ROOT / "journals" / "work-items" / wid / "nodes" / f"{leaf}.md"
    if not note.is_file():
        return None, "missing leaf note"
    return note, leaf


def _acquire_lock(lock: Path, tries: int = 10) -> bool:
    for _ in range(tries):
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


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _append(target: Path, heading: str, body: str) -> None:
    block = f"\n### {heading}\n\n{body.rstrip()}\n"
    with target.open("a", encoding="utf-8") as fh:
        fh.write(block)


def _status_failed(text: str) -> bool:
    for line in text.splitlines():
        lower = line.lower()
        if "status" in lower and "fail" in lower:
            return True
    return field(text, "Status").lower().find("fail") >= 0


def _process_shared_tasks(notes_dir: Path, journal: Path, wid: str) -> bool:
    tasks = notes_dir / "tasks"
    if not tasks.is_dir():
        return False
    did = False
    archive_root = notes_dir / "merged"
    for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
        if (task_dir / ".merged").is_file():
            continue
        manifest_path = task_dir / "manifest.json"
        if not manifest_path.is_file():
            _log(f"task {task_dir.name} has no manifest - skip")
            continue
        try:
            manifest = json.loads(read_text(manifest_path) or "{}")
        except json.JSONDecodeError:
            _log(f"task {task_dir.name} bad manifest - skip")
            continue
        subtasks = manifest.get("subtasks") if isinstance(manifest, dict) else None
        if not isinstance(subtasks, list) or not subtasks:
            _log(f"task {task_dir.name} has no subtasks - skip")
            continue
        task_name = str(manifest.get("task") or "unnamed task")
        deadline = str(manifest.get("deadline") or "").strip()
        names = [str(s).strip() for s in subtasks if str(s).strip()]
        present: list[str] = []
        missing: list[str] = []
        failed: list[str] = []
        for name in names:
            nf = task_dir / f"{name}.md"
            if nf.is_file():
                present.append(name)
                if _status_failed(read_text(nf)):
                    failed.append(name)
            else:
                missing.append(name)
        if missing:
            stalled = False
            if deadline:
                try:
                    # Accept Z or offset; compare as naive UTC-ish string order when parse fails.
                    dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                    stalled = datetime.now(timezone.utc) > dl
                except ValueError:
                    stalled = False
            if stalled and not (task_dir / ".stall-warned").is_file():
                ts = _now()
                with journal.open("a", encoding="utf-8") as fh:
                    fh.write(
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {len(present)}/{len(names)} "
                        f"subtasks reported.\n"
                        f"Never reported: {', '.join(missing) or 'none'}\n\n"
                        "**Blockers:** operator action needed.\n"
                    )
                needs = ROOT / "work-items" / wid / "NEEDS-ATTENTION.md"
                needs.parent.mkdir(parents=True, exist_ok=True)
                needs.write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {', '.join(missing)}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                _log(f"escalated STALLED task '{task_name}'")
                did = True
            else:
                _log(
                    f"task '{task_name}' not terminal "
                    f"({len(present)}/{len(names)} reported) - waiting"
                )
            continue
        ts = _now()
        if failed:
            header = (
                f"## △ Background Task PARTIAL: {task_name} - "
                f"{len(failed)} of {len(names)} subtask(s) FAILED (merged {ts})"
            )
            status_note = (
                f"{len(failed)} subtask(s) failed: **{' '.join(failed)}**. "
                "See NEEDS-ATTENTION.md."
            )
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status_note = (
                f"All {len(names)} subtasks succeeded. Fold into journal sections "
                "via journal-keeper."
            )
        with journal.open("a", encoding="utf-8") as fh:
            fh.write(f"\n{header}\n\n{status_note}\n")
        archive = archive_root / task_dir.name
        for name in names:
            nf = task_dir / f"{name}.md"
            if nf.is_file():
                _append(journal, f"subtask: {name}", read_text(nf))
                _archive(nf, archive)
        try:
            shutil.copy2(manifest_path, archive / "manifest.json")
        except OSError:
            pass
        (task_dir / ".merged").write_text("", encoding="utf-8")
        if failed:
            needs = ROOT / "work-items" / wid / "NEEDS-ATTENTION.md"
            needs.parent.mkdir(parents=True, exist_ok=True)
            needs.write_text(
                f"PARTIAL task '{task_name}' at {ts}: "
                f"{len(failed)}/{len(names)} FAILED ({' '.join(failed)})\n",
                encoding="utf-8",
            )
            _log(f"merged PARTIAL task '{task_name}'")
        else:
            _log(f"merged shared task '{task_name}' into {journal}")
        did = True
    return did


def _process_loose(notes_dir: Path, journal: Path) -> bool:
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
            "Consolidated from background agents. Fold into the proper journal "
            "sections via journal-keeper.\n"
        )
    archive = notes_dir / "merged"
    for note in loose:
        _append(journal, note.stem, read_text(note))
        _archive(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(wid: str) -> bool:
    notes_dir = ROOT / "journals" / "work-items" / wid / "agent-notes"
    if not notes_dir.is_dir():
        return False
    journal, leaf = _active_leaf(wid)
    if journal is None:
        _log(f"no branch map for {wid} - skip" if leaf == "no branch map" else f"{leaf} for {wid} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        _log(f"could not acquire lock for {wid} - skip")
        return False
    try:
        did = _process_shared_tasks(notes_dir, journal, wid)
        did = _process_loose(notes_dir, journal) or did
        return did
    finally:
        _release_lock(lock)


def discover_work_ids() -> list[str]:
    found: set[str] = set()
    base = ROOT / "journals" / "work-items"
    if base.is_dir():
        for notes in base.glob("*/agent-notes"):
            wid = notes.parent.name
            if wid.startswith("_"):
                continue
            found.add(wid)
    return sorted(found)


def main() -> int:
    for wid in discover_work_ids():
        if process_work_item(wid):
            try:
                from journal_snapshot import snapshot_work_item

                snapshot_work_item(wid)
            except Exception as exc:  # noqa: BLE001
                _log(f"journal snapshot failed for {wid}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
