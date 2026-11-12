# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Real estate transaction coordinator role Expert.

This expert keeps **canonical expert skills** (from the base platform expert, including pipeline skills) plus **role workflows** for residential contract-to-close file completeness. Old generic role-process skills were removed; the expert loop is `continue` / `workflow-selector` / `journal-keeper` / `operator-qa` / `remember`.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a **job pack** under the Work Item `out/` folder. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble or reassemble a solution. Do not invent missing parts. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Work Item method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/` + active Work Item. One ready workflow step. Continue is not a yes. |
| **define-role** | Ask what this Expert is for; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Updates expert vs Work Item journals (`journals/expert/progress.md`, `journals/work-items/<id>/`). |
| **remember** | Saves facts/rules into operations memory or Work Item memory; tool pointers under `docs/tools/`. |
| **workflow-selector** | Offers registered role jobs from `workflow-registry.json`. |
| **operator-qa** | Clarification sessions under `qa-sessions/`. |
| **promote-facts-rules** | Elevate Work Item memory into `facts-operations` / `rules-operations`. |
| **switch-context** | Change active Work Item. |
| **integrate-docs** | Batch-ingest notes into operations memory. |
| **memory-optimize** | Health check on operations memory files. |
| **visual-page** | Optional shared visual page. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Role workflows (not skills)

Role jobs live under `.claude/workflows/` and are listed in `workflow-registry.json`. Default: `dates-calendar`. Tools live under `docs/tools/`.

## Not used on this role

A second generic role-process skill layer from the old seeds is not used. Replacement behavior for that glue is in the canonical skills above plus the role workflow files.

**Later if needed:** archive old rules that never get used.
