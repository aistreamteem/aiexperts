# Agent notes

Background agents write notes here. The stop hook merges them into the **active leaf** node under `../nodes/`, then archives processed files under `merged/`.

## Loose note

Create `journals/work-items/<id>/agent-notes/<label>.md` with the note body. Optional:

```markdown
**Status:** ok
```

A `Status` line containing `fail` marks a give-up for shared tasks.

## Shared task

Create `tasks/<task-id>/manifest.json`:

```json
{
  "task": "short description",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T00:00:00+00:00"
}
```

Each subtask agent writes `tasks/<task-id>/<subtask>.md`. The merge runs only when every listed subtask has a note (or after the optional deadline, once, as a stall escalation).
