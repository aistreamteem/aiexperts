---
name: journal-keeper
description: >-
  Update journals/expert/progress.md and the active Work Item journal after
  work, decisions, or session end. Use whenever next action or the pack
  story changes.
---

# Journal keeper

Keep a readable progress file and a small state file so **continue** works.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## When

After define-role, after a pack step, after a decision, at session end, when next action changes, when the operator answers a question.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes; checks run |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored as a journal field | Current phase — it is the phase node on the `active` path in `state.json` |

## Do

1. Update `journals/expert/progress.md`: current Work Item id, one-line session story if it changed.
2. Update the active Work Item journal `journals/work-items/<id>/progress.md` for item-wide fields (workflow type, completion status, decisions).
3. Update the active leaf under `journals/work-items/<id>/nodes/` for step notes, open questions, checks, and next action.
4. Update `journals/work-items/<id>/state.json` so `active` names the current note. Do not keep a parallel role-state file at the expert root.
5. Long Q&A: one line in the node note; details in Resolved Q&A. Use **operator-qa** when a clarifying session is needed.
6. Do not mark the job complete if blocking questions remain, or if workflow steps still lack a passing check (unless the operator recorded an exception).
7. Extra workers must not edit the journal. Only this chat, using this skill. Background agents write loose notes under `journals/work-items/<id>/agent-notes/` (see that folder's README); `on_stop.py` merges them into the active node — not into a legacy `work-items/<id>/journal/progress.md` pointer.

`next_action` examples: `define-role`, `wait for operator`, `continue` (named step in the selected `.claude/workflows/` file), `done`.
