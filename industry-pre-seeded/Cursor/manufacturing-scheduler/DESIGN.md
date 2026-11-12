# Expert — skill design

**Updated:** 2026-11-08  
**Folder:** this production-scheduler Expert. Role: **Small-plant production scheduler**.

Keep the expert architecture: `journals/`, `work-items/`, `qa-sessions/`, `facts/facts-operations.md` + `facts/rules-operations.md`, `.cursor/workflows/` + registry. Role method: `docs/role/work-item-method.md`.

Use ordinary shop words with the person. Finished work is a pack in `work-items/<id>/out/` that quotes their exports. Look in saved files before starting. Do not invent cycle times, yields, setup, ATP, or promise dates. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0 or a documented exception is recorded.

## Canonical expert skills (keep)

| Skill | Role in this Expert |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` + active Work Item. One ready scheduler step. Continue is not a yes. |
| **define-role** | First session if Role status is pending; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Expert vs Work Item journals under `journals/`. |
| **remember** | Facts/rules into operations memory or the Work Item; tools under `docs/tools/`. |
| **workflow-selector** | Registered shop jobs only (dispatch, kit, shortage, traveler, …). |
| **operator-qa** | Clarification sessions under `qa-sessions/`. |
| **promote-facts-rules** | Elevate Work Item memory into `facts-operations` / `rules-operations`. |
| **switch-context** | Change active Work Item id. |
| **integrate-docs** | Batch shop docs into operations memory. |
| **memory-optimize** | Health of operations memory files. |
| **visual-page** | Optional visual of a board or flow. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not used (removed)

Software-delivery pipeline skills and old role-runtime glue are **not** part of this Expert. Their jobs are covered by Work Items, registered workflow files, continue / journal-keeper / remember / operator-qa, and `MyRole.txt` constraints.

## Workflow files

Each shop job is a self-contained instruction file under `.cursor/workflows/` with a YAML map (`needs` / `produces` / `tool` / `check`). **continue** walks one ready step. Tools are cited from `docs/tools/`. Default job: `dispatch-list`.
