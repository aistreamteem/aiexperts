# Agent notes

Background agents write one markdown file here (loose notes) or under `tasks/<task-id>/` (shared tasks with `manifest.json` + one `<subtask>.md` each).

Loose notes merge into the active leaf node under `journals/work-items/<id>/nodes/` on the next stop hook. Shared tasks merge only when every subtask has a note.

Do not edit `progress.md` from background agents. Processed notes move to `merged/`.
