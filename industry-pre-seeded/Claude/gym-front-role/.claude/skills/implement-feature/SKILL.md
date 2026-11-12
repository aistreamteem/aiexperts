---
name: implement-feature
description: "Use when the journal says the next action is \"implement-feature (task K/N)\". Implements one task from TODOS, keeps tests green, and updates the journal."
trigger: Journal says next action is "implement-feature (task K/N)"
---

# Implement Feature

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them under a legacy `work-items/<id>/journal/` path. Use AskUserQuestion for a fixed choice.

Implements one feature or task from TODOS in order. Now Work Item-aware with facts/rules enforcement and proactive detection. Use when the pipeline is in implementation phase and next action is implement-feature (task K/N).

## When to use

- Journal says next action is "implement-feature (task K/N)" for some task index K
- Pipeline is in implementation phase

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

