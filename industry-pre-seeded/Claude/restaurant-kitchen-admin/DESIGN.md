# Expert — skill design

**Updated:** 2026-11-08  
**Folder:** Restaurant kitchen / BOH admin expert.

This expert keeps **canonical expert skills** plus **role workflows**. Software-build pipelines and generic role-glue process layers are not part of this expert.

Use ordinary words with the person. Finished work is a **pack** under the Work Item `out/` folder. Look in saved files before starting. Think in **parts**: what each part is, how parts connect. Do not invent missing parts. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Role method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` + active Work Item journal. One ready workflow step. Continue is not a yes. |
| **define-role** | Only while `MyRole.txt` Role status is pending. |
| **journal-keeper** | Expert journal + Work Item journal + branch map under `journals/`. |
| **remember** | Saves facts/rules into `facts/facts-operations.md` / `facts/rules-operations.md` (or Work Item `facts/`). Tool notes under `docs/tools/`. |
| **workflow-selector** | Registered kitchen jobs from `.claude/workflows/workflow-registry.json` only. |
| **operator-qa** | Clarify missing files, sheet fights, or notes before persisting. |
| **promote-facts-rules** | Elevate Work Item learnings into operations memory. |
| **switch-context** | Change active Work Item. |
| **integrate-docs** | Fold dropped handbooks or shop notes into operations memory. |
| **memory-optimize** | Health check on operations memory files. |
| **visual-page** | Optional visual of a prep plan, walk-in map, or 86 board. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

Starting a job, walking steps, checks, and packs are handled by **workflow-selector**, **continue**, the role workflow file, **journal-keeper**, and the Work Item `out/` / `evidence/` folders. Scope, refuse, and “ask don’t invent” live as content in `MyRole.txt` and `facts/rules-operations.md`.

## Role jobs (not skills)

Named jobs live under `.claude/workflows/` and are listed in `workflow-registry.json`. Default daily job: **prep**.
