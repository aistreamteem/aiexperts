---
name: spec-parser
description: >-
  Use when the operator drops a pack brief, count sheet description, or other
  intake note and asks to open a kitchen Work Item from it. Captures blocking
  questions and seeds the journal — not a software HLD/DD pipeline.
---

# Spec Parser

## Journal layer

Do not create a second tree. `continue` copies `journals/work-items/_TEMPLATE/`. A blocking question becomes a map node through journal-keeper and becomes the active leaf. Use AskQuestion for a fixed choice and chat for an open answer.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## When to use

- Operator points at a brief, BEO, count sheet, invoice, or allergen request and wants a Work Item opened from it
- Journal says next action is "run spec-parser" (rare on this role; prefer **workflow-selector** + the job file)

## Instructions

1. **Load facts and rules:**
   - Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`
   - Load Work Item `facts/` / `rules/` when present
   - Do not load developer or production-incident memory files

2. **Artifact path:** Write a short intake note under `work-items/<id>/in/` or `work-items/<id>/work/intake.md` as the operator prefers. Do not invent design docs under `docs/design/`.

3. **Ask kitchen-neutral questions when missing:**
   - What is affected (service date, shift, vendor, event, waste window)?
   - Who has escalated or must confirm (chef, expo, owner)?
   - Where is the evidence (count sheet, POS export, invoice PDF, allergen matrix)?

4. **Record** blocking vs deferred questions on the active node through **journal-keeper**. Do not invent quantities, pars, allergen status, or inspection outcomes to fill gaps.

5. **Next action:** run **workflow-selector** (or the named registered kitchen job) — not hld-writer, dd-writer, or incident analysis skills.

## Notes

This role’s day-to-day path is registry workflows under `.cursor/workflows/`. Keep this skill only for turning a dropped brief into a Work Item with clear open questions.
