# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Pest control office role expert.

This expert keeps **universal expert infrastructure** (journals, work items, operations memory, canonical skills) and **this job’s** pest-office workflows. Old old role-runtime glue are not part of the expert. Canonical platform skills from the base expert (including pipeline skills) are kept.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a **pack** (list or completeness file) under the Work Item `out/` folder. Look in saved files before starting. Think in **parts**: route rows, tickets, skips, callbacks, log fields, inventory names, bait-map ids, WDO form pages. Do not invent missing parts. Multi-step work is a **registered job** under `.claude/workflows/`: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

## Canonical expert skills (keep)

| Skill | Role here |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` and the active Work Item journal. One ready pest-office step. Continue is not a yes. |
| **define-role** | First session if role is pending; write `MyRole.txt` and stub pest-office jobs. |
| **journal-keeper** | Update expert vs Work Item journals after work, decisions, or session end. |
| **remember** | Save facts/rules into `facts/facts-operations.md` / `facts/rules-operations.md` or Work Item memory. |
| **workflow-selector** | Offer jobs from `workflow-registry.json` only. |
| **operator-qa** | Clarification sessions under `qa-sessions/`. |
| **promote-facts-rules** | Elevate Work Item learnings into operations memory. |
| **switch-context** | Change the active Work Item. |
| **integrate-docs** | Fold operator docs into operations memory. |
| **memory-optimize** | Health-check operations memory files. |
| **visual-page** | Optional picture beside chat. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Role jobs (not skills)

Pest control office jobs live in `.claude/workflows/` and the registry. Method: `docs/role/work-item-method.md`.

bait-map-index, callback-list, chemical-log-completeness, device-count, estimate-from-price, inventory-chem-vs-log, route-day, skip-list, wdo-form-completeness.

## Not in this expert

Developer SDLC (spec-parser, implement-feature, scaffold, HLD/DD writers, refactor, diagram-generator) and old role-runtime glue (start-job, run-map, verifier, write-up, teach, and similar) are **not** skills here. Their jobs are covered by **continue**, **workflow-selector**, **journal-keeper**, **remember**, **operator-qa**, Work Item folders, and the pest-office workflow files.

## Memory

- Index: `facts/MEMORY-INDEX.md`
- Facts: `facts/facts-operations.md`
- Rules: `facts/rules-operations.md`
- Tools: `docs/tools/`
