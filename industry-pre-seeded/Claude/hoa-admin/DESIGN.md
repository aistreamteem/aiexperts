# Expert — skill design

**Updated:** 2026-11-08
**Folder:** HOA / association admin role Expert.

This expert keeps universal expert infrastructure (journals, Work Items, operations memory, canonical skills) and role content for community-association admin work. Software-build skills and old generic role-process skills are **not** part of this expert.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a **write-up** under the Work Item `out/` folder. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble or reassemble a solution. Do not invent missing parts. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Role method: `docs/role/work-item-method.md`.

## Canonical skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` + active Work Item. One ready workflow step. Continue is not a yes. |
| **define-role** | Ask what this Expert is for; write `MyRole.txt` and stub registered workflows. |
| **journal-keeper** | Update expert vs Work Item journals after work, answers, and session end. |
| **remember** | Save facts/rules into operations memory or the Work Item `facts/` folder. |
| **workflow-selector** | Offer only jobs in `.claude/workflows/workflow-registry.json`. |
| **operator-qa** | Clarification sessions under `qa-sessions/`. |
| **promote-facts-rules** | Move selected Work Item memory into `facts/facts-operations.md` / `facts/rules-operations.md`. |
| **switch-context** | Change the active Work Item pointer. |
| **integrate-docs** | Fold operator docs into operations memory and `MyRole.txt`. |
| **memory-optimize** | Health-check operations memory files. |
| **visual-page** | Optional shared visual page beside chat. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not used (removed)

Developer SDLC pipeline skills and old generic role-process glue were deleted from this expert. Their behavior is covered by Work Items, registered workflows, `continue`, `journal-keeper`, `operator-qa`, `remember`, `integrate-docs`, `MyRole.txt`, and `facts/rules-operations.md`. Do not restore a second process-skill layer.

## Role content

Facts and rules for this role live in `facts/facts-operations.md` and `facts/rules-operations.md`. Tools live under `docs/tools/`. Registered jobs live under `.claude/workflows/` and `workflow-registry.json`.
