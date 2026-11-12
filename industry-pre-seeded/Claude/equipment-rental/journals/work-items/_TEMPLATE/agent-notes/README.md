# Background agent notes

Background agents write one file here. The stop hook merges them into the active leaf node under `../nodes/` and archives processed files under `merged/`.

## Loose notes

Create `<label>.md` directly in this folder (not in `tasks/`). Merged on the next Stop/SubagentStop.

Suggested fields:

```markdown
**Status:** ok
**Summary:** what the agent did

(details)
```

## Shared tasks

Use `tasks/<task-id>/`:

- `manifest.json` — `{ "task": "...", "subtasks": ["a", "b"], "deadline": "optional ISO-8601" }`
- `<subtask>.md` — one file per subtask when that agent finishes (success or give-up)

A shared task merges only when every listed subtask has a note. A note whose Status line says failed marks the task partial. A task past its deadline is escalated once into `work-items/<id>/NEEDS-ATTENTION.md`.

Do not edit `README.md` as a note; it is ignored by the merger.
