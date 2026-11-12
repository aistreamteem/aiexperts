# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Optometry front role (not the doctor)

This Expert keeps **universal expert infrastructure** (journals, Work Items, operations memory, canonical skills) and **this job’s** workflows, tools, facts, and rules. It does **not** run a software-build pipeline and does **not** keep a second generic role-runtime skill layer.

Use ordinary words with the person. No jargon. Finished work is a **pack note** plus list files under the Work Item `out/` folder. Look in saved files before starting. Do not invent missing shop procedure. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Work-item method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role here |
| --- | --- |
| **continue** | Resume from `journals/expert/` + active Work Item; one ready workflow step |
| **define-role** | Pending role only; write `MyRole.txt` and stub role jobs |
| **journal-keeper** | Expert journal + `journals/work-items/<id>/` |
| **remember** | Operations facts/rules or Work Item memory; tools under `docs/tools/` |
| **workflow-selector** | Registered jobs in `.claude/workflows/workflow-registry.json` |
| **operator-qa** | Clarification sessions under `qa-sessions/` |
| **promote-facts-rules** | Elevate Work Item memory into operations files |
| **switch-context** | Change active Work Item |
| **integrate-docs** | Fold operator docs into operations memory |
| **memory-optimize** | Health check on operations memory |
| **visual-page** | Optional shared picture of a list, day book, or flow |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not used

Software-build pipeline skills and old generic role-runtime glue are gone. Starting work, walking a job, checks, pack notes, scope, and asking instead of inventing now live in **continue**, **journal-keeper**, **workflow-selector**, **operator-qa**, **remember**, **integrate-docs**, `MyRole.txt`, `facts/rules-operations.md`, and the job files under `.claude/workflows/`.

## Role jobs

Listed in `.claude/workflows/workflow-registry.json`. Default typical-day start: **day-list**.
