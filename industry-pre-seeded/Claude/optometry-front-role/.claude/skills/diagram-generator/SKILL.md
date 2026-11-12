---
name: diagram-generator
description: "Use when the journal or user asks to regenerate, refresh, expand, or synchronize design diagrams (docs/diagrams/*.mmd and index.html) with existing HLD/DD documents."
disable-model-invocation: false
---

# Diagram Generator

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Regenerates Mermaid diagrams from design docs when asked. Use AskQuestion for a fixed choice. This leftover skill is not part of the optometry-role job maps. Keep only the Standard profile when HLD docs are present (D2).

## When to use

- Journal or user requests diagram regeneration/refresh/synchronization
- Diagrams in `docs/diagrams/` are missing, outdated, or inconsistent with design docs
- The HTML viewer page needs to be rebuilt or updated after design changes

## Instructions

1. Use **Mermaid** by default for all diagrams (architecture, sequence, ER, C4-style).
2. Read available design docs under `docs/design/` (for example `hld.md`, `dd.md`) and align diagrams to what exists. Do not invent Extended HLD section lists.
3. Regenerate or update diagrams in `docs/diagrams/` so they are synchronized with current HLD/DD content. Preserve clear naming conventions and avoid removing valid existing diagrams without reason.
4. **Generate or refresh the HTML page** (e.g. `docs/diagrams/index.html`) used to view diagrams in a browser. The page should load Mermaid.js (e.g. from a CDN), render each diagram, and include a simple list or nav.
5. Verify `docs/design/hld.md` and `docs/design/dd.md` reference relevant diagrams and update references if needed.
6. Update the journal with what was regenerated/refreshed and set the next action according to the active pipeline step (do not force a pipeline jump if the project is not in a standalone diagram phase).
