---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to Expert Role shared memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

## Journal layer

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Reviews Work Item-level facts and rules and lets the operator promote durable shop knowledge into Expert Role shared memory.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" and continue prompts for promotion review

> **Memory model:** This role’s Expert Role memory is **shared**. Promote facts into `facts/facts-shared.md` and rules into `facts/rules-shared.md`. `Workflows:` may be `all` or one or more registry ids (`beo-pack`, `banquet-check-file`, …). After promoting, add a pointer to `facts/MEMORY-INDEX.md` if the entry introduces a new topic. Work Item files stay unsplit.

## Instructions

1. Read active Work Item ID from `.cursor/active-context.txt` (`work-item:<id>`; legacy `.cursor/active-work-item.txt` is read-only fallback).

2. Read `work-items/<id>/facts/facts.md` and `.../rules.md`.

3. Skip entries already marked `promoted-to-expert` or `archived`.

4. Present a numbered list and ask Yes/No/Skip for each.

5. For each Yes:
 - Optional edit/generalize
 - Ask which workflows: default current registry id; allow `all` or comma-separated venue job ids. Route `all` to the shared pair. Do not route to developer or incident files.
 - For a **rule**, ask Triggers: `write:doc`, `write:csv`, or `none`
 - Append with header `### YYYY-MM-DD: Title` to `facts/facts-shared.md` or `facts/rules-shared.md`
 - If Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`
 - Mark the Work Item entry promoted
 - Record the decision in the Work Item journal

6. Include proactively detected facts/rules from the journal.

7. Summarize counts. Remind the operator to keep shared memory with the rest of this Expert folder.

8. If a new recurring role job appeared, ask whether to add a workflow file and registry entry (and update `docs/role/work-item-method.md`).

## Example

Work Item WID-20261108 (beo-pack) done.

- Fact: “This shop numbers BEOs as event-date + function.” → Yes → `facts-shared.md`, Workflows: `beo-pack`
- Rule: “Never copy card PAN onto the banquet-check exception CSV.” → Yes → `rules-shared.md`, Triggers: `write:csv`
