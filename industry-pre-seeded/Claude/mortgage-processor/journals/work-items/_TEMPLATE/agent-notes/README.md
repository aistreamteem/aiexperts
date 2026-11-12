# Agent notes

Background agents write here. The stop hook merges ready notes into the active leaf node under `../nodes/`.

## Loose notes

Drop a single markdown file in this folder (`label.md`). Do not name it `README.md`. On the next stop/SubagentStop merge it is appended to the active node and moved to `merged/`.

Suggested fields:

```markdown
**Status:** ok
**Summary:** what the agent did

Details…
```

## Shared tasks

Use `tasks/<task-id>/`:

- `manifest.json` — `{ "task": "…", "subtasks": ["a", "b"], "deadline": "optional ISO-8601" }`
- One `<subtask>.md` per subtask when that subtask finishes (success or give-up)
- A note whose `**Status:**` line contains `fail` marks the task partial

The merge runs only when every listed subtask has a note (or the deadline has passed once for stall escalation). After a full merge, `.merged` is written and files move under `merged/<task-id>/`.
