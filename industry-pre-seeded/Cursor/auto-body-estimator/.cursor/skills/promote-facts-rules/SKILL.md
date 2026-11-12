---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to shared memory.
disable-model-invocation: false
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields go in `journals/work-items/<id>/progress.md`. Use AskQuestion for a fixed choice.

Reviews Work Item-level facts and rules and lets the operator promote durable shop knowledge to Expert Role shared memory.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" and continue prompts for promotion review
- User wants to review what was learned on this assignment / RO / claim

> **Memory model:** This role stores Expert Role memory in `facts/facts-shared.md` and `facts/rules-shared.md`. `Workflows: all` is the normal tag. After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry is a new topic. Work Item files stay under `work-items/<id>/facts/`.

## Instructions

1. **Read active Work Item ID** from `.cursor/active-context.txt` (legacy fallback: `.cursor/active-work-item.txt`).

2. **Read Work Item facts and rules:**
 - `work-items/<work-item-id>/facts/facts.md`
 - `work-items/<work-item-id>/facts/rules.md`

3. **Parse entries:** Skip any already marked `promoted-to-expert` or `archived`.

4. **Present to user for review** as a numbered list. For each: "Should this be promoted to Expert Role shared memory? (Yes/No/Skip)"

5. **For each "Yes":**

 a. Optional edit/generalize before promoting.

 b. Workflow applicability default: `all` (this collision-shop office). Destination is always the shared pair.

 b.5. **Ask action trigger (rules only):**
 - Vocabulary: `write:doc`, `write:csv`, `write:estimate`, `write:photo-index`, `write:supplement`, `write:sql`, `sql:generate`, `pr:open`, `git:push`, `git:commit`, or `none`. Do not use `config:change`.

 c. **Append** facts to `facts/facts-shared.md`, rules to `facts/rules-shared.md`.

```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** all
**Triggers:** [token or none — rules only]
**Captured:** [Original capture date]
**Promoted from:** WID-XXXXXXXX (on YYYY-MM-DD)
**Source:** [Original source if any]
**Status:** active

[Content]

---
```

 - After appending a rule whose `Triggers:` is not `none`, run `python scripts/memory/build_trigger_index.py`.

 d. Mark the Work Item entry `promoted-to-expert`.

 e. Record the promotion in the Work Item journal Decisions.

6. Include journal field "Proactively detected facts/rules" in the review.

7. Confirm counts. Remind the operator that shared files plus MEMORY-INDEX are the durable shop memory.

8. If a new repeating job appeared, ask whether to add a workflow file and registry entry (not a new SDLC pipeline).

## Success Criteria

- Selected learnings live in shared memory
- Work Item entries marked promoted
- Journal records the decisions
