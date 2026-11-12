---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to operations memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskUserQuestion for a fixed choice.

Reviews Work Item-level facts and rules and allows the operator to promote valuable learnings to Expert Role memory.

## When to use

- Operator says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" and continue prompts for promotion review

> **Memory model:** `Workflows: all` → shared pair; a registered job id → operations pair. Do not invent software-build or incident-response memory files. After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic. Work Item files stay unsplit.

## Instructions

1. Read active Work Item ID from `.claude/active-context.txt` (`work-item:<id>`; legacy read fallback `.claude/active-work-item.txt`).
2. Read `work-items/<id>/facts/facts.md` and `.../rules.md`.
3. Skip entries already `promoted-to-expert` or `archived`.
4. Present a numbered list. For each: "Should this be promoted to Expert Role level? (Yes/No/Skip)"
5. For each Yes:
   - Optional generalize/edit
   - Workflows: `all` → append to `facts/facts-shared.md` or `facts/rules-shared.md`; a registered job id → operations pair
   - Rules only — Triggers: `write:doc`, `write:csv`, or `none` (typical for this role). Not `config:change` / `write:sql` / `pr:open` unless they insist.
   - Use heading `### YYYY-MM-DD: Title`
   - If a rule trigger is not `none`, run `python scripts/memory/build_trigger_index.py`
   - Mark the Work Item entry `promoted-to-expert` and record the decision in the journal
6. Also review "Proactively detected facts/rules" on the journal.
7. Confirm counts. Remind the operator to keep shared/operations files and `MEMORY-INDEX.md` with the Expert folder.
8. If a new repeating job appeared, offer to add a pipeline/workflow to `MyRole.txt` and the registry — still a childcare-office job, not a software pipeline.

## Example

Work Item: Room A attendance for 2026-11-08.

- Fact "They code extra-care as XC on the Brightwheel export" → operations facts, Workflows: `attendance-day`
- Rule "Never mark present to tidy ratio" → already in operations; skip duplicate
