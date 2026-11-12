# Expert — skill design

**Updated:** 2026-11-08  
**Folder:** childcare-admin — Childcare center office (not the teacher).

This Expert keeps **canonical expert skills** plus **this role’s** work maps, tools, and operations memory. Software-build pipelines and the old generic role process layer are not part of the Expert.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a pack under `work-items/<id>/out/`. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble or reassemble a solution. Do not invent missing parts. Multi-step work is a **work map**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Role method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/` + active Work Item journal. One ready work-map step. Continue is not a yes. |
| **define-role** | Ask what this Expert is for; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Update expert vs Work Item journals after a step, decision, or session end. |
| **remember** | Save facts/rules into shared or operations memory, or the Work Item `facts/` files. |
| **workflow-selector** | Offer only registered childcare-office jobs from `workflow-registry.json`. |
| **operator-qa** | Clarify with the operator; close into `qa-sessions/Q*/conclusions.md`. |
| **promote-facts-rules** | Elevate Work Item notes into shared or operations memory. |
| **switch-context** | Change the active Work Item. |
| **integrate-docs** | Fold operator docs into shared/operations memory. |
| **memory-optimize** | Health-check shared and operations memory files. |
| **visual-page** | Optional shared visual page. |

Leftover scaffold folders (`spec-parser`, `scaffold-project`, `implement-feature`, `iterative-feature`, `refactor`, `diagram-generator`) are **not** part of this role’s loop.

Scope, refuse, conflict, and “ask don’t invent” live in `MyRole.txt` and `facts/rules-operations.md` / `facts/rules-shared.md`. Tool how-to lives in `docs/tools/`. Job steps live in `.cursor/workflows/`. Evidence lives in `work-items/<id>/evidence/`.

## Role content (not skills)

- Work maps: `.cursor/workflows/*.md` + `workflow-registry.json`
- Tools: `docs/tools/`
- Memory: `facts/facts-shared.md`, `facts/rules-shared.md`, `facts/facts-operations.md`, `facts/rules-operations.md`, `facts/MEMORY-INDEX.md`

## Work items

Each real job is `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`. Journals: `journals/expert/progress.md` and `journals/work-items/<id>/`.
