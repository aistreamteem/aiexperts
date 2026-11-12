---
name: journal-keeper
description: >-
  Update the expert journal and the active Work Item journal after a role-job
  step, operator answer, or session end. Continue depends on this.
---

# Journal keeper

Keep a readable progress file so **continue** can take one ready construction-office step.

## When

After define-role, after a workflow step, after a decision, at session end, when next action changes, when the operator answers a question.

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background-agent notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README). Merged notes land in the active leaf node file.

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Journal Schema — which file holds each field

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; HLD profile, intake links, compliance review; Decisions and approvals that every branch inherits; Completion status; Job number / Source files (this role) |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes; Checks run |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Work Item fields (this role)

Prefer the table above. For this construction-office role specifically:

- **Work Item ID** / **Work Item description** — item-wide journal
- **Workflow type** — registry id; set once by workflow-selector — item-wide journal
- **Last completed** / **Next action** — active node
- **Job number** / **Source files** — item-wide journal
- **Artifacts** — `STATUS.md` (and note paths in the node)
- **Checks run** — active node
- Open questions / Resolved Q&A / Blockers — active node
- Completion status / Last session summary — item-wide journal / STATUS.md

Do not use software-design phase fields or outage-bridge fields.

## Update procedures

**After each step:**
1. Write Last completed on the active node
2. Add artifacts (Work Item-relative paths) to STATUS.md
3. Set Next action on the active node to the next YAML `next` step, or pack review, or done
4. Do not mark a step complete if blocking questions remain or the check did not pass
5. Preserve workflow type on the flat journal

**When the operator answers:** In the same response, add to Resolved Q&A and remove from Open questions on the active node.

**At session end:** Last session summary on STATUS.md; optionally refresh completion fields.

**Hooks:** After the journal update, the stop hook runs `py -3 .claude/hooks/on_stop.py` (merge + audit). If it fails, log and continue. Fold merged agent-notes into the proper sections.

## Next-action examples (this role)

- wait for source files
- intake: confirm job number
- extract: write work/daily-log.csv
- exception-pass: age RFIs
- pack: write out/rfi-status.md
- wait for pack review
- done
