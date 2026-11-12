---
name: refactor
description: "Use when the user asks to refactor or reduce tech debt, or when a change would duplicate logic. Keeps existing tests green."
disable-model-invocation: false
---
# Refactor

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields go in `journals/work-items/<id>/progress.md`. Use AskUserQuestion for a fixed choice.

Improves code structure without changing behavior; reduces tech debt and avoids spaghetti code. Use when code would become duplicated, when the user asks to refactor, or when tech debt is blocking a feature.

## When to use

- User asks to refactor or reduce tech debt
- Before or during a feature when the change would duplicate logic or worsen structure
- When existing code is hard to extend or test

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

