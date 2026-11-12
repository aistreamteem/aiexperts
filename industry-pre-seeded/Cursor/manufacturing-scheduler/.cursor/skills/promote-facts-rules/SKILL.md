---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to Expert Role memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Write through journal-keeper only.

Reviews this pack’s facts/rules and lets the operator promote durable shop knowledge to Expert Role memory.

## When to use

- User says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches done and **continue** offers a promotion review

> **Memory model:** Expert Role memory is `facts/facts-shared.md` + `facts/rules-shared.md` for `Workflows: all`, and `facts/facts-operations.md` + `facts/rules-operations.md` for job-specific entries. Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay as-is until promoted.

## Instructions

1. Read active Work Item ID from `.cursor/active-context.txt` (legacy read fallback: `.cursor/active-work-item.txt`).
2. Read `work-items/<id>/facts/facts.md` and `.../rules.md`.
3. Skip entries already `promoted-to-expert` or `archived`.
4. Present each remaining entry; ask Yes / No / Skip.
5. For Yes:
   - Offer to edit/generalize (remove a single WO number if this is now a shop rule).
   - Workflows: default `all` → shared pair; or a registered job key (`dispatch-list`, `kit-list`, …) → operations pair.
   - Rules: keep `**Triggers:** none` unless they named a real write action (`write:doc` or `write:csv`).
   - Append with header `### YYYY-MM-DD: Title` and `**Promoted from:** <id>`.
   - Mark the Work Item entry `promoted-to-expert`.
   - If a rule trigger is not `none`, run `py -3 scripts/memory/build_trigger_index.py`.
6. Record decisions in the Work Item journal via journal-keeper.
7. Remind them to keep Expert Role memory with the Expert folder (backup the whole folder).

## Example

Pack `2026-11-08-dispatch` learned “hot is only the HOT column on the WO export.” Operator says Yes → append to `facts/rules-operations.md` if job-specific, or `facts/rules-shared.md` if it applies to every pack (ask update vs skip if a similar rule exists).
