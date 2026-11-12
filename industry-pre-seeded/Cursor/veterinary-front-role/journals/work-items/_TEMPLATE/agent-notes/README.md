# Background agent notes

Drop loose notes as `*.md` files in this folder. Shared multi-agent tasks go under `tasks/<task-id>/` with a `manifest.json` listing `task`, optional `deadline`, and `subtasks` (note basenames without `.md`).

On stop, `merge_agent_notes.py` merges completed notes into the active leaf node under `../nodes/`, then archives them in `merged/`.
