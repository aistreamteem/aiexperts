---
name: diagram-generator
description: "Use when the journal or user asks to regenerate, refresh, expand, or synchronize diagrams for a chart pack or design note."
disable-model-invocation: false
---

# Diagram Generator

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write step notes into the flat journal; use the active node file via journal-keeper. Use AskQuestion for a fixed choice.

## When to use

- Journal or user requests diagram regeneration/refresh/synchronization
- Prefer **visual-page** for operator-facing chart/process visuals when that skill fits

## Instructions

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

1. Prefer this role’s **visual-page** skill for operator-facing chart/process visuals. Use Mermaid only when a design diagram is still requested.
2. Read whatever design notes exist under `work-items/<id>/`. Do not invent missing HLD/DD profile documents.
3. Regenerate or update diagrams the operator asked for. Preserve clear naming and avoid removing valid existing diagrams without reason.
4. If an HTML viewer is needed, refresh it so diagrams render in a browser.
5. Update the journal with what was regenerated/refreshed and set the next action via journal-keeper.
