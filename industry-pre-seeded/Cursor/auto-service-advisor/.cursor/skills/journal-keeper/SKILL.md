---
name: journal-keeper
description: >-
  Update journals/expert/progress.md and the active Work Item journal after
  work, decisions, or session end. Use whenever next_action or the RO pack
  story changes.
disable-model-invocation: false
---

# Journal keeper

Keep a readable progress file so **continue** works. Expert journal vs Work Item journal — not a leftover top-level journal folder.

## When

After define-role, after a workflow step, after a decision, at session end, when `next_action` changes, when the operator answers a blocking question.

## Do

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

1. Update `journals/expert/progress.md`: current Work Item, future work that is not a Work Item yet, last session summary.
2. Update `journals/work-items/<id>/progress.md` with the **item-wide** fields in the schema table below.
3. Update `journals/work-items/<id>/state.json` only for the branch map (`active` node names). Do not keep `active_map`, `current_job_folder`, or `steps_passed` as a second runtime.
4. Write step notes under `journals/work-items/<id>/nodes/` for the active leaf. Do not write notes under a removed `work-items/<id>/journal/` path.
5. Long Q&A: one line in progress.md; details in the Work Item journal decisions section or the node file.
6. Do not mark the pack complete if blocking questions remain, or if workflow steps still lack passing checks.
7. Extra workers must not edit the journal. Only this chat, using this skill. Background agents write loose notes under `journals/work-items/<id>/agent-notes/` (see that folder's `README.md`); `on_stop.py` / `merge_agent_notes.py` merges them into the **active leaf node**, not into `progress.md`.

`next_action` examples: `define-role`, `workflow-selector`, `wait for operator`, `wait for auth`, `continue`, a named workflow step id (`parts`, `pack`, `find`).

## Journal schema (where each field lives)

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; HLD profile, intake links, compliance review; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |
