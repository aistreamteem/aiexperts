---
name: journal-keeper
description: >-
  Update the expert journal and the active Work Item journal after a
  workflow step, operator answer, or session end. Continue depends on this.
disable-model-invocation: false
---

# Journal keeper

Keep a readable progress file so **continue** can resume this janitorial-office role.

## When to use

After define-role, after a workflow step, after a decision, at session end, when next action changes, when the operator answers a blocking question.

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>` (legacy read fallback: `.cursor/active-work-item.txt`).
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.
- Background-agent notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README). Merged notes land on the active node file, not only in `progress.md`.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

**Workflow type** values: one registered role job (`night-board`, `complaint-callback`, `quality-checklist-pack`, `missed-service-list`, `supply-below-par`, `sds-index-missing`, `extra-work-auth-list`, `holiday-coverage`, `key-log-completeness`).

**Artifacts** on STATUS are paths relative to the Work Item folder (`work/site-list.csv`, `out/night-board.md`, `evidence/…`).
## Do

1. Update the Work Item journal and the active node note: what happened, artifacts, checks (command, exit code, log path), decisions, next ready step.
2. Do not mark the pack complete if blocking questions remain or if a workflow step has no passing check.
3. When the operator answers, record Q&A in the same turn and remove the question from Open questions.
4. Extra workers must not edit the journal. Only this chat, using this skill.
5. Do not keep a parallel role-machine state file. Progress lives in the Work Item journal and `journals/work-items/<id>/state.json`.

`next_action` examples: `wait for operator`, `continue`, a workflow step id (`sites`, `schedule`, `pack`), `done`.
