---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to shared or operations memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them under a legacy `work-items/<id>/journal/` path. Use AskUserQuestion for a fixed choice.

Reviews Work Item-level facts and rules and lets the operator promote clinic learnings into Expert Role shared or operations memory.

## When to use

- Operator says promote facts/rules, summarize learnings, or elevate to expert level
- Work Item reaches done and continue offers a promotion review

## Memory model

Expert Role memory for this PT front role:

> shared pair for `Workflows: all` (`facts/facts-shared.md` / `facts/rules-shared.md`); operations pair for job-scoped (`facts/facts-operations.md` / `facts/rules-operations.md`).

Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay unsplit. Do not route to developer or incident files.

## Instructions

1. **Read active Work Item ID** from `.claude/active-context.txt` (`work-item:<id>`; legacy `.claude/active-work-item.txt` fallback only).
2. Read `work-items/<id>/facts/facts.md` and `rules.md`.
3. List active (not already promoted) entries. For each, ask Yes / No / Skip.
4. On Yes:
   - Optional edit/generalize.
   - Workflow applicability: default current job (`day-list`, `auth-remaining-from-file`, …) or `all`.
   - Rules only: Triggers `write:csv` | `write:pack` | `write:doc` | `none`.
   - If fact and `Workflows: all`: append to `facts/facts-shared.md`
   - If rule and `Workflows: all`: append to `facts/rules-shared.md`
   - Otherwise append to the matching operations file.
   - After a rule whose trigger is not `none`, run `python scripts/memory/build_trigger_index.py`.
   - Mark the Work Item entry `promoted-to-expert` and record the decision in the journal.
5. Also present journal field “Proactively detected facts/rules”.
6. Summarize counts. Remind the operator to keep memory files with the Expert folder.
7. If this pack followed a new repeating job, ask whether to add a workflow to `MyRole.txt` and the registry.

## Example

Work Item fact “Thursday remaining lives in the auth-tracker Remaining column, not the visit-count export” → promote to `facts/facts-operations.md` with Workflows `auth-remaining-from-file, visit-count-export-check`.

Work Item rule “Never put date of birth next to name on the day list” → promote to `facts/rules-shared.md` when `Workflows: all`, trigger `write:csv`.
