---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to shared memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write step notes into the flat `journals/work-items/<id>/progress.md`.

Reviews Work Item-level facts and rules and lets the operator promote durable clinic knowledge into Expert Role shared memory.

## When to use

- Operator says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches done and continue asks about promotion
- Operator wants to review what this pack taught about *this* clinic

> **Memory model:** This veterinary role stores Expert Role memory in `facts/facts-shared.md` and `facts/rules-shared.md`. Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay unsplit.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Instructions

1. Read active Work Item ID from `.cursor/active-context.txt` (legacy `.cursor/active-work-item.txt` as read fallback only).

2. Read `work-items/<id>/facts/facts.md` and `.../rules.md`.

3. Skip entries already marked `promoted-to-expert` or `archived`.

4. Present each remaining entry and ask Yes / No / Skip.

5. For each Yes:
 - Optional edit/generalize
 - Default workflow applicability: `all` (or the current role job id)
 - For a **rule**, ask Triggers (`write:doc`, `write:csv`, `none`)
 - Append to `facts/facts-shared.md` or `facts/rules-shared.md` using `### YYYY-MM-DD: Title`
 - If a rule trigger is not `none`, run `python scripts/memory/build_trigger_index.py`
 - Mark the Work Item entry promoted
 - Record the decision in the Work Item journal

6. Also present journal field "Proactively detected facts/rules".

7. Confirm counts. Remind the operator that shared memory is this clinic’s saved knowledge.

8. Optional: if this pack followed a new repeating job, offer to add a workflow file and registry entry.

## Example

Work Item `2026-11-10-day-book` captured “Sick visits are 30 minutes on this floor.” Operator promotes it → append to `facts/facts-shared.md` with Workflows: `day-appointments` (or `all`).
