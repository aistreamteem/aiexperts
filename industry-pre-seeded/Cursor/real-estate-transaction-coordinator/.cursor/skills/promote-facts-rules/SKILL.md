---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to operations memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Use AskQuestion for a fixed choice.

Reviews Work Item-level facts and rules and lets the operator promote shop learnings into Expert Role operations memory.

## When to use

- Operator says promote facts/rules, summarize learnings, or elevate to expert level
- Work Item reaches done and continue offers a promotion review

## Memory model

Expert Role memory for this TC role is the operations pair:

- facts → `facts/facts-operations.md`
- rules → `facts/rules-operations.md`

Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay unsplit. Route promotions to the operations pair only.

## Instructions

1. Read active Work Item ID from `.cursor/active-context.txt` (`work-item:<id>`).
2. Read `work-items/<id>/facts/facts.md` and `rules.md`.
3. List active (not already promoted) entries. For each, ask Yes / No / Skip.
4. On Yes:
   - Optional edit/generalize.
   - Workflow applicability: default current job (`dates-calendar`, `missing-docs`, …) or `all`.
   - Rules only: Triggers `write:csv` | `write:checklist` | `write:doc` | `none`.
   - Append to the operations file. After a rule whose trigger is not `none`, run `python scripts/memory/build_trigger_index.py`.
   - Mark the Work Item entry `promoted-to-expert` and record the decision in the journal.
5. Also present journal field “Proactively detected facts/rules”.
6. Summarize counts. Remind the operator to keep operations files with the Expert folder.
7. If this pack followed a new repeating job, ask whether to add a workflow to `MyRole.txt` and the registry.

## Example

Work Item fact “This shop uses calendar days for option periods” → promote to `facts/facts-operations.md` with Workflows `dates-calendar, option-period-pack`.

Work Item rule “Never invent option days from a typical period” → promote to `facts/rules-operations.md`, trigger `write:checklist`.
