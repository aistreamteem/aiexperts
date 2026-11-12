---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to Expert Role operations memory.
disable-model-invocation: false
---

# Promote Facts and Rules

## Journal layer

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Use AskQuestion for a fixed choice.

Reviews Work Item-level facts and rules and allows the operator to promote durable hotel-role knowledge to Expert Role operations memory.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" status and continue skill prompts for promotion review
- User wants to review what was learned during a stay-date pack

> **Memory model (read first):** This role’s Expert Role memory is **operations only**.
> Promote into `facts/facts-operations.md` and `facts/rules-operations.md`.
> Set `**Workflows:** all` unless the operator names a single registered job id (for example `arrivals-day`).
> After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic.
> Work Item facts (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay as-is until marked promoted.

## Instructions

1. **Read active Work Item ID** from `.cursor/active-context.txt` (`work-item:<id>`).

2. **Read Work Item facts and rules:**
 - `work-items/<work-item-id>/facts/facts.md`
 - `work-items/<work-item-id>/facts/rules.md`

3. **Parse entries:** Extract all fact/rule entries with labels, dates, and content. Skip any already marked as "promoted-to-expert" or "archived".

4. **Present to user for review:**

```
Work Item Facts:
1. [Date] [Label]: [First line of content...]

Work Item Rules:
1. [Date] [Label]: [First line of content...]
```

For each entry, ask: "Should this be promoted to Expert Role level? (Yes/No/Skip)"

5. **For each "Yes" selection:**

 a. Optional: ask whether to edit or generalize before promoting.

 b. Workflow applicability: default **all** (hotel-role operations). Operator may name a registry id from `workflow-registry.json`.

 b.5. **Ask action trigger (rules only):** `write:doc`, `write:csv`, or `none`. Carry forward any existing `**Triggers:**`. Facts skip this.

 c. **Append** to `facts/facts-operations.md` or `facts/rules-operations.md`:

```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** all
**Triggers:** [action token(s) or `none` – rules only]
**Captured:** [Original capture date]
**Promoted from:** WID-XXXXXXXX (on YYYY-MM-DD)
**Source:** [Original source if any]

[Content]
```

 - After appending a rule whose `Triggers:` is not `none`, run `python scripts/memory/build_trigger_index.py`.

 d. Mark the Work Item entry **Status:** `promoted-to-expert` on YYYY-MM-DD.

 e. Record the promotion in the Work Item journal Decisions.

6. Include journal field "Proactively detected facts/rules" in the review.

7. Confirm counts. Remind the operator to keep operations memory in the Expert folder backup.

8. Optional: if a new repeating role job appeared, ask whether to add it to `MyRole.txt` and `workflow-registry.json`.

## Example

**Scenario:** Arrivals Work Item complete; operator wants to promote.

- "We never overbook Friday football nights" → rule in `facts/rules-operations.md`
- "Room 12 connecting door is 14" → fact in `facts/facts-operations.md` if it is property-wide; else leave at Work Item

## Notes

- Promotion is selective, not automatic
- Promoted facts/rules load on future Work Items via operations memory
