# Background agent notes

Background agents write notes here. The stop hook merges them into the active leaf node under `../nodes/`.

## Loose notes

Drop a single markdown file in this folder (not named `README.md`). It is merged on the next stop / subagentStop.

Suggested fields:

```markdown
**Status:** done
**Summary:** what the agent finished

(details)
```

## Shared tasks

Use `tasks/<task-id>/`:

- `manifest.json` — `{ "task": "...", "subtasks": ["a", "b"], "deadline": "optional ISO-8601" }`
- one `<subtask>.md` per subtask when that agent finishes (success or give-up)

A shared task merges only when every listed subtask has a note. A note whose Status line contains `fail` marks the task partial. A task past its deadline is escalated once into `NEEDS-ATTENTION.md` on the Work Item.

Processed notes move to `merged/`.
