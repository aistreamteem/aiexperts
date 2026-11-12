# Background agent notes

Background agents write notes here. The stop hook merges them into the active leaf node under `../nodes/`.

## Loose notes

Drop a single markdown file in this folder (`<label>.md`). On the next stop/SubagentStop, it is appended to the active node and moved to `merged/`.

Suggested fields:

```markdown
**Status:** ok
**Summary:** what finished

Details…
```

## Shared tasks

Use `tasks/<task-id>/`:

- `manifest.json` — `{ "task": "...", "subtasks": ["a", "b"], "deadline": "optional ISO-8601" }`
- one `<subtask>.md` per subtask when that subtask finishes (success or give-up)

A shared task merges only when every listed subtask has a note. A note whose **Status** contains `fail` marks the task partial and writes `work-items/<id>/NEEDS-ATTENTION.md`. Past-deadline missing notes escalate once.

Do not edit `README.md` as a note; it is documentation only.
