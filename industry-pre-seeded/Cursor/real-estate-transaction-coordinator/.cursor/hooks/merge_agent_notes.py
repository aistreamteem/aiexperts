"""Merge background-agent notes into the active journal node.

Notes live under journals/work-items/<id>/agent-notes/.
Merge target is the active leaf node from state.json (stdlib JSON; no jq).
Always exits 0.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, journals_base, read_text


def _log(msg: str) -> None:
    print(f"[merge-agent-notes] {msg}", file=sys.stderr)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _status_failed(text: str) -> bool:
    for line in text.splitlines():
        lower = line.lower()
        if "status" in lower and "fail" in lower:
            return True
    return False


class _Lock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.held = False

    def acquire(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(10):
            try:
                self.path.mkdir()
                self.held = True
                return True
            except FileExistsError:
                time.sleep(1)
        return False

    def release(self) -> None:
        if self.held:
            try:
                self.path.rmdir()
            except OSError:
                pass
            self.held = False


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


def _load_state(path: Path) -> dict:
    raw = read_text(path)
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _past_deadline(deadline: str) -> bool:
    if not deadline:
        return False
    try:
        # Accept Z or offset; fall back to fromisoformat with Z replaced
        cleaned = deadline.replace("Z", "+00:00")
        dl = datetime.fromisoformat(cleaned)
        if dl.tzinfo is None:
            dl = dl.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > dl
    except ValueError:
        return False


def _process_shared_tasks(
    notes_dir: Path, journal: Path, session_dir: Path, archive_root: Path, ts: str
) -> bool:
    tasks = notes_dir / "tasks"
    if not tasks.is_dir():
        return False
    did = False
    for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
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
        missing: list[str] = []
        failed_list: list[str] = []
        for st in subtasks:
            if not isinstance(st, str) or not st.strip():
                continue
            st = st.strip()
            total += 1
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                present += 1
                if _status_failed(read_text(nf)):
                    failed += 1
                    failed_list.append(st)
            else:
                missing.append(st)
        if present < total:
            if _past_deadline(deadline) and not (task_dir / ".stall-warned").is_file():
                with journal.open("a", encoding="utf-8") as fh:
                    fh.write("\n")
                    fh.write(f"## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n")
                    fh.write(
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                    )
                    fh.write(
                        f"Never reported (no success or failure note): "
                        f"{' '.join(missing) or 'none'}\n\n"
                    )
                    fh.write(
                        "**Blockers:** operator action needed - a subtask agent appears "
                        "to have died without reporting. Re-dispatch the missing "
                        "subtask(s) or investigate.\n"
                    )
                (session_dir / "NEEDS-ATTENTION.md").write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
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
                f"{failed} subtask(s) failed after their retry budget: "
                f"**{' '.join(failed_list)}**. Successful work below is still captured. "
                "**Blockers:** operator must review the failed subtask(s). See NEEDS-ATTENTION.md."
            )
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status_note = (
                f"All {total} subtasks succeeded. Fold into the proper journal sections "
                "via journal-keeper."
            )
        with journal.open("a", encoding="utf-8") as fh:
            fh.write("\n" + header + "\n\n" + status_note + "\n")
        task_archive = archive_root / task_dir.name
        for st in subtasks:
            if not isinstance(st, str) or not st.strip():
                continue
            st = st.strip()
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                _append_note(journal, f"subtask: {st}", read_text(nf))
                _archive(nf, task_archive)
        try:
            shutil.copy2(manifest_path, task_archive / "manifest.json")
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
        did = True
    return did


def _process_loose(notes_dir: Path, journal: Path, archive: Path, ts: str) -> bool:
    loose = []
    for note in sorted(notes_dir.glob("*.md")):
        if note.name.lower() == "readme.md":
            continue
        loose.append(note)
    if not loose:
        return False
    with journal.open("a", encoding="utf-8") as fh:
        fh.write("\n")
        fh.write(f"## Background Agent Notes (merged {ts})\n\n")
        fh.write(
            "Consolidated from background agents. Fold into the proper journal "
            "sections via journal-keeper.\n"
        )
    for note in loose:
        _append_note(journal, note.stem, read_text(note))
        _archive(note, archive)
    _log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    if work_id in {"_TEMPLATE", "_template"}:
        return False
    base = journals_base(root, work_id)
    notes_dir = base / "agent-notes"
    if not notes_dir.is_dir():
        # Also accept notes left under the legacy work-item journal agent-notes folder
        legacy = root / "work-items" / work_id / "journal" / "agent-notes"
        if legacy.is_dir():
            notes_dir = legacy
        else:
            return False
    state = _load_state(base / "state.json")
    leaf = active_leaf(state)
    if not leaf:
        _log(f"no active leaf for {work_id} - skip")
        return False
    journal = base / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        _log(f"no active leaf for {work_id} - skip")
        return False
    lock = _Lock(notes_dir / ".merge.lock")
    if not lock.acquire():
        _log(f"could not acquire lock for {work_id} - skip")
        return False
    try:
        ts = _now()
        archive = notes_dir / "merged"
        session_dir = root / "work-items" / work_id
        did = _process_shared_tasks(notes_dir, journal, session_dir, archive, ts)
        did = _process_loose(notes_dir, journal, archive, ts) or did
        return did
    finally:
        lock.release()


def discover_work_ids(root: Path) -> list[str]:
    found: set[str] = set()
    journals = root / "journals" / "work-items"
    if journals.is_dir():
        for notes in journals.glob("*/agent-notes"):
            wid = notes.parent.name
            if wid not in {"_TEMPLATE", "_template"}:
                found.add(wid)
    work_items = root / "work-items"
    if work_items.is_dir():
        for notes in work_items.glob("*/journal/agent-notes"):
            wid = notes.parent.parent.name
            if wid not in {"_TEMPLATE", "_template"}:
                found.add(wid)
    return sorted(found)


def main(argv: list[str] | None = None) -> int:
    root = Path.cwd()
    args = list(argv if argv is not None else sys.argv[1:])
    if args:
        ids = [Path(a).name for a in args]
    else:
        ids = discover_work_ids(root)
    merged_any = False
    for wid in ids:
        if process_work_item(root, wid):
            merged_any = True
            try:
                from journal_snapshot import snapshot_work_item

                snapshot_work_item(root, wid)
            except Exception as exc:  # noqa: BLE001 — never fail the stop hook
                _log(f"journal snapshot failed for {wid}: {exc}")
    return 0 if True else int(merged_any)  # always 0


if __name__ == "__main__":
    raise SystemExit(main())
