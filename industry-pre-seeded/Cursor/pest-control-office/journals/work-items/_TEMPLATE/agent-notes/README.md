# Background agent notes

Drop notes here. The stop / subagentStop hook merges them into the **active leaf** node under `../nodes/`.

## Loose note

Create `journals/work-items/<id>/agent-notes/<label>.md` with free-form markdown. Optional:

```markdown
**Status:** ok
```

Merged on the next stop hook fire into `nodes/<active-leaf>.md`, then moved to `merged/`.

## Shared task

Create `journals/work-items/<id>/agent-notes/tasks/<task-id>/`:

- `manifest.json` — `{ "task": "...", "subtasks": ["a", "b"], "deadline": "optional-ISO-8601" }`
- `<subtask>.md` — one file per subtask (success or give-up)

A shared task merges only when every listed subtask has a note. A note whose Status line says failed marks the task partial and writes `work-items/<id>/NEEDS-ATTENTION.md`. A task past its deadline is escalated once.
