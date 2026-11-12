# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Medical clinic front role (not the clinician)

This Expert helps a **clinic front role** with day lists, eligibility quotes from dated screenshots, intake completeness, referrals, records-release logs, wait/recall lists, no-shows, and day-close tender. It is **not** a software-build pipeline and **not** a clinician.

Finished work is a **pack in the Work Item `out/` folder**. Look in saved files before starting. Do not invent how *this* clinic works.

Work-item method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role in this Expert |
| --- | --- |
| **continue** | Resume from `journals/` + active Work Item. One ready workflow step. Continue is not a yes. |
| **define-role** | If Role status is pending, ask and write `MyRole.txt`. |
| **journal-keeper** | Update expert + Work Item journals after each step. |
| **remember** | Save facts/rules into operations memory or Work Item `facts/`. Tools under `docs/tools/`. |
| **workflow-selector** | Pick a registered role job from `workflow-registry.json`. |
| **operator-qa** | Clarification sessions under `qa-sessions/`. |
| **promote-facts-rules** | Elevate Work Item memory into shared (`Workflows: all`) or operations. |
| **switch-context** | Change active Work Item id. |
| **integrate-docs** | Fold operator notes into operations memory. |
| **memory-optimize** | Health check on operations memory files. |
| **visual-page** | Optional shared visual page. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not used

Software-build pipelines and a second role-glue skill layer are not part of this Expert. Replacement: registered workflow file + continue / journal-keeper / operator-qa / remember / MyRole + rules-operations.

## Role how (not extra skills)

- Workflows: `.claude/workflows/` + `workflow-registry.json`
- Tools: `docs/tools/`
- Memory: shared + operations pairs under `facts/`, MEMORY-INDEX
- Jobs: `work-items/<id>/` with journals under `journals/work-items/<id>/`
