# Background agent notes

Background agents write one markdown file here. The stop / subagentStop hook merges ready notes into the active leaf under `../nodes/`.

## Loose note

Drop `<label>.md` directly in this folder (not in `tasks/`). Example:

```markdown
**Status:** done

What the agent finished, artifacts touched, and any open question for the main session.
```

## Shared task

Create `tasks/<task-id>/manifest.json`:

```json
{
  "task": "short description",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T18:00:00-05:00"
}
```

Each subtask agent writes `tasks/<task-id>/<subtask>.md`. The merge runs only when every listed subtask has a note. A note whose **Status:** line contains `fail` marks the task partial. Processed notes move to `merged/`.
