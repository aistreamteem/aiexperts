---
name: journal-keeper
description: >-
  Use after every workflow step completes or when the user answers a question.
  Updates the expert journal and the active Work Item journal (phase completed,
  artifacts, Resolved Q&A, next action).
---

# Journal Keeper

Updates progress after each moving-office step or when the operator answers a question.

## When to use

- After every workflow step (estimate draft, inventory hole list, crew day, truck calendar, weigh-ticket pack, claims routing, and so on)
- Whenever the user answers a blocking or deferred question (record in the same response)
- At session end (write Last session summary)
- When facts/rules are loaded or proactively detected

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background-agent notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README). Merged notes land in the active leaf node file.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

`active` is the path from `work-item` to the leaf. A load reads `active` only. A closed question must not stay in `history`.

A blocking question becomes the active leaf. Answering or deferring it: if another open blocking question remains, move `active` there; otherwise return `active` to the parent, update that parent's next action, and clear `history`.

## Journal Schema — which file holds each field

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version if any; Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Update procedures

**After each step:**
1. Write the step completed to **Last completed** (active node)
2. Add artifacts (Work Item-relative paths) on STATUS / Artifacts
3. Set **Next action** from the workflow file (`next` ids, or a human gate)
4. Do not mark a step complete if blocking questions remain or the check did not exit 0
5. Preserve workflow type on the flat journal

**When user answers a question:**
- In the **same response**, add question and answer to **Resolved Q&A / Decisions**
- Remove it from Open questions
- Include date: `[YYYY-MM-DD] Q: [question] A: [answer]`

**At session end:**
1. Write **Last session summary** (what was done, what is next, what is needed from the operator)
2. Optionally refresh `work-items/<id>/STATUS.md`

**Trigger audit snapshot:** after the journal update, run `py -3 .claude/hooks/journal_snapshot.py` if present (or rely on the stop hook `on_stop.py`). If it fails, log and do not block the role.

**Merge background-agent notes:** if `agent-notes/` exists, the stop hook folds them into the active leaf node. Do not invent a parallel role-state file.

## Artifact paths

All under `work-items/<id>/`:
- `in/` — operator-dropped rate file, inventory, calendar, tickets, photos
- `work/` — working CSVs and indexes
- `out/` — finished pack (estimate draft, crew day, hole list, claims routing)
- `evidence/` — check logs
- `facts/` — Work Item facts and rules
- `TODOS.md` / `STATUS.md`

Do not keep a parallel `items/` tree or a role `active_map` machine only to drive a deleted process skill.
