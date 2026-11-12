---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to Expert Role operations memory.
disable-model-invocation: false
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`.

Reviews Work Item-level facts and rules and lets the operator promote durable shop knowledge into Expert Role operations memory.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" and continue prompts for promotion review

> **Memory model:** This role’s Expert Role memory is **operations**. Promote facts into `facts/facts-operations.md` and rules into `facts/rules-operations.md`. `Workflows:` may be `all` or one or more registry ids (`weekly-pack`, `meeting-pack`, …). After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic. Work Item files stay unsplit.

## Instructions

1. Read active Work Item ID from `.claude/active-context.txt` (`work-item:<id>`).

2. Read `work-items/<id>/facts/facts.md` and `.../rules.md`.

3. Skip entries already marked `promoted-to-expert` or `archived`.

4. Present a numbered list and ask Yes/No/Skip for each.

5. For each Yes:
 - Optional edit/generalize
 - Ask which workflows: default current registry id; allow `all` or comma-separated office-operations job ids. Do not route to developer or incident files.
 - For a **rule**, ask Triggers: `write:doc`, `write:csv`, or `none`
 - Append with header `### YYYY-MM-DD: Title` to `facts/facts-operations.md` or `facts/rules-operations.md`
 - If Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`
 - Mark the Work Item entry promoted
 - Record the decision in the Work Item journal

6. Include proactively detected facts/rules from the journal.

7. Summarize counts. Remind the operator to keep operations memory with the rest of this Expert folder.

8. If a new recurring role job appeared, ask whether to add a workflow file and registry entry (and update `docs/role/work-item-method.md`).

## Example

Work Item WID-20261108 (weekly-pack) done.

- Fact: “This office’s week starts Monday on the wall calendar, even when the export starts Sunday.” → Yes → `facts-operations.md`, Workflows: `weekly-pack`
- Rule: “Never copy a full SSN onto the weekly pack CSV.” → Yes → `rules-operations.md`, Triggers: `write:csv`
