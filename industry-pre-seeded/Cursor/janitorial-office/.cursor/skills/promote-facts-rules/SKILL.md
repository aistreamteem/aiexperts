---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to operations memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskQuestion for a fixed choice.

Reviews Work Item-level facts and rules and lets the operator promote selected learnings into Expert Role **operations** memory for this janitorial-office role.

## When to use

- User says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches done and continue prompts for promotion
- User wants to review what was learned on a pack

> **Memory model:** Shared pair (`facts/facts-shared.md`, `facts/rules-shared.md`) for `Workflows: all`; operations pair for job-scoped entries. Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) are not split.

## Instructions

1. Read active Work Item ID from `.cursor/active-context.txt` (`work-item:<id>`; legacy fallback `.cursor/active-work-item.txt`).

2. Read `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md`.

3. Parse entries. Skip already `promoted-to-expert` or `archived`.

4. Present a numbered list of facts and rules. For each: "Should this be promoted to Expert Role operations memory? (Yes/No/Skip)"

5. For each Yes:
 - Optional edit/generalize
 - Ask which role jobs it applies to (default: current workflow, or `all`)
 - For a **rule**, ask for Triggers (`write:file`, `write:sheet`, `write:csv`, `write:doc`, `none`)
 - Append to shared (`facts/facts-shared.md` / `facts/rules-shared.md`) when Workflows is `all`, otherwise to `facts/facts-operations.md` or `facts/rules-operations.md`
 - After a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`
 - Mark the Work Item entry promoted; record the decision in the Work Item journal
 - Add a MEMORY-INDEX pointer if the topic is new

6. Also present journal field "Proactively detected facts/rules".

7. Confirm counts. Remind the operator to keep operations files with the Expert folder backup.

8. If a new repeating role job appeared, ask whether to add it to `MyRole.txt` and the workflow registry — not a developer pipeline.

## Example

Work Item `2026-09-15-clinic-night` done. Promote “this shop names wings East/West on the night board” → `facts/facts-operations.md` with Workflows: `night-board`. Leave a one-off complaint quote at Work Item level.
