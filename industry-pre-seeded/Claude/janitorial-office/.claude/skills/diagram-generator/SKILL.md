---
name: diagram-generator
description: "Use when the journal or user asks to regenerate, refresh, expand, or synchronize design diagrams (docs/diagrams/*.mmd and index.html) with existing HLD/DD documents."
disable-model-invocation: false
---

# Diagram Generator

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Write through journal-keeper. Use AskQuestion for a fixed choice.

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



1. Use **Mermaid** by default for all diagrams.
2. Prefer diagrams the operator asked for from files that exist under the Work Item or `docs/`. This role does not ship HLD/DD profile packs; do not invent `docs/design/hld-profiles.md` or `hld-extended-sections.md`.
3. Regenerate or update diagrams under `docs/diagrams/` (or the Work Item `out/` / `work/` path the operator named). Preserve clear naming.
4. When useful, refresh an HTML viewer page (e.g. `docs/diagrams/index.html`) that loads Mermaid.js and lists diagrams.
5. Update the journal via journal-keeper with what was regenerated and the next ready role step.
