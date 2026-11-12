---
name: journal-keeper
description: >-
  Update journals/expert/progress.md and the active Work Item journal after
  work, decisions, or session end. Use whenever next action or the day’s
  dispatch story changes.
---

# Journal keeper

Keep a readable expert journal and a Work Item journal so **continue** works.

## When

After define-role, after a pack step, after a decision, at session end, when next action changes.

## Do

1. Update `journals/expert/progress.md`: current Work Item id, and future work that is not a Work Item yet.
2. Write through the files below (item-wide vs step-specific). Do not invent a parallel store.
3. Update `journals/work-items/<id>/state.json` only as a branch map (`active` node names). Current phase is the phase node on the `active` path — it is not stored as a separate journal field.
4. Long Q&A: one line in the active node; details in **operator-qa** session files when a recorded session is open.
5. Do not mark the job complete if blocking questions remain, or if the work map still has steps without a passing check (unless the operator recorded a documented exception).
6. Extra workers must not edit the journal. Only this chat, using this skill. Background agents write loose notes under `journals/work-items/<id>/agent-notes/` (see that folder’s README); the stop hook merges them into the active node.
7. There is no `work-items/<id>/journal/` folder; journals live under `journals/work-items/<id>/`.
8. Optionally refresh `work-items/<id>/STATUS.md` Last session summary and Artifacts list.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec/pack brief; Mode; Repo URL; Current branch; Commit strategy; PR URL; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase (use the `active` path in `state.json`) |

`next_action` examples: `define-role`, `wait for person`, `continue`, a workflow step id (`pull`, `pack`, `dvirs`), `wait for operator to accept pack`.
