---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to the workflow-split Expert Role memory as permanent institutional knowledge.
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

Use AskQuestion for a fixed choice.

Reviews Work Item-level facts and rules and allows user to promote valuable learnings to Expert Role level, making them permanent institutional knowledge available to all future Work Items.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" status and continue skill prompts for promotion review
- User wants to review what was learned during a Work Item

> **Memory model (read first):** This landscaping office Expert stores Expert Role memory in
> `facts/facts-shared.md` and `facts/rules-shared.md` only. Promote into those files.
> Set `**Workflows:** all` unless the operator names a single registered job id (daily-log, rfi-status, …).
> After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic.
> **Work Item** facts (`work-items/<id>/facts/facts.md`, `.../rules.md`) are not split – read them as-is.
> Do not create extra workflow memory files outside the shared pair.

## Instructions

1. **Read active Work Item ID** from `.claude/active-context.txt` (`work-item:<id>`).

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
 - Yes: Promote to `facts/facts-shared.md` or `facts/rules-shared.md`
 - No: Leave at Work Item level
 - Skip: Move to next entry

5. **For each "Yes" selection:**

 a. **Optional: Ask user to generalize/edit:**
 - Present the full content
 - Ask: "Would you like to edit or generalize this before promoting? (e.g., make it more broadly applicable)"
 - If user edits, use edited version for promotion

 b. **Ask workflow applicability:**
 - "Which jobs should this apply to?"
 - **Smart default:** `all` (every landscaping-office pack)
 - User can override with registered job ids (`daily-log`, `rfi-status`, …) or `all`

 b.5. **Ask action trigger (rules only):**
 - For a **rule**, ask: "What tool-action is the agent about to take when this rule becomes relevant?" – the **action axis** the PreToolUse hook uses to surface the rule in any workflow.
 - Carry forward any `**Triggers:**` already on the Work Item rule; if none, elicit one now.
 - Vocabulary (comma-separate; `none` if pure background/judgment): `write:doc`, `write:sheet`, `none`.
 - Facts skip this – they are browse-only.

 c. **Append to shared memory:**
 - If fact: append to `facts/facts-shared.md`
 - If rule: append to `facts/rules-shared.md`
 - Format:
```markdown
### YYYY-MM-DD: [Label/Title]

**Scope:** expert-role
**Workflows:** [all | registered job id]
**Triggers:** [write:doc | write:sheet | none – rules only; from step b.5]
**Captured:** [Original capture date]
**Promoted from:** WID-XXXXXXXX (on YYYY-MM-DD)
**Source:** [Original source if any]

[Content]

---
```
 - **After appending a rule whose `Triggers:` is not `none`, regenerate the index:** `python scripts/memory/build_trigger_index.py`

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
 - Remind user: "Remember to keep `facts/facts-shared.md`, `facts/rules-shared.md`, and `facts/MEMORY-INDEX.md` with this Expert folder so later packs still see the shop knowledge."

8. **Optional: Suggest a new registered job:**
 - If this pack followed a repeating office job that is not in the registry, suggest adding a workflow file and a MyRole.txt entry.

## Success Criteria

After running this skill:
- Valuable Work Item learnings elevated to Expert Role level
- `facts/facts-shared.md` and/or `facts/rules-shared.md` updated with promoted content
- Work Item facts/rules marked as promoted (not duplicated on future reviews)
- Work Item journal documents promotion decisions
- User reminded to commit Expert Role files to repo

## Example Workflow

**Scenario:** Work Item WID-21411151 complete; user wants to promote learnings

1. **Agent reads Work Item facts/rules:**
 - Work Item Facts: 2 entries
 - "2026-11-08: Job 12 daily log export is the superintendent Procore CSV"
 - "2026-11-08: This week's punch walk was building B only"
 - Work Item Rules: 1 entry
 - "2026-11-08: Never close a punch item unless the sheet already says complete"

2. **Agent presents for promotion:**
 - "Should 'Job 12 daily log export' fact be promoted to Expert Role? (Yes/No/Skip)"
 - User: "No, specific to this Work Item"
 - "Should 'punch walk building B' fact be promoted? (Yes/No/Skip)"
 - User: "No"
 - "Should 'Never close punch unless sheet says complete' rule be promoted? (Yes/No/Skip)"
 - User: "Yes"

3. **Agent promotes:**
 - Punch-complete rule (Workflows: all) → appended to `facts/rules-shared.md`
 - Marked as promoted in the Work Item file
 - Journal updated with promotion decisions

4. **Agent confirms:**
 - "Promoted 1 rule to Expert Role shared memory."
 - "Keep facts-shared.md / rules-shared.md (and MEMORY-INDEX.md) with this Expert folder."

## Notes

- Promotion is selective, not automatic - user decides what becomes institutional knowledge
- Promoted facts/rules are available to all future Work Items via auto-loading (Rule 21)
- Over time, Expert Role rules accumulate, making the expert smarter
- Consider promotion at end of each Work Item to build knowledge incrementally
