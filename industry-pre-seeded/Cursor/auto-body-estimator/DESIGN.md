# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Auto body estimator / office role Expert.

This expert keeps **canonical expert infrastructure** (journals, work-items, shared memory, registered role workflows) and **collision-shop office** content. It does **not** keep a software design/implement pipeline or a parallel generic role-process skill stack.

Finished work is a **pack in the Work Item `out/` folder**. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble or reassemble a solution. Do not invent missing parts. Multi-step work is a **workflow file** under `.cursor/workflows/`: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Role method: [`docs/role/work-item-method.md`](docs/role/work-item-method.md).

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` and the active Work Item journal. One ready workflow step. Continue is not a yes. |
| **define-role** | First session if role is pending; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Update expert and Work Item journals after work, decisions, or session end. |
| **remember** | Store a fact or rule in shared memory or Work Item `facts/`. |
| **workflow-selector** | Offer registered role jobs from `workflow-registry.json` when starting a Work Item. |
| **operator-qa** | Short Q&A session under `qa-sessions/` when shop knowledge or a choice is missing. |
| **promote-facts-rules** | Elevate selected Work Item facts/rules into shared memory. |
| **switch-context** | Change the active Work Item id. |
| **integrate-docs** | Fold operator docs into shared facts/rules. |
| **memory-optimize** | Health-check shared memory files. |
| **visual-page** | Optional shared visual page when a diagram or layout helps. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not used (removed)

Software design/implement pipelines and old generic role-process glue are **not** part of this expert. Starting work, walking a job, checks, write-ups, and scope refusals live in **continue**, **journal-keeper**, **workflow-selector**, **operator-qa**, **remember**, `MyRole.txt`, Work Item folders, and the registered workflow files.

## Role workflows

Named jobs live under `.cursor/workflows/` and are listed in `.cursor/workflows/workflow-registry.json`. Default: `assignment-intake`. Each file is self-contained: walk the YAML, follow `docs/tools/`, write under `work-items/<id>/`, check, journal.

## Memory

- `facts/facts-shared.md` — shop facts (starter until the operator confirms)
- `facts/rules-shared.md` — shop rules
- `facts/MEMORY-INDEX.md` — navigation
- Work Item facts/rules under `work-items/<id>/facts/`
