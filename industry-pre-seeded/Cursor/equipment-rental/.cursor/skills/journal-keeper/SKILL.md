---
name: journal-keeper
description: >-
  Update journals/expert/progress.md and the active Work Item journal after
  work, decisions, or session end. Use whenever the next action or the
  week's story changes.
---

# Journal keeper

Keep a readable progress file and a small state file so **continue** works.

## When

After define-role, after a workflow step, after a decision, at session end, when `next_action` changes, when the operator answers a blocking question.

## Do

1. Read `.cursor/active-context.txt` (fallback `.cursor/active-work-item.txt`) to get the Work Item id.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (pack, intake, evidence, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec/intake links; Mode; Repo URL; Current branch; Commit strategy; PR URL; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored as a journal field | Current phase — it is the phase node on the `active` path in `state.json` |

2. Update `journals/work-items/<id>/progress.md` for item-wide fields only (workflow type, completion status, inherited decisions, work item record).

3. Update the active leaf under `journals/work-items/<id>/nodes/`:
   - What happened this step
   - Checks run (command, exit, log under `evidence/`)
   - Decisions / Resolved Q&A for this step
   - Open questions (blocking / deferred)
   - Blockers / Last failure
   - Next action (next ready step id from the selected workflow, or wait-for-answer / wait-for-approval / done)
   - Facts/rules loaded and applied

4. Update `work-items/<id>/STATUS.md` with last session summary and artifact links when the pack or session changes.

5. Update `journals/work-items/<id>/state.json` only as the Work Item method needs it (active node, status, history). Do not keep a parallel role-runtime machine (`active_map`, `current_job_folder` under a top-level `items/` tree).

6. Update `journals/expert/progress.md` **Current work item** when the active id changes. Do not replace Work Item detail with a second copy of the whole story.

7. Long Q&A: one line in the node note; details in Decisions or in a `qa-sessions/` conclusions file.

8. Do not mark the job complete if blocking questions remain, or if a required workflow step has no passing check.

9. Extra workers must not edit the journal. Only this chat, using this skill. Background agents write loose notes under `journals/work-items/<id>/agent-notes/` (see that folder's `README.md`); the stop hook merges them into the active node file via `merge_agent_notes.py`. Merged notes land in the active node's note file, not in a legacy `progress.md` pointer.

`next_action` examples: `define-role`, `wait for operator`, `continue`, a workflow step id such as `pdf` / `pack`, `wait for pack approval`, `done`.
