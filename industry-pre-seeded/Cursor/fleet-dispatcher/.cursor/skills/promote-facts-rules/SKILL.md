---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to the workflow-split Expert Role memory as permanent institutional knowledge.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them to a legacy `work-items/<id>/journal/` path. Use AskQuestion for a fixed choice.

Reviews Work Item-level facts and rules and allows user to promote valuable learnings to Expert Role level, making them permanent institutional knowledge available to all future Work Items.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" status and continue skill prompts for promotion review
- User wants to review what was learned during a Work Item

> **Memory model (read first):** Always-on cross-job knowledge goes in the **shared** pair
> (`facts/facts-shared.md`, `facts/rules-shared.md`) with `**Workflows:** all`.
> Role-job-specific knowledge goes in the **operations** pair
> (`facts/facts-operations.md`, `facts/rules-operations.md`) with a registered job id.
> After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic.
> **Work Item context-level** facts (`work-items/<id>/facts/facts.md`, `.../rules.md`) are NOT split – read them as-is.
> Do not create developer or incident-response memory files for this role.

## Instructions

1. **Read active Work Item ID** from `.cursor/active-context.txt` (`work-item:<id>`; legacy file is read-only fallback).

2. **Read Work Item facts and rules:**
 - `work-items/<work-item-id>/facts/facts.md`
 - `work-items/<work-item-id>/facts/rules.md`

3. **Parse entries:** Extract all fact/rule entries with labels, dates, and content. Skip any already marked as "promoted-to-expert" or "archived".

4. **Present to user for review:**

Create a summary list:
```
Work Item Facts:
1. [Date] [Label]: [First line of content...]
2. [Date] [Label]: [First line of content...]

Work Item Rules:
1. [Date] [Label]: [First line of content...]
2. [Date] [Label]: [First line of content...]
```
For each entry, ask: "Should this be promoted to Expert Role level? (Yes/No/Skip)"
 - Yes: Promote to the workflow-split Expert Role file matching its `Workflows:` value (see Memory model above)
 - No: Leave at Work Item level
 - Skip: Move to next entry

5. **For each "Yes" selection:**

 a. **Optional: Ask user to generalize/edit:**
 - Present the full content
 - Ask: "Would you like to edit or generalize this before promoting? (e.g., make it more broadly applicable)"
 - If user edits, use edited version for promotion

 b. **Ask workflow applicability:**
 - "Which workflows should this apply to?"
 - **Smart default:** Current registered role job (from parent Work Item journal) or `all`
 - User can override: "all", or a comma-separated list of registry ids
 - Decision tree: roster/assignment → assignment-pack; stops/windows → todays-routes; inspection files → dvir-gap; late/fail → exceptions; unit down → breakdown; dwell times → detention; signatures → pod-check; ELD gaps → hos-questions; gallons → fuel-outliers; shop-wide never/always → all

 b.5. **Ask action trigger (rules only):**
 - For a **rule**, ask: "What tool-action is the agent about to take when this rule becomes relevant?"
 - Carry forward any `**Triggers:**` already on the Work Item rule; if none, elicit one now.
 - Vocabulary (comma-separate; `none` if pure background/judgment): `write:doc`, `write:csv`, `none`.
 - Facts skip this – they are browse-only.

 c. **Append to Expert Role memory:**
 - If `Workflows: all`: fact → `facts/facts-shared.md`; rule → `facts/rules-shared.md`
 - Else: fact → `facts/facts-operations.md`; rule → `facts/rules-operations.md`
 - Format:
```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** [all | assignment-pack | todays-routes | dvir-gap | exceptions | breakdown | detention | pod-check | hos-questions | fuel-outliers]
**Triggers:** [action token(s) or `none` – rules only; from step b.5]
**Captured:** [Original capture date]
**Promoted from:** WID-XXXXXXXX (on YYYY-MM-DD)
**Source:** [Original source if any]

[Content]

---
```
 - **After appending a rule whose `Triggers:` is not `none`, regenerate the index:** `python scripts/memory/build_trigger_index.py` (so the action hook picks it up).

 d. **Mark as promoted in Work Item file:**
 - Update the Work Item fact/rule entry
 - Change **Status:** from `active` to `promoted-to-expert` on YYYY-MM-DD`
 - Or add line: `[Promoted to Expert Role on YYYY-MM-DD]`

 e. **Record promotion decision in Work Item journal:**
 - Add to "Resolved Q&A / Decisions" section:
 - "Promoted [fact/rule] '[Label]' to Expert Role level on [date]"

6. **Include proactively detected facts/rules:**
 - Check Work Item journal field "Proactively detected facts/rules"
 - Present these to user for promotion consideration as well
 - These may already be stored in facts/rules files; if not, store and then promote

7. **Summary and next steps:**
 - Confirm how many facts/rules were promoted
 - List the promoted items
 - Remind user: "Remember to keep `facts/facts-operations.md`, `facts/rules-operations.md`, and `facts/MEMORY-INDEX.md` with the Expert so these learnings are preserved for future Work Items."

8. **Optional: Suggest new MyRole.txt pipelines:**
 - If workflow deviations were detected during the Work Item, suggest:
 - "I noticed this Work Item followed a [different pattern]. Should we add a new pipeline to MyRole.txt for this workflow?"
 - If user agrees, help update MyRole.txt with new pipeline definition

## Success Criteria

After running this skill:
- Valuable Work Item learnings elevated to Expert Role level
- The relevant workflow-split Expert Role files (facts-*/rules-*.md) updated with promoted content
- Work Item facts/rules marked as promoted (not duplicated on future reviews)
- Work Item journal documents promotion decisions
- User reminded to commit Expert Role files to repo

## Example Workflow

**Scenario:** Work Item 2026-09-15-truck-14-route-a complete; user wants to promote learnings

1. **Agent reads Work Item facts/rules:**
 - Work Item Facts: 2 entries
 - "2026-09-15: This date's spare unit was 88, not on the printed roster"
 - "2026-09-15: Night dispatcher on-call label is ROLE-ONCALL"
 - Work Item Rules: 1 entry
 - "2026-09-15: Tractor and trailer DVIRs stay separate files"

2. **Agent presents for promotion:**
 - "Should 'spare unit 88' fact be promoted to Expert Role? (Yes/No/Skip)"
 - User: "No, specific to this Work Item"
 - "Should 'on-call label' fact be promoted to Expert Role? (Yes/No/Skip)"
 - User: "Yes"
 - "Should 'separate DVIR files' rule be promoted to Expert Role? (Yes/No/Skip)"
 - User: "Yes"

3. **Agent promotes:**
 - Team contact fact (Workflows: all) → appended to `facts/facts-operations.md`
 - Shop rule (Workflows: assignment-pack) → appended to `facts/rules-operations.md`
 - Both marked as promoted in Work Item files
 - Journal updated with promotion decisions

4. **Agent confirms:**
 - "Promoted 1 fact and 1 rule to Expert Role operations memory."
 - "Keep facts-operations.md / rules-operations.md (and MEMORY-INDEX.md) with this Expert."

## Notes

- Promotion is selective, not automatic - user decides what becomes institutional knowledge
- Promoted facts/rules are available to all future Work Items via auto-loading (Rule 21)
- Over time, Expert Role rules accumulate, making the expert smarter
- Consider promotion at end of each Work Item to build knowledge incrementally
