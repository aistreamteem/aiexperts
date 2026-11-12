"""Cursor preToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _context(stdout: str) -> str:
    payload = json.loads(stdout)
    text = payload.get("additional_context") or ""
    nested = (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""
    _assert(bool(text), "additional_context missing")
    _assert(nested == text, "nested additionalContext drifted")
    _assert(payload.get("continue") is True, "continue was not true")
    return text


def _fill_template(text: str, values: dict[str, str]) -> str:
    out = text
    for key, value in values.items():
        # Preserve bolded field labels from the real templates.
        needle = f"**{key}:**"
        if needle in out:
            lines = []
            for line in out.splitlines():
                if line.strip().startswith(needle):
                    lines.append(f"**{key}:** {value}")
                else:
                    lines.append(line)
            out = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
        else:
            out = out.replace(f"{key}:", f"{key}: {value}", 1)
    return out


def _run_hook(workspace: Path, payload: dict) -> subprocess.CompletedProcess[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_journal_context.py"
    return subprocess.run(
        [sys.executable, str(hook)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
        wi_src = ROOT / "journals" / "work-items" / "_TEMPLATE"
        wi = tmp / "journals" / "work-items" / "WID-1"
        shutil.copytree(wi_src, wi)
        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)

        expert = tmp / "journals" / "expert" / "progress.md"
        expert.write_text(
            _fill_template(expert.read_text(encoding="utf-8"), {"Current work item": "WID-1"}),
            encoding="utf-8",
        )
        flat = wi / "progress.md"
        flat.write_text(
            _fill_template(
                flat.read_text(encoding="utf-8"),
                {"Completion status": "in progress", "Work item record": "work-items/WID-1/"},
            ),
            encoding="utf-8",
        )
        (wi / "state.json").write_text(
            json.dumps(
                {
                    "active": ["work-item", "intake"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []},
                        "intake": {"parent": "work-item", "status": "open", "history": []},
                        "pack": {"parent": "work-item", "status": "open", "history": []},
                    },
                }
            ),
            encoding="utf-8",
        )
        (wi / "nodes" / "work-item.md").write_text(
            "# work-item\n\n**Next action:** run intake\n", encoding="utf-8"
        )
        (wi / "nodes" / "intake.md").write_text("ACTIVE_BRANCH_NOTE\n", encoding="utf-8")
        (wi / "nodes" / "pack.md").write_text("INACTIVE_BRANCH_NOTE\n", encoding="utf-8")

        # No pointer files: work item comes only from the expert journal line.
        loaded = _run_hook(
            tmp, {"tool_name": "Bash", "tool_input": {"command": "echo hi"}}
        )
        _assert(loaded.returncode == 0, loaded.stderr or "hook failed")
        body = _context(loaded.stdout)
        _assert("Current work item" in body or "WID-1" in body, "expert journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        reading = _run_hook(
            tmp,
            {
                "tool_name": "Read",
                "tool_input": {"file_path": "journals/work-items/WID-1/nodes/intake.md"},
            },
        )
        read_body = _context(reading.stdout)
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")

        flat.write_text(
            _fill_template(
                flat.read_text(encoding="utf-8"),
                {"Completion status": "done"},
            ),
            encoding="utf-8",
        )
        done = _run_hook(
            tmp, {"tool_name": "Bash", "tool_input": {"command": "echo hi"}}
        )
        done_body = _context(done.stdout)
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        print("cursor journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
