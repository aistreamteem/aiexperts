---
name: journal-keeper
description: >-
  Update expert and Work Item journals after a childcare-office step, a
  director decision, or session end. Use whenever next_action or the day's
  pack changes.
---

# Journal keeper

Keep a readable progress file and a small branch map so **continue** works. This Expert uses `journals/expert/` and `journals/work-items/<id>/`.

## When

After define-role, after a workflow step, after a director/operator decision, at session end, when `next_action` changes, when facts/rules are loaded or proposed.

## Where notes go

Three stores. Do not put step notes under `work-items/<id>/` as a journal.

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README). Merged notes land in the active node file via `on_stop.py`, not in the flat progress file.

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

`active` is the path from `work-item` to the leaf. A load reads `active` only. A closed question must not stay in `history`.

A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name. Answering or deferring it: if another open blocking question remains, move `active` there; otherwise return `active` to the parent, update that parent's next action, and clear `history`. Use **AskUserQuestion** for a fixed choice. Use chat for an open answer.

## Work Item context

1. Read active Work Item ID from `.claude/active-context.txt` (`work-item:<id>`; legacy `.claude/active-work-item.txt` as read fallback)
2. Flat journal: `journals/work-items/<work-item-id>/progress.md`
3. Active note: last id in `state.json` `active`, file `nodes/<id>.md`
4. STATUS path: `work-items/<work-item-id>/STATUS.md`

## Which file holds each field

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes; checks run |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; Quick Links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Fields to maintain

**Work Item context (flat journal):**
- **Work Item ID**
- **Work Item description** (date, room, child/family, period, or pack name)
- **Workflow type:** one of the registered role jobs (`attendance-day`, `pickup-list-check`, `ratio-from-their-posted`, `missing-enrollment-forms`, `waitlist`, `tuition-from-file`, `licensing-packet-completeness`, `incident-routing`, `holiday-calendar-pack`)
- **Completion status**

**Step fields (active node):**
- **Last completed** / **Next action** (exact workflow step id or `wait for director` / `wait for operator`)
- Open questions, blockers, checks, loaded facts/rules

**Artifacts (STATUS.md):**
- Paths relative to the Work Item folder (`in/`, `work/`, `out/`, `evidence/`)

**Human gates:**
- Start-without-packet, pickup mismatch, incident signature, ratio alert, licensing gap — stay listed until the director answers

Do **not** keep a parallel role-machine state that only existed to drive an old process loop. Track progress in this journal and `STATUS.md`.

## Session end

Update **Last session summary** on `STATUS.md`: what was completed, what is next, what file or director decision is needed.

Extra workers must not edit the journal. Only this chat, using this skill. Background agents write under `agent-notes/` and let `on_stop.py` merge.
