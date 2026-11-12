# Background agent notes

Background agents write here. The stop hook merges ready notes into the active leaf node under `../nodes/`, then archives them under `merged/`.

## Loose notes

Drop a single markdown file in this folder (`label.md`). It merges on the next stop/subagentStop.

Suggested fields:

```markdown
**Status:** ok
**Summary:** what the agent finished

Notes...
```

Do not name a loose note `README.md`.

## Shared tasks

For work split across several agents, use `tasks/<task-id>/`:

- `manifest.json` — `{ "task": "...", "subtasks": ["a", "b"], "deadline": "optional ISO-8601" }`
- one `<subtask>.md` per agent (success or failure)

The task merges only when every listed subtask has a note. A note whose `Status` contains `fail` marks the task partial and writes `work-items/<id>/NEEDS-ATTENTION.md`. A task past its deadline is escalated once.
