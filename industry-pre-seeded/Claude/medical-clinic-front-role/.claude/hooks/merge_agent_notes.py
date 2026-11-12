"""Merge background-agent notes into the active journal leaf node.

Notes live under journals/work-items/<id>/agent-notes/.
Merge target is the active leaf node from state.json (stdlib JSON; no jq).
Always exits 0.
"""

from __future__ import annotations

import json
import re
import shutil
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
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _active_leaf(state_path: Path) -> str:
    if not state_path.is_file():
        return ""
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return ""
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return ""
    leaf = active[-1]
    return leaf.strip() if isinstance(leaf, str) else ""


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


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text)


def _archive(note: Path, archive: Path) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    dest = archive / note.name
    if dest.exists():
        dest = archive / f"{note.stem}-{int(time.time())}{note.suffix}"
    shutil.move(str(note), str(dest))


def _merge_note(note: Path, journal: Path, archive: Path, heading: str) -> None:
    body = read_text(note)
    _append(
        journal,
        f"\n### {heading}\n\n{body.rstrip()}\n\n",
    )
    _archive(note, archive)


def _process_shared_tasks(
    notes_dir: Path, journal: Path, archive: Path, needs_attention: Path, ts: str
) -> bool:
    tasks = notes_dir / "tasks"
    if not tasks.is_dir():
        return False
    did = False
    for task_dir in sorted(p for p in tasks.iterdir() if p.is_dir()):
        if (task_dir / ".merged").exists():
            continue
        manifest_path = task_dir / "manifest.json"
        if not manifest_path.is_file():
            log(f"task {task_dir.name} has no manifest - skip")
            continue
        try:
            manifest = json.loads(read_text(manifest_path))
        except json.JSONDecodeError:
            log(f"task {task_dir.name} has invalid manifest - skip")
            continue
        task_name = str(manifest.get("task") or "unnamed task")
        deadline = str(manifest.get("deadline") or "").strip()
        subtasks = manifest.get("subtasks") if isinstance(manifest.get("subtasks"), list) else []
        missing: list[str] = []
        failed: list[str] = []
        present = 0
        for raw in subtasks:
            if not isinstance(raw, str) or not raw.strip():
                continue
            st = raw.strip()
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                present += 1
                if STATUS_FAIL.search(read_text(nf)):
                    failed.append(st)
            else:
                missing.append(st)
        total = len([s for s in subtasks if isinstance(s, str) and s.strip()])
        if present < total:
            stalled = False
            if deadline:
                try:
                    # Accept ISO-8601; treat naive as local
                    dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
                    now = datetime.now(dl.tzinfo) if dl.tzinfo else datetime.now()
                    stalled = now > dl.replace(tzinfo=None) if dl.tzinfo is None else now > dl
                except ValueError:
                    stalled = False
            if stalled and not (task_dir / ".stall-warned").exists():
                _append(
                    journal,
                    (
                        f"\n## △ ATTENTION - Background task STALLED: {task_name} ({ts})\n\n"
                        f"Past deadline ({deadline}) with {present}/{total} subtasks reported.\n"
                        f"Never reported (no success or failure note): "
                        f"{' '.join(missing) if missing else 'none'}\n\n"
                        "**Blockers:** operator action needed - a subtask agent appears to have "
                        "died without reporting. Re-dispatch the missing subtask(s) or investigate.\n"
                    ),
                )
                needs_attention.write_text(
                    f"STALLED task '{task_name}' at {ts}: missing {' '.join(missing)}\n",
                    encoding="utf-8",
                )
                (task_dir / ".stall-warned").write_text("", encoding="utf-8")
                log(f"escalated STALLED task '{task_name}' (missing: {' '.join(missing)})")
                did = True
            else:
                log(f"task '{task_name}' not terminal ({present}/{total} reported) - waiting")
            continue

        if failed:
            header = (
                f"## △ Background Task PARTIAL: {task_name} - {len(failed)} of "
                f"{total} subtask(s) FAILED (merged {ts})"
            )
            status_note = (
                f"{len(failed)} subtask(s) failed after their retry budget: "
                f"**{' '.join(failed)}**. Successful work below is still captured. "
                "**Blockers:** operator must review the failed subtask(s) and decide to "
                "re-dispatch or accept. See NEEDS-ATTENTION.md."
            )
        else:
            header = f"## Background Task Complete: {task_name} (merged {ts})"
            status_note = (
                f"All {total} subtasks succeeded. Fold into the proper journal sections "
                "(Artifacts, Resolved Q&A, Next action) via journal-keeper."
            )
        _append(journal, f"\n{header}\n\n{status_note}\n")
        task_archive = archive / task_dir.name
        for raw in subtasks:
            if not isinstance(raw, str) or not raw.strip():
                continue
            st = raw.strip()
            nf = task_dir / f"{st}.md"
            if nf.is_file():
                _merge_note(nf, journal, task_archive, f"subtask: {st}")
        try:
            shutil.copy2(manifest_path, task_archive / "manifest.json")
        except OSError:
            pass
        (task_dir / ".merged").write_text("", encoding="utf-8")
        if failed:
            needs_attention.write_text(
                f"PARTIAL task '{task_name}' at {ts}: {len(failed)}/{total} FAILED "
                f"({' '.join(failed)})\n",
                encoding="utf-8",
            )
            log(f"merged PARTIAL task '{task_name}' - {len(failed)}/{total} failed")
        else:
            log(f"merged shared task '{task_name}' into {journal}")
        did = True
    return did


def _process_loose(notes_dir: Path, journal: Path, archive: Path, ts: str) -> bool:
    loose = [
        p
        for p in notes_dir.glob("*.md")
        if p.is_file() and p.name.lower() != "readme.md"
    ]
    if not loose:
        return False
    _append(
        journal,
        (
            f"\n## Background Agent Notes (merged {ts})\n\n"
            "Consolidated from background agents. Fold into the proper journal "
            "sections via journal-keeper.\n"
        ),
    )
    for note in sorted(loose):
        _merge_note(note, journal, archive, note.stem)
    log(f"merged loose notes into {journal}")
    return True


def process_work_item(root: Path, work_id: str) -> bool:
    if not work_id or work_id.startswith("_"):
        return False
    notes_dir = root / "journals" / "work-items" / work_id / "agent-notes"
    if not notes_dir.is_dir():
        return False
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    leaf = _active_leaf(state_path)
    if not leaf:
        log(f"no branch map for {work_id} - skip")
        return False
    journal = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf}.md"
    if not journal.is_file():
        log(f"no active leaf for {work_id} - skip")
        return False
    lock = notes_dir / ".merge.lock"
    if not _acquire_lock(lock):
        log(f"could not acquire lock for {work_id} - skip")
        return False
    try:
        ts = _now()
        archive = notes_dir / "merged"
        needs = root / "work-items" / work_id / "NEEDS-ATTENTION.md"
        did = False
        did |= _process_shared_tasks(notes_dir, journal, archive, needs, ts)
        did |= _process_loose(notes_dir, journal, archive, ts)
        return did
    finally:
        _release_lock(lock)


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


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = ROOT
    ids = [a for a in argv if a and not a.startswith("-")]
    if not ids:
        ids = discover_work_ids(root)
    merged_any = False
    for wid in ids:
        # Allow passing work-items/<id> paths
        name = Path(wid).name
        if process_work_item(root, name):
            merged_any = True
            try:
                from journal_snapshot import snapshot_work_item

                snapshot_work_item(root, name)
            except Exception as exc:  # noqa: BLE001
                log(f"journal snapshot failed for {name}: {exc}")
    _ = merged_any
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
