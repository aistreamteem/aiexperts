---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to Expert Role shared or operations memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them to `journals/work-items/<id>/progress.md` as step notes.

Reviews Work Item-level facts and rules and lets the operator promote durable shop knowledge into Expert Role shared or operations memory.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" and continue prompts for promotion review

> **Memory model:** Route `Workflows: all` into `facts/facts-shared.md` / `facts/rules-shared.md`. Route a named registry id into `facts/facts-operations.md` / `facts/rules-operations.md`. After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic. Work Item files stay unsplit.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Instructions

1. Read active Work Item ID from `.claude/active-context.txt` (legacy `.claude/active-work-item.txt` only as read fallback).

2. Read `work-items/<id>/facts/facts.md` and `.../rules.md`.

3. Skip entries already marked `promoted-to-expert` or `archived`.

4. Present a numbered list and ask Yes/No/Skip for each.

5. For each Yes:
 - Optional edit/generalize
 - Ask which workflows: default current registry id; allow `all` or comma-separated inventory job ids. Do not route to developer or incident files.
 - For a **rule**, ask Triggers: `write:doc`, `write:csv`, `write:pack`, or `none`
 - Append to shared (`all`) or operations (named job)
 - If Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`
 - Mark the Work Item entry promoted
 - Record the decision in the Work Item journal

6. Include proactively detected facts/rules from the journal.

7. Summarize counts. Remind the operator to keep shared/operations memory with the rest of this Expert folder.

8. If a new recurring role job appeared, ask whether to add a workflow file and registry entry (and update `docs/role/work-item-method.md`).

## Example

Work Item WID-20261108 (cycle-count) done.

- Fact: “This shop’s recount threshold is 2 units or 1%.” → Yes → `facts-operations.md`, Workflows: `cycle-count`
- Rule: “Never invent on-hand qty.” → Yes → `rules-shared.md`, Workflows: `all`, Triggers: `none`
