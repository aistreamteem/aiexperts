# Background agent notes

Background agents write one note file here. The stop hook merges them into the
active leaf node under `journals/work-items/<id>/nodes/`, then archives them
under `merged/`.

## Loose notes

Drop a single markdown file in this folder (not named `README.md`):

```markdown
**Status:** done
**Summary:** what the agent finished

Details...
```

## Shared tasks

Use `tasks/<task-id>/`:

- `manifest.json` — `{ "task": "...", "subtasks": ["a", "b"], "deadline": "..." }`
- one `<subtask>.md` per subtask (success or failure)
- `.merged` is written by the hook after a successful merge

Do not write notes to `work-items/<id>/journal/progress.md`.
