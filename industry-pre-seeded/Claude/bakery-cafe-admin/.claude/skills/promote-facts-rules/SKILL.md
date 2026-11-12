---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to operations memory.
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Put step notes and next action on `journals/work-items/<id>/nodes/<active leaf>.md` via journal-keeper; keep item-wide fields on `journals/work-items/<id>/progress.md`. Use AskUserQuestion for a fixed choice.

Reviews Work Item-level facts and rules and promotes selected shop knowledge into Expert Role **operations** memory.

## When to use

- User says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" and continue offers a promotion review
- User wants to review what this bake date / wholesale day / cake board taught

> **Memory model:** Shared shop-wide memory is `facts/facts-shared.md` / `facts/rules-shared.md` (`Workflows: all`). Job-tagged memory is `facts/facts-operations.md` / `facts/rules-operations.md`. After promoting, add a MEMORY-INDEX pointer only if the entry is a new topic. Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay as-is except for a promoted status mark.

## Instructions

1. **Read active Work Item ID** from `.claude/active-context.txt` (`work-item:<id>`; legacy `.claude/active-work-item.txt` is read-only fallback).

2. **Read Work Item facts and rules:**
 - `work-items/<work-item-id>/facts/facts.md`
 - `work-items/<work-item-id>/facts/rules.md`

3. **Parse entries.** Skip already `promoted-to-expert` or `archived`.

4. **Present for review** (Yes / No / Skip) each fact and rule.

5. **For each Yes:**

 a. Optional edit/generalize before promoting.

 b. Ask workflow applicability. Default: current job id, or `all` for shop-wide (never invent a formula; allergen sheet is live). Options are this role’s registered jobs, not software-developer pipelines.

 b.5. For a **rule**, ask the action trigger if any: `none` (default), `write:sheet`, `write:pack`, `file:intake`. Carry forward an existing `**Triggers:**` field.

 c. Append to:
 - `Workflows: all` → `facts/facts-shared.md` or `facts/rules-shared.md`
 - Job-tagged → `facts/facts-operations.md` or `facts/rules-operations.md`
 - After a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`

 d. Mark the Work Item entry `promoted-to-expert` with the date.

 e. Record the decision in the Work Item journal Resolved Q&A.

6. Include journal field "Proactively detected facts/rules".

7. Confirm counts. Remind the operator to keep a backup of this Expert folder (shop memory lives here).

8. Optional: if a new repeating job appeared (for example a second wholesale route day), ask whether to add it to `MyRole.txt` and the workflow registry.

## Example

Work Item `2026-11-08-bake-list` complete:

- Fact: "Weekend croissant par lives on the Saturday tab" → promote to operations, Workflows: `case-par-vs-count, bake-list-day`
- Rule: "Do not reuse last year's pie card unless they said it is live" → promote to operations, Workflows: `holiday-bake-up`

Leave Work Item-only notes (this Tuesday's oven-down baker note) unpromoted.
