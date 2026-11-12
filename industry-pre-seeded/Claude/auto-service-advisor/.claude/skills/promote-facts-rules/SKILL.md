---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to Expert Role memory.
disable-model-invocation: false
---

# Promote Facts and Rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them under a removed `work-items/<id>/journal/` path. Use AskQuestion for a fixed choice.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Reviews Work Item-level facts and rules and allows user to promote durable shop knowledge to Expert Role memory.

## When to use

- User explicitly says "promote facts/rules", "summarize learnings", "elevate to expert level"
- Work Item reaches "done" status and continue skill prompts for promotion review
- User wants to review what was learned during an RO pack

> **Memory model:** Expert Role memory uses `facts/facts-shared.md` / `facts/rules-shared.md` for `Workflows: all`, and `facts/facts-operations.md` / `facts/rules-operations.md` for shop RO-job detail. Do not promote into developer or incident-response files. Work Item facts stay as-is until promoted.

## Instructions

1. **Read active Work Item ID** from `.claude/active-context.txt` (legacy `.claude/active-work-item.txt` read-only fallback).

2. **Read Work Item facts and rules:**
 - `work-items/<id>/facts/facts.md`
 - `work-items/<id>/facts/rules.md`

3. **Parse entries.** Skip any already marked `promoted-to-expert` or `archived`.

4. **Present to user for review** (Yes / No / Skip per entry).

5. **For each "Yes":**
 - Optional: ask to generalize (shop-wide vs this RO).
 - Workflows: default `all` → append to the **shared** pair. Shop-job-only detail → **operations** pair. Do not offer software-build or incident-response labels.
 - Rules: keep or elicit `**Triggers:**` (`none` unless the rule must fire on a tool action such as `write:doc`).
 - Use `### YYYY-MM-DD: Title` headers.
 - After appending a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.
 - Mark the Work Item entry `promoted-to-expert` and record the decision in the Work Item journal.
 - Add a MEMORY-INDEX pointer if the topic is new.

6. **Summary:** how many promoted, paths updated. Remind the operator to keep the facts files with the Expert folder.

## Example

Work Item for RO 5521 captured "This shop's MPI export is the Mitchell DVI PDF, not a paper 50-point." Operator promotes → append to `facts/facts-shared.md` with Workflows: all (or operations if it is job-step detail only).
