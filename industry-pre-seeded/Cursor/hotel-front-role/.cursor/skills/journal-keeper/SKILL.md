---
name: journal-keeper
description: >-
  Update journals/expert/progress.md and the active Work Item journal after
  work, decisions, or session end. Use whenever the next action or the
  day's role story changes.
---

# Journal keeper

Keep a readable expert journal and a Work Item journal so **continue** works.

## When

After define-role, after a pack step, after a decision, at session end, when the next action changes, and when the operator answers a blocking question.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Do

1. Update `journals/expert/progress.md`: current Work Item id, future work that is not a Work Item yet.
2. Update `journals/work-items/<id>/progress.md` with the item-wide fields in the table above.
3. Update `journals/work-items/<id>/state.json` only as a branch map (`active`, `nodes`).
4. Write step notes under `journals/work-items/<id>/nodes/` when `active` names a node.
5. If the Work Item has `STATUS.md`, refresh Last session summary and Next action.
6. Long Q&A: one line in progress.md; details in **operator-qa** session files when a Q&A session is open.
7. Do not mark the job complete if Open questions are non-empty, or if a registered workflow still has unpassed steps.
8. Extra workers must not edit the journal. Only this chat, using this skill. Background agents write loose notes under `journals/work-items/<id>/agent-notes/` (see that folder’s README); the stop hook merges them into the active node via `merge_agent_notes.py`.

`next_action` examples: `define-role`, `wait for operator` (missing arrivals CSV), `arrivals-day: status`, `pack`, `continue`, `done`.
