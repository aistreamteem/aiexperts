# Agent notes

Background agents write one Markdown file here (loose notes) or under `tasks/<task-id>/` (shared tasks with `manifest.json`).

The stop hook `on_stop.py` merges ready notes into the **active leaf** under `../nodes/`, then archives them in `merged/`.

## Loose note

`label.md` — free-form completion note. Merged on the next stop.

## Shared task

`tasks/<task-id>/manifest.json`:

```json
{ "task": "short name", "subtasks": ["a", "b"], "deadline": "optional ISO-8601" }
```

Each subtask agent writes `tasks/<task-id>/<subtask>.md`. Merge runs only when every listed subtask file exists. A `**Status:** ... fail` line marks that subtask failed (task merges as partial).
