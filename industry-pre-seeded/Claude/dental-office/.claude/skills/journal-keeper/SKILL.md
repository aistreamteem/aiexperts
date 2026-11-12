---
name: journal-keeper
description: >-
  Update journals/expert and the active Work Item journal after role work,
  decisions, or session end. Use whenever the next action or the day's story changes.
---

# Journal keeper

Keep a readable expert journal and Work Item journal so **continue** works.

## When to use

- After every dental-role map step, operator answer, or completed artifact
- After define-role, workflow-selector, or remember
- At session end (Last session summary)
- When facts/rules are loaded or proposed

## Where notes go

Three stores. Do not put step notes in the pointer file.

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)

Preserve the exact `Current work item:` line. Only **continue** and **switch-context** may change it.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>` (legacy `.claude/active-work-item.txt` is read-only fallback).
- Artifacts (`in/`, `work/`, `out/`, `evidence/`, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Background agents drop notes under `journals/work-items/<id>/agent-notes/` (see that folder's README). The stop hook merges them into the active node via `merge_agent_notes.py`; do not tell agents that merged notes land in `progress.md`.

## Where each journal field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and job-specific context; Mode; Decisions and approvals every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes; checks |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; Quick links |
| Not stored as a field | Current phase. It is the phase node on the `active` path in `state.json` |

**Workflow type values:** registered job id (`day-list`, `broken-list`, `claims-fields`, `day-close`, `eligibility-notes`, `eob-index`, `forms-check`, `preauth-fields`, `recall-list`).

**Facts and rules sources:** Work Item files under `work-items/<id>/facts/`; Expert Role operations memory in `facts/facts-operations.md` and `facts/rules-operations.md`.

## Rules

- Do not mark the job complete if blocking questions remain or map steps remain unpassed.
- When the operator answers, record Q&A in the same turn and remove the question from Open questions.
- Extra workers must not edit the journal. Only this chat, using this skill.
- Track progress in the Work Item journal and STATUS.md.

`next_action` examples: `define-role`, `workflow-selector`, `pull schedule export`, `wait for operator`, `staff review of out/day-list.md`, `done`.
