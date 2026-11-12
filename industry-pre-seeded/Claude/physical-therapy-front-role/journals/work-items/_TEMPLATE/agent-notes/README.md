# Background-agent notes

Drop loose notes here as `<label>.md`. Shared tasks go under `tasks/<task-id>/` with a `manifest.json` listing subtasks and one `<subtask>.md` per agent.

The stop / subagentStop hooks (`merge_agent_notes.py`) merge ready notes into the active leaf node under `../nodes/`, then archive processed files under `merged/`.

Do not write notes into `work-items/<id>/journal/`.
