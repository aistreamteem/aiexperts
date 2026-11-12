# Background agent notes

Background agents write one markdown note here. The stop hook merges them into the active leaf node under `../nodes/`.

## Loose notes

Drop `<label>.md` directly in this folder. Merged on the next stop/subagentStop.

Suggested fields:

```markdown
**Status:** done | failed
**Summary:** one line

(details)
```

## Shared tasks

Use `tasks/<task-id>/`:

- `manifest.json` — `{ "task": "...", "subtasks": ["a", "b"], "deadline": "optional ISO-8601" }`
- one `<subtask>.md` per agent (success or give-up)

A shared task merges only when every listed subtask has a note. A note whose Status line contains `fail` marks the task partial. Past-deadline tasks with missing notes escalate once via `work-items/<id>/NEEDS-ATTENTION.md`.

Processed notes move to `merged/`. Do not hand-edit `merged/` or `.merged` markers.
