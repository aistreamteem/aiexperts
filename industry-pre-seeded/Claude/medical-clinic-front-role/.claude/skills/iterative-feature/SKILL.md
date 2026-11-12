---
name: iterative-feature
description: "Use when the user asks to add a new feature, change an existing feature, or continue iterative development on an existing codebase (gather requirements -> design -> approval -> implement -> test -> PR)."
trigger: User asks to add a new feature, change a feature, or continue iterative development

---

# Iterative Feature

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them under a legacy `work-items/<id>/journal/` path. Use AskUserQuestion for a fixed choice.

Drives the workflow for a new or modified feature after initial delivery: gather requirements, research, design, approval, branch, implement, test, commit/PR/push. Use when the user asks to add a feature, change a feature, or continue iterative development.

## When to use

- User asks to add a new feature or modify an existing feature
- Journal mode is `iterative_feature` or user says "new feature", "add feature", "change feature"
- Continued development after initial project delivery

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

