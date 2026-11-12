---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to operations memory as permanent institutional knowledge.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them to `journals/work-items/<id>/progress.md`. Use AskQuestion for a fixed choice.

Reviews Work Item-level facts and rules and allows user to promote valuable learnings to Expert Role level, making them permanent institutional knowledge available to all future Work Items.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" status and continue skill prompts for promotion review
- User wants to review what was learned during a Work Item

> **Memory model (read first):** This catering office stores Expert Role memory in the **operations** pair:
> facts → `facts/facts-operations.md`.
> rules → `facts/rules-operations.md`.
> After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic. **Work Item**
> facts (`work-items/<id>/facts/facts.md`, `.../rules.md`) are NOT split – read them as-is.

## Instructions

1. **Read active Work Item ID** from `.cursor/active-context.txt` (`work-item:<id>`), with `.cursor/active-work-item.txt` as a read fallback only.

2. **Read Work Item facts and rules:**
 - `work-items/<work-item-id>/facts/facts.md`
 - `work-items/<work-item-id>/facts/rules.md`

3. **Parse entries:** Extract all fact/rule entries with labels, dates, and content. Skip any already marked as "promoted-to-expert" or "archived".

4. **Present to user for review:**

Create a summary list of Work Item Facts and Work Item Rules. For each entry, ask: "Should this be promoted to Expert Role level? (Yes/No/Skip)"
 - Yes: Promote into operations memory
 - No: Leave at Work Item level
 - Skip: Move to next entry

5. **For each "Yes" selection:**

 a. **Optional: Ask user to generalize/edit** the wording so it is safe across events (do not promote a single Saturday's guarantee as a house law).

 b. **Workflow applicability:** default `all` (this role's operations memory). Do not offer developer or production-incident as destinations unless the operator explicitly creates those files later.

 b.5. **Ask action trigger (rules only):**
 - For a **rule**, ask: "What tool-action is the agent about to take when this rule becomes relevant?"
 - Carry forward any `**Triggers:**` already on the Work Item rule; if none, elicit one now.
 - Vocabulary for this role: `write:doc`, `write:csv`, `git:commit`, `git:push`, `pr:open`, `none`. (`none` if pure background/judgment.) Do not use the retired config-change token.
 - Facts skip this – they are browse-only.

 c. **Append** to `facts/facts-operations.md` or `facts/rules-operations.md`.

 Format:
```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** all
**Triggers:** [action token(s) or `none` – rules only]
**Captured:** [Original capture date]
**Promoted from:** WID-XXXXXXXX (on YYYY-MM-DD)
**Source:** [Original source if any]

[Content]

---
```
 - **After appending a rule whose `Triggers:` is not `none`, regenerate the index:** `python scripts/memory/build_trigger_index.py`.

 d. **Mark as promoted** in the Work Item file (`Status: promoted-to-expert`).

 e. **Record** the promotion in the Work Item journal Resolved Q&A / Decisions.

6. **Include proactively detected facts/rules** from the Work Item journal field "Proactively detected facts/rules".

7. **Summary:** Confirm counts, list promoted items, remind the operator to keep operations memory with the expert folder.

8. **Optional:** If this Work Item followed a new catering-job pattern (for example a tasting board they want every week), ask whether to add a pipeline to `MyRole.txt` and a workflow file.

## Success Criteria

After running this skill:
- Valuable Work Item learnings elevated to Expert Role operations memory
- Work Item facts/rules marked as promoted
- Work Item journal documents promotion decisions

## Example Workflow

**Scenario:** Work Item for Saturday's Acme lunch is done.

1. Work Item Facts include "This shop's leftover release is required on full-service only."
2. Operator says Yes, promote.
3. Append to `facts/facts-operations.md` (and a matching leftover rule if they asked).
4. Confirm and point at operations memory.
