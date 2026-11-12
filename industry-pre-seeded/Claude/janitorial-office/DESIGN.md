# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Janitorial / contract-cleaning office expert.

This expert keeps the **expert architecture** (journals, work-items, operations memory, registered workflows) and **canonical expert skills** only. Developer SDLC skills and old-seed generic process skills are not part of this role.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a pack under `work-items/<id>/out/` plus STATUS. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble or reassemble a solution. Do not invent missing parts. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Role method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role here |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` + active Work Item. One ready workflow step. Continue is not a yes. |
| **define-role** | Pending role only. This seed is already defined. |
| **journal-keeper** | Expert journal vs Work Item journal / `state.json` / node notes. |
| **remember** | Facts and rules into operations memory or the Work Item `facts/` files. |
| **workflow-selector** | Registered role jobs from `workflow-registry.json`. |
| **operator-qa** | Clarifying Q&A under `qa-sessions/`. |
| **promote-facts-rules** | Elevate selected Work Item learnings into operations memory. |
| **switch-context** | Change active Work Item id. |
| **integrate-docs** | Batch notes into operations facts/rules. |
| **memory-optimize** | Health of operations memory files. |
| **visual-page** | Optional visual of a board, route, or pack. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not in this expert

Developer SDLC skills and old generic process-skill glue are **not part of this role**. Starting work uses **workflow-selector** + a Work Item. Stepping a job uses the workflow file + **continue**. Checks live inside the workflow file. Scope and refuse live in `MyRole.txt` and `facts/rules-operations.md`.

## Work Item method (this role)

Intake source files → match a registered role job → extracts in `work/` → pack in `out/` → human gates for missing scope/SDS/keys/auth → close with checks and STATUS.

Jobs: complaint-callback, extra-work-auth-list, holiday-coverage, key-log-completeness, missed-service-list, night-board, quality-checklist-pack, sds-index-missing, supply-below-par.
