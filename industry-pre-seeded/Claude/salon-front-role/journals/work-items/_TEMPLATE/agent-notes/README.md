# agent-notes

Drop folder for background agents. Agents never edit the journal directly. The stop and subagentStop hooks (`.claude/hooks/on_stop.py`, which runs `.claude/hooks/merge_agent_notes.py`) append what they find here to the **active node file** (`journals/work-items/<id>/nodes/<leaf>.md`, the last entry of `active` in `state.json`), archive the originals under `merged/`, then commit an audit snapshot. The merge is lock-guarded (`.merge.lock`) and idempotent.

## Loose note (one agent, no shared task)

Write `agent-notes/<label>.md`. It is merged on the next hook fire. Suggested content:

```markdown
**Status:** done
**Artifacts:** paths written
**Findings:** what the next step needs to know
```

`README.md` is never merged.

## Shared task (several agents dividing one task)

Create `agent-notes/tasks/<task-id>/manifest.json`:

```json
{
  "task": "Short task name",
  "subtasks": ["a", "b", "c"],
  "deadline": "2026-11-10T09:00:00-05:00"
}
```

`deadline` is optional (ISO-8601). Each subtask agent writes `agent-notes/tasks/<task-id>/<subtask>.md` when it finishes, on success or when it gives up.

- The task merges only when every subtask in the manifest has a note. Until then nothing is merged.
- A note whose `**Status:**` line contains "fail" makes the merge **partial**. The merge still happens and `work-items/<id>/NEEDS-ATTENTION.md` is written.
- If the deadline passes with notes still missing, the hook escalates once (`.stall-warned` marker, a section in the node file, and `NEEDS-ATTENTION.md`). It does not mark the task merged, so late notes still merge normally.
- After a merge the task folder holds a `.merged` marker and the notes move to `merged/<task-id>/`.
