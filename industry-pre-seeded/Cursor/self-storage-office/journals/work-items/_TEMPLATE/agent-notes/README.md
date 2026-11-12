# Background agent notes

Drop loose notes here as `<label>.md`. Shared tasks go under `tasks/<task-id>/` with a `manifest.json` listing `subtasks` and one `<subtask>.md` per agent.

The stop hook merges notes into the active leaf node under `../nodes/` (from `state.json`). Processed notes move to `merged/`.

Do not write journal fields here; use journal-keeper on the node or flat progress file.
