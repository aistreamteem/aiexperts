---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to operations Expert Role memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Use AskUserQuestion for a fixed choice.

Reviews Work Item-level facts and rules and allows the user to promote valuable learnings to Expert Role operations memory for future chart packs.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" status and continue skill prompts for promotion review
- User wants to review what was learned during a pack (export names, week-start, palette override)

> **Memory model (read first):** Shared pair (`facts/facts-shared.md`, `facts/rules-shared.md`)
> for `**Workflows:** all`. Operations pair (`facts/facts-operations.md`, `facts/rules-operations.md`)
> for a registered chart-job id. After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the
> entry introduces a new topic. **Work Item** facts (`work-items/<id>/facts/`) are not split.

## Instructions

1. **Read active Work Item ID** from `.claude/active-context.txt` (`work-item:<id>`).

2. **Read Work Item facts and rules:**
   - `work-items/<work-item-id>/facts/facts.md`
   - `work-items/<work-item-id>/facts/rules.md`

3. **Parse entries:** Extract all fact/rule entries. Skip any already marked as "promoted-to-expert" or "archived".

4. **Present to user for review:**

```
Work Item Facts:
1. [Date] [Label]: [First line of content...]

Work Item Rules:
1. [Date] [Label]: [First line of content...]
```

For each entry, ask: "Should this be promoted to Expert Role level? (Yes/No/Skip)"

5. **For each "Yes" selection:**

   a. Optional: ask to generalize/edit before promoting.

   b. Ask workflow applicability. **Smart default:** `all`. User may name a registered chart job (`describe-csv`, `time-series-line`, …). Do not offer software-build or incident-response jobs.

   b.5. **Ask action trigger (rules only):**
   - Vocabulary: `write:python`, `write:csv`, `write:chart`, `write:doc`, `none`.
   - Facts skip this.

   c. **Append** to shared (`Workflows: all`) or operations (registered job id):

```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** [all | registered workflow id]
**Triggers:** [action token(s) or `none` – rules only]
**Captured:** [Original capture date]
**Promoted from:** WID-XXXXXXXX (on YYYY-MM-DD)
**Source:** [Original source if any]

[Content]
```

   After appending a rule whose `Triggers:` is not `none`, run `python scripts/memory/build_trigger_index.py`.

   d. Mark the Work Item entry `promoted-to-expert`.

   e. Record the decision in the Work Item journal.

6. Include journal field "Proactively detected facts/rules" in the review.

7. **Summary:** Confirm counts. Remind: commit changed files under `facts/` if they use git.

8. Optional: if this pack followed a new repeating job, ask whether to add a workflow to `MyRole.txt` and the registry.

## Success Criteria

- Selected learnings live in shared or operations memory
- Work Item entries marked promoted
- Journal documents decisions

## Example

**Scenario:** Histogram pack done; they taught bin width and a colorblind override.

- Promote "week starts Sunday in the POS export" → `facts/facts-operations.md`
- Promote "never use red-green as the only good/bad encoding" (already a role rule; skip duplicate)
- Do not promote a one-off source filename
