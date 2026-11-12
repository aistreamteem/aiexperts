---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to Expert Role shared memory as permanent institutional knowledge.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Reviews Work Item-level facts and rules and allows the operator to promote valuable learnings to Expert Role level.

## When to use

- Operator explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" status and continue skill prompts for promotion review
- Operator wants to review what was learned during a board pack, grant, gift batch, or restricted-fund question

> **Memory model (read first):** This role stores Expert Role memory in the **shared** pair:
> `facts/facts-shared.md` and `facts/rules-shared.md`.
> `Workflows: all` or a registry job id (`board-pack`, `grant-report`, …). After promoting, add a pointer to
> `facts/MEMORY-INDEX.md` if the entry introduces a new topic. **Work Item** facts
> (`work-items/<id>/facts/facts.md`, `.../rules.md`) are not split — read them as-is.

## Instructions

1. **Read active Work Item ID** from `.claude/active-context.txt` (legacy read fallback: `.claude/active-work-item.txt`).

2. **Read Work Item facts and rules:**
 - `work-items/<work-item-id>/facts/facts.md`
 - `work-items/<work-item-id>/facts/rules.md`

3. **Parse entries:** Extract all fact/rule entries with labels, dates, and content. Skip any already marked as "promoted-to-expert" or "archived".

4. **Present to operator for review:**

```
Work Item Facts:
1. [Date] [Label]: [First line of content...]

Work Item Rules:
1. [Date] [Label]: [First line of content...]
```

For each entry, ask: "Should this be promoted to Expert Role level? (Yes/No/Skip)"

5. **For each "Yes" selection:**

 a. Optional: ask to generalize/edit before promoting.

 b. Ask workflow applicability:
 - Default: current role job from the Work Item journal, or `all` for shop-wide practice
 - Operator can override: `all`, or a registry id (`board-pack`, `donor-list`, `grant-report`, …)

 b.5. Ask action trigger (rules only):
 - Default for this role: `none` (judgment loaded with shared memory)
 - Also allowed: `write:doc` | `write:csv` when the rule should surface on pack/CSV writes
 - Facts skip this
 - Vocabulary must match `.claude/hooks/inject_rules_on_action.py` (`KNOWN_TOKENS`)

 c. Append to shared memory:
 - Fact → `facts/facts-shared.md`
 - Rule → `facts/rules-shared.md`
 - Keep `**Workflows:**` as chosen
 - After appending a rule whose `Triggers:` is not `none`, run `python scripts/memory/build_trigger_index.py`

 d. Mark as promoted in the Work Item file (`Status: promoted-to-expert`).

 e. Record the promotion in the Work Item journal Resolved Q&A / Decisions.

6. Include proactively detected facts/rules from the journal.

7. **Summary:** how many promoted, which files, remind the operator to keep shared memory current.

8. **Optional:** If this Work Item followed a new repeating pattern, ask whether to add a role job to `MyRole.txt` and `workflow-registry.json`.

## Example

Work Item complete after a September board pack:

- Fact "Fiscal year starts July 1" → `facts/facts-shared.md` (`Workflows: all`)
- Rule "Do not recast restricted totals as unrestricted on the board cover" → `facts/rules-shared.md` (`Workflows: board-pack`)

## Notes

- Promotion is selective, not automatic
- Promoted items load for future Work Items via shared memory
- Consider promotion at the end of each pack
