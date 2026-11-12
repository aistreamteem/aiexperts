# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Nonprofit office admin role expert.

This expert keeps the universal expert architecture (journals, work-items, shared facts/rules, registered workflows) and role content for a small nonprofit office. Software-build skills (design docs, implement, tests, git) are **not** part of this role. Old generic role-runtime glue is **not** part of this role.

Use ordinary words with the person. Finished work is a pack under `work-items/<id>/out/` plus journal STATUS. Look in saved files before starting. Think in **parts**. Do not invent missing parts. Multi-step work is a **work map**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Work-item method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/` and run one ready workflow step |
| **define-role** | Role pending: write `MyRole.txt` and stub workflows |
| **journal-keeper** | Expert journal + Work Item journal/`state.json` |
| **remember** | Facts/rules into shared or Work Item memory |
| **workflow-selector** | Pick a registered role job from `workflow-registry.json` |
| **operator-qa** | Focused Q&A under `qa-sessions/` |
| **promote-facts-rules** | Elevate Work Item memory into shared |
| **switch-context** | Change active Work Item |
| **integrate-docs** | Fold dropped handbooks into shared memory |
| **memory-optimize** | Health of shared memory files |
| **visual-page** | Optional visual for a list, timeline, or packet map |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Role workflows (not skills)

Named jobs live under `.claude/workflows/` and in `workflow-registry.json`: board-pack, donor-list, funder-gap, gift-ack-draft, grant-deadlines, grant-report, in-kind-list, minutes-index, restricted-ask.

Default: `board-pack`.

## Not in this expert

No software-build pipeline and no parallel role-runtime skill layer. Replacement mapping:

- Starting work → **workflow-selector** + `work-items/<id>/` + **continue**
- Stepping a job → the workflow file itself + **continue** / **journal-keeper**
- Checks / human gates → steps inside the workflow file + **operator-qa**
- Pack evidence → Work Item `out/` / `evidence/` + journal STATUS
- Remember / ingest → **remember** / **integrate-docs**
- Scope / refuse / conflict → `MyRole.txt` + `facts/rules-shared.md` + `.claude/rules/expert.md`
- Tools → `docs/tools/` cited from the workflow file
