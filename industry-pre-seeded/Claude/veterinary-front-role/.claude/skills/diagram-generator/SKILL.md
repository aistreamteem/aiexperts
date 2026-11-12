---
name: diagram-generator
description: "Use when the journal or user asks to regenerate, refresh, expand, or synchronize design diagrams (docs/diagrams/*.mmd and index.html) with existing HLD/DD documents."
trigger: Journal or user requests diagram regeneration/refresh/synchronization
---

# Diagram Generator

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them under a legacy `work-items/<id>/journal/` path. Use AskUserQuestion for a fixed choice.

Regenerates and synchronizes architecture, sequence, ER, and C4-style diagrams from design docs. Use when diagrams need refresh or consistency checks.

## When to use

- Journal or user requests diagram regeneration/refresh/synchronization
- Diagrams in `docs/diagrams/` are missing, outdated, inconsistent, or not aligned with `docs/design/hld.md` and `docs/design/dd.md`
- The HTML viewer page needs to be rebuilt or updated after design changes

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

