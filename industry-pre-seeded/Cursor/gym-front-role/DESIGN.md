# Expert — skill design

**Updated:** 2026-11-08  
**Folder:** Gym / fitness front role Expert (Cursor). Role method: `docs/role/work-item-method.md`.

This is a **role role** expert, not a software-build pipeline. Developer SDLC skills and old generic process skills are not part of this expert.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a **pack** under the Work Item `out/` folder. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble or reassemble a solution. Do not invent missing parts. Multi-step work is a **work map**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/` + active Work Item; one ready role-job step. Continue is not a yes. |
| **define-role** | First session if role is pending; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Update `journals/expert/progress.md` and `journals/work-items/<id>/`. |
| **remember** | Save facts/rules into operations memory or the Work Item `facts/` files. |
| **workflow-selector** | Offer only jobs in `.cursor/workflows/workflow-registry.json`. |
| **operator-qa** | Clarification sessions under `qa-sessions/Q*/`. |
| **promote-facts-rules** | Elevate Work Item memory into `facts/facts-operations.md` / `facts/rules-operations.md`. |
| **switch-context** | Change the active Work Item id. |
| **integrate-docs** | Fold operator docs into operations memory. |
| **memory-optimize** | Health-check operations memory files. |
| **visual-page** | Optional shared visual page. |

## Not in this expert

Software-build pipeline skills (spec parse, design-doc writers, scaffold, implement, tests, git) and old role-glue process skills are **deleted**. Role *how* lives in `.cursor/workflows/*` and `docs/tools/`. Starting work is **workflow-selector** + a Work Item under `work-items/<id>/` + **continue**. Checks and human gates live inside the workflow file and **operator-qa**.

## Role jobs

See `docs/role/work-item-method.md` and `.cursor/workflows/workflow-registry.json`. Default daily job: **check-in-day**.
