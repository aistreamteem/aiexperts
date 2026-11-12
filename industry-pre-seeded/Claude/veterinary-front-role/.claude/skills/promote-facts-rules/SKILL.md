---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to shared or operations memory.
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

Reviews Work Item-level facts and rules and allows the operator to promote durable clinic knowledge to Expert Role shared or operations memory.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" and continue prompts for promotion review

> **Memory model:** Route `Workflows: all` to `facts/facts-shared.md` / `facts/rules-shared.md`. Job-scoped entries go to `facts/facts-operations.md` / `facts/rules-operations.md`. Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay unsplit. After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic.

## Instructions

1. **Read active Work Item ID** from `.claude/active-context.txt` (legacy `.claude/active-work-item.txt` as read fallback only).

2. **Read Work Item facts and rules:**
 - `work-items/<work-item-id>/facts/facts.md`
 - `work-items/<work-item-id>/facts/rules.md`

3. **Parse entries.** Skip any already marked as "promoted-to-expert" or "archived".

4. **Present for review.** For each entry, ask: "Should this be promoted to Expert Role level? (Yes/No/Skip)"

5. **For each "Yes":**

 a. Optional: ask whether to edit/generalize before promoting.

 b. Workflow applicability: default `all` → shared pair; otherwise a registered job id → operations pair. Do not offer software-build or incident-response jobs.

 b.5. For a **rule**, ask for `**Triggers:**` (`none` unless a tool-action such as `write:csv`, `write:pack`, or `write:doc` should surface it). Facts skip this.

 c. Append to:
 - Facts with `Workflows: all` → `facts/facts-shared.md`; job-scoped facts → `facts/facts-operations.md`
 - Rules with `Workflows: all` → `facts/rules-shared.md`; job-scoped rules → `facts/rules-operations.md`
 - Format:
```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** [Original capture date]
**Promoted from:** WID-XXXXXXXX (on YYYY-MM-DD)
**Source:** [Original source if any]

[Content]
```
 - After appending a rule whose `Triggers:` is not `none`, run `python scripts/memory/build_trigger_index.py`.

 d. Mark the Work Item entry **Status:** `promoted-to-expert`.

 e. Record the promotion in the Work Item journal Decisions section.

6. Include proactively detected facts/rules from the journal.

7. Confirm counts. Remind the operator that shared and operations memory files plus MEMORY-INDEX are this Expert’s lasting shop notes.

8. Optional: if a new repeating role job appeared, offer to add a workflow file and registry entry — not a software pipeline.

## Example

Work Item complete after a new-client-forms pack:

- Fact "This clinic’s new-patient packet is pages 1–8 plus required signature" → promote to facts-operations
- Rule "Do not mark complete without required signature or declined-to-sign" → already in rules-operations; skip duplicate
