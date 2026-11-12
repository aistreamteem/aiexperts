# Expert — skill design

**Updated:** 2026-11-08  
**Folder:** Hotel / inn front role Expert.

This Expert keeps the **canonical expert architecture** (journals, work-items, operations memory, registered workflows) and this role’s hotel-role jobs. Software-build skills and old role-glue process skills are **not** part of this Expert.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a **pack** in the Work Item `out/` folder. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble or reassemble a solution. Do not invent missing parts. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Work-item method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` and the active Work Item journal. One ready workflow step. Continue is not a yes. |
| **define-role** | If role status is pending, ask and write `MyRole.txt` plus stub workflows. |
| **journal-keeper** | Update expert vs Work Item journals after steps, answers, and session end. |
| **remember** | Save facts/rules into operations memory or Work Item `facts/`. |
| **workflow-selector** | Offer only jobs in `workflow-registry.json`. |
| **operator-qa** | Clarification sessions under `qa-sessions/Q*/`. |
| **promote-facts-rules** | Elevate Work Item notes into `facts-operations` / `rules-operations`. |
| **switch-context** | Change the active Work Item id. |
| **integrate-docs** | Fold operator docs into operations memory. |
| **memory-optimize** | Health-check operations memory files. |
| **visual-page** | Optional shared visual page beside chat. |

## Not in this Expert

Software-build pipelines (`hld-writer`, `dd-writer`, `task-breakdown`, `git-workflow`, and leftover scaffold coding skills) are **not** part of this Expert. Canonical skills plus registered hotel-role jobs cover the loop:

- Starting work → **workflow-selector** + `work-items/<id>/` + **continue**
- Stepping a job → registered workflow file + **continue** / **journal-keeper**
- Checks / human gates → steps inside the workflow file + **operator-qa**
- Pack / evidence → Work Item `out/` and `evidence/` + journal STATUS
- Remember / ingest → **remember** / **integrate-docs**
- Scope / refuse / ask → `MyRole.txt` + `facts/rules-operations.md` + `.cursor/rules/expert.mdc`

## Role jobs (not generic process skills)

Named hotel-role jobs live under `.cursor/workflows/` and `workflow-registry.json`: arrivals-day, departures-due-out, folio-exceptions, group-block-vs-pickup, house-count, night-audit-file-check, no-show-list, ooo-and-status, tax-exempt-completeness.

Tools live under `docs/tools/`.
