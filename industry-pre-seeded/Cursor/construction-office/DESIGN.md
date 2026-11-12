# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Construction office coordinator role Expert.

This Expert keeps **universal expert infrastructure** (journals, Work Items, shared memory, canonical skills) and **this role’s jobs** (daily logs, RFIs, submittals, punch, COIs, change registers, look-aheads, minutes, closeout). It does not keep a software-build pipeline and it does not keep a second layer of generic role-runtime skills.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a **pack in `out/`** that quotes their files. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble a solution. Do not invent missing parts. Multi-step work follows `docs/role/work-item-method.md` and the YAML steps in `.cursor/workflows/`.

## Canonical expert skills (keep)

| Skill | Role in this Expert |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` + active Work Item journal. One ready method step. Continue is not a yes. |
| **define-role** | Ask what this Expert is for; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Update expert vs Work Item journals under `journals/`. |
| **remember** | Save facts/rules to shared memory or the Work Item `facts/` folder. |
| **workflow-selector** | Offer only jobs in `workflow-registry.json`. |
| **operator-qa** | Clarification session under `qa-sessions/`. |
| **promote-facts-rules** | Elevate Work Item memory into `facts/facts-shared.md` / `facts/rules-shared.md`. |
| **switch-context** | Change active Work Item id. |
| **integrate-docs** | Fold operator docs into shared memory. |
| **memory-optimize** | Health check on shared memory files. |
| **visual-page** | Optional visual page beside chat. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not in this Expert

Software-build design/implement skills are not used. Old generic role-runtime skills are not used either. Starting work, stepping a job, checks, packs, and scope live in **continue**, **journal-keeper**, **workflow-selector**, **operator-qa**, **remember**, Work Item folders, `MyRole.txt`, and the role workflow files. Canonical platform skills from the base expert (including pipeline skills) are kept.

## Role method

See `docs/role/work-item-method.md`. Shared phases: intake → extract → exception pass → pack → operator review → close.

## Work items

Each real job is `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`. Journals: `journals/expert/progress.md` and `journals/work-items/<id>/`.
