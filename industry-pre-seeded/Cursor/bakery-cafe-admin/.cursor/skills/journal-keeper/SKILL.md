---
name: journal-keeper
description: >-
  Use after every bakery-cafe job step completes or when the operator answers a
  question. Updates the expert journal and the active Work Item journal
  (phase completed, artifacts, Resolved Q&A, next action).
---

# Journal Keeper

Keep a readable expert journal and Work Item journal so **continue** works.

## When to use

- After every workflow step (bake-list row extract, formula index, pack, receiving join, and so on)
- When the operator answers a blocking or deferred question (record in the same response)
- At session end (Last session summary)
- When facts/rules are loaded or proactively detected

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (item-wide fields, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README); the stop hook merges into the active node

There is no `work-items/<id>/journal/` notes path.

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

A blocking question becomes the active leaf. Answering or deferring it: if another open blocking question remains, move `active` there; otherwise return `active` to the parent and set the parent’s next action.

## Work Item context

1. Read active Work Item ID from `.cursor/active-context.txt` (`work-item:<id>`; legacy `.cursor/active-work-item.txt` is read-only fallback)
2. Flat journal: `journals/work-items/<work-item-id>/progress.md`
3. Active note: last id in `state.json` `active`, file `nodes/<id>.md`
4. STATUS path: `work-items/<work-item-id>/STATUS.md`

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and job-specific context; Mode; source file pointers; Decisions and approvals every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; quick links |
| Not stored as a field | Current phase. It is the phase node on the `active` path in `state.json` |

## Journal fields for this role

**Flat journal:**
- **Work Item ID:** bake date, pack name, or `WID-XXXXXXXX`
- **Work Item description:** e.g. Tuesday bake list, wholesale Thursday, cake board for 11/14
- **Workflow type:** registered job id (`bake-list-day`, `case-par-vs-count`, `wholesale-day`, `custom-cake-board`, `holiday-bake-up`, `receiving-shorts`, `ingredient-below-par`, `stale-and-waste`, `allergen-sheet-index`)
- **Completion status:** not started | in progress | done

**Active node:**
- **Last completed:** last step id that passed its check
- **Next action:** exact next step (e.g. `bake-list-day:formulas`, `wait for missing formula file`, `done`)
- Open questions (blocking / deferred), blockers, step notes, facts/rules loaded

**External references:** bake-list sheet, formula file, standing CSV, invoice PDF folder, cake-order folder, allergen sheet, production calendar, case-par sheet, receiving CSV

**Artifacts / session summary:** `work-items/<id>/STATUS.md` and pack paths under `in/`, `work/`, `out/`, `evidence/`

**Facts and rules:**
- Work Item facts/rules loaded from `work-items/<id>/facts/`
- Expert Role facts/rules applied from shared + operations pairs under `facts/`
- Rule violations / conflicts
- Proactively detected facts/rules

Do not keep a parallel role-state system (`active_map` as a second runtime). Step progress lives in this journal and `state.json` `active`.

## Update procedures

**After each step:**
1. Write the step completed to **Last completed** on the active node
2. Add artifacts produced (Work Item-relative paths) on STATUS / node notes
3. Set **Next action** to the next YAML step, a wait-for-file gate, or `done`
4. Do not mark a step complete if blocking questions remain or the check did not exit 0
5. Preserve **Workflow type** — set once by workflow-selector

**When the operator answers:**
- Same response: add to Resolved Q&A, remove from Open questions, include the date

**When facts/rules load:**
- Update the facts/rules loaded lists from shared + operations memory and Work Item files

**At session end:**
1. Write Last session summary on STATUS
2. Optionally refresh `work-items/<id>/STATUS.md`
3. If the hook exists, run `py -3 .cursor/hooks/on_stop.py` or `py -3 .cursor/hooks/journal_snapshot.py` (log failure; do not block)

## Artifact paths (this role)

- `in/` — files they dropped for this bake date / pack
- `work/` — bake-list CSV, formula index, standing extract, joins
- `out/` — finished pack markdown
- `evidence/` — check logs
- `facts/` — Work Item facts and rules
- `TODOS.md` / `STATUS.md` — remaining steps and status

## Example

**After bake-list extract:**
- Last completed: `bake-list-day:list`
- Next action: `bake-list-day:formulas`
- Artifacts: `work/bake-list.csv`

**After a missing formula gate:**
- Next action: `wait for missing formula file`
- Open questions (blocking): bake-list row "Holiday pie" has no formula card

**At session end:**
- Last session summary: Packed Tuesday bake list with two missing formula pointers left visible. Next: drop those formula cards or confirm the items are off the list.
