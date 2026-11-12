# Agent notes

Background agents write one markdown note here (loose) or under `tasks/<task-id>/` (shared task).

## Loose note

`<label>.md` — merged into the active leaf node on the next stop hook.

## Shared task

`tasks/<task-id>/manifest.json` with `task`, optional `deadline`, and `subtasks`.
Each subtask writes `<subtask>.md`. Merge happens only when every subtask has a note.
A note whose Status line says failed marks the task partial.

Processed notes move to `merged/`.
