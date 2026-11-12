---
name: journal-keeper
description: >-
  Update the expert journal and the active Work Item journal after a role-job
  step, operator answer, or session end. Continue depends on this.
---

# Journal keeper

Keep a readable progress file so **continue** can take one ready landscaping-office step.

## When

After define-role, after a workflow step, after a decision, at session end, when next action changes, when the operator answers a question.

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background agent notes: `journals/work-items/<id>/agent-notes/` (see that folder's README). The stop hook merges them into the active leaf node; fold merged blocks into the proper sections afterward.
- Artifacts / STATUS: `work-items/<id>/`

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

Do **not** keep a parallel role-machine state (`active_map`, `current_job_folder`, `steps_passed`) as a second system. Progress lives in the journals above.

## Journal Schema (where each field lives)

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec/source file pointers; Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; Checks run; Source files / Artifacts for this step; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored as a free-text field | Current phase — it is the phase node on the `active` path in `state.json` |

## Work Item fields (this role)

Use the schema table above. Typical values for this shop:

- **Work Item description** — crew day, property + date, ticket, or week
- **Workflow type** — registry id (`crew-day`, `estimate-from-price`, …). Set once by workflow-selector; never change it
- **Last completed** / **Next action** — exact step id from the workflow file, or wait for source files / wait for pack review
- **Artifacts** — paths relative to `work-items/<id>/` (`in/`, `work/`, `out/`, `evidence/`)
- **Checks run** — command, exit code, log path

Do not use software-design phase fields or outage-bridge fields.

## Update procedures

**After each step:**
1. Write Last completed on the active node
2. Add artifacts (Work Item-relative paths)
3. Set Next action to the next YAML `next` step, or pack review, or done
4. Do not mark a step complete if blocking questions remain or the check did not pass
5. Preserve workflow type on the flat journal

**When the operator answers:** In the same response, add to Resolved Q&A and remove from Open questions.

**At session end:** Last session summary on `STATUS.md`; keep Next action on the active node.

**Hooks:** Stop/subagentStop run `py -3 .cursor/hooks/on_stop.py`, which merges `journals/work-items/<id>/agent-notes/` into the active leaf node and commits the audit snapshot of the real journal paths. Fold merged agent notes into the proper sections. Merged notes land in the node file, not in a pointer under `work-items/<id>/journal/`.

## Next-action examples (this role)

- wait for source files
- wait for operator (missing ticket / weather not called / extra-work auth)
- roster / tickets / pack (crew-day)
- extract: write work/tickets.csv
- pack: write out/crew-day.md
- wait for pack review
- done
