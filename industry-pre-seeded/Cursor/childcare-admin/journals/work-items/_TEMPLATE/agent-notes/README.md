# Background agent notes

Background agents write one markdown file here. The stop hook merges them into the active node under `../nodes/`.

## Loose note

Create `journals/work-items/<id>/agent-notes/<label>.md` with the note body. Optional:

```markdown
**Status:** done
```

Use `**Status:** failed` when the agent gave up after retries.

## Shared task

Create `tasks/<task-id>/manifest.json`:

```json
{
  "task": "short name",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T00:00:00+00:00"
}
```

Each subtask agent writes `tasks/<task-id>/<subtask>.md`. The merge runs only when every listed subtask has a note. Processed notes move to `merged/`.
