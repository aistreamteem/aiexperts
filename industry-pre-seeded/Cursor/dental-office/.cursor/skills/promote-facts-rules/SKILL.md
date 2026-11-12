---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to operations memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Write through journal-keeper only.

Reviews Work Item-level facts and rules and lets the operator promote durable office knowledge into Expert Role operations memory.

## When to use

- Operator says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches done and continue asks about promotion
- Operator wants to review what this pack taught about *this* office

> **Memory model:** This dental role stores Expert Role memory in `facts/facts-operations.md` and `facts/rules-operations.md`. Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay unsplit.

## Instructions

1. Read active Work Item ID from `.cursor/active-context.txt` (`work-item:<id>`; legacy `.cursor/active-work-item.txt` is read-only fallback).

2. Read `work-items/<id>/facts/facts.md` and `.../rules.md`.

3. Skip entries already marked `promoted-to-expert` or `archived`.

4. Present each remaining entry and ask Yes / No / Skip.

5. For each Yes:
 - Optional edit/generalize
 - Default workflow applicability: `all` (or the current role job id)
 - For a **rule**, ask Triggers (`write:doc`, `write:csv`, `none`)
 - Append to `facts/facts-operations.md` or `facts/rules-operations.md`
 - If a rule trigger is not `none`, run `python scripts/memory/build_trigger_index.py`
 - Mark the Work Item entry promoted
 - Record the decision in the Work Item journal

6. Also present journal field "Proactively detected facts/rules".

7. Confirm counts. Remind the operator that operations memory is this office’s saved knowledge.

8. Optional: if this pack followed a new repeating job, offer to add a workflow file and registry entry.

## Example

Work Item `2026-11-10-day-list` captured “Hygiene chairs are HyA and HyB on this floor.” Operator promotes it → append to `facts/facts-operations.md` with Workflows: `day-list` (or `all`).
