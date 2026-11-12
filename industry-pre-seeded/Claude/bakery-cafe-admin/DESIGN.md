# Expert — skill design

**Updated:** 2026-11-08  
**Folder:** Bakery / cafe production office expert.

This expert keeps **canonical expert skills** plus **role workflows**. Software-build pipelines and generic role-glue process layers are not part of this expert.

Use ordinary words with the person. Finished work is a **pack** under the Work Item `out/` folder. Look in saved files before starting. Think in **parts**: what each part is, how parts connect. Do not invent missing parts. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Role method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` + active Work Item journal. One ready workflow step. Continue is not a yes. |
| **define-role** | Only while `MyRole.txt` Role status is pending. |
| **journal-keeper** | Expert journal + Work Item journal + branch map under `journals/`. |
| **remember** | Saves facts/rules into shared or operations memory (or Work Item `facts/`). Tool notes under `docs/tools/`. |
| **workflow-selector** | Registered bakery-cafe jobs from `.claude/workflows/workflow-registry.json` only. |
| **operator-qa** | Clarify missing files, sheet fights, or notes before persisting. |
| **promote-facts-rules** | Elevate Work Item learnings into shared/operations memory. |
| **switch-context** | Change active Work Item. |
| **integrate-docs** | Fold dropped handbooks or shop notes into shared/operations memory. |
| **memory-optimize** | Health check on memory files under `facts/`. |
| **visual-page** | Optional visual of a bake plan, cake board, or route. |

Leftover software-build skill folders (`spec-parser`, `scaffold-project`, `implement-feature`, `iterative-feature`, `refactor`, `diagram-generator`) may still exist in `.claude/skills/` from the scaffold; this role does not use them for bake-plan work.

Starting a job, walking steps, checks, and packs are handled by **workflow-selector**, **continue**, the role workflow file, **journal-keeper**, and the Work Item `out/` / `evidence/` folders. Scope, refuse, and “ask don’t invent” live as content in `MyRole.txt` and `facts/rules-*.md`.

## Role jobs (not skills)

Named jobs live under `.claude/workflows/` and are listed in `workflow-registry.json`. Default daily job: **bake-list-day**.
