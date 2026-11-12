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

After define-role, after a pack step, after a decision, at session end, when next action changes, when facts/rules are loaded or proposed.

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line; future work that is not a Work Item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, workflow type, decisions, completion)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background-agent notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README). Merged notes land in the active leaf node file, not in a pointer under `work-items/`.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Preserve the exact `Current work item:` line. Only **continue** and **switch-context** may change it.

A blocking question becomes the active leaf. Answering or deferring it returns `active` to the parent when no other blocking question remains. Use **AskUserQuestion** for a fixed choice. Use chat for an open answer.

## Journal Schema — which file holds each field

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context (service date, unit/route); Spec file and version if any; Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Update procedures

**After each workflow step:**
1. Last completed = step id (on the active node)
2. Add produced files to Artifacts / STATUS
3. Next action = next ready step, or wait for operator if a gate/check failed
4. Do not mark complete if blocking questions remain or a required check failed
5. Preserve workflow type on the flat journal

**When the operator answers:** same response, move to Resolved Q&A with date, remove from Open questions.

**At session end:** one-paragraph Last session summary (what was packed, what is next, what file or answer is needed). Refresh `work-items/<id>/STATUS.md`.

**After journal update:** run `py -3 .claude/hooks/journal_snapshot.py` if present (or rely on the stop hook `on_stop.py`); log failure but do not block.

**Next actions** follow the selected fleet workflow file and `docs/role/work-item-method.md` (intake → assignment → routes → DVIR → exceptions → POD → file questions → accepted pack). Not HLD/DD/implement.

`next_action` examples: `define-role`, `wait for person`, `continue`, a workflow step id (`pull`, `pack`, `dvirs`), `wait for operator to accept pack`.
