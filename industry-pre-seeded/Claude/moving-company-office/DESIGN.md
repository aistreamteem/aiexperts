# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Moving company office role Expert.

This Expert keeps the universal expert architecture (journals, Work Items, operations memory, registered workflows) and this shop’s moving-office jobs. It does **not** run a software HLD → DD → implement pipeline and does **not** keep a parallel role-runtime skill layer.

Use ordinary words with the person. Finished work is a pack in the Work Item `out/` folder. Look in saved files before starting. Think in **parts**. Do not invent missing parts. Multi-step work is a registered **workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` and the active Work Item journal. One ready workflow step. Continue is not a yes. |
| **define-role** | First session if role is pending; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Expert journal + Work Item journal/`state.json`/node notes. |
| **remember** | Facts and rules into `facts/facts-operations.md` / `facts/rules-operations.md` or Work Item memory. |
| **workflow-selector** | Registered moving-office jobs only (`workflow-registry.json`). |
| **operator-qa** | Clarification sessions under `qa-sessions/`. |
| **promote-facts-rules** | Elevate Work Item memory into operations memory. |
| **switch-context** | Change active Work Item. |
| **integrate-docs** | Fold operator docs into operations memory. |
| **memory-optimize** | Health of operations memory files. |
| **visual-page** | Optional shared visual page. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not used (removed)

Software-only: implement-feature, hld-writer, dd-writer, spec-parser, scaffold-project, test-writer, refactor, git-workflow, diagram-generator, iterative-feature, task-breakdown.

Old role-runtime glue: start-job, run-map, run-until-check, write-up, write-check, verifier, after-task, playbook-keeper, tool-operator, read-saved-files, first-principles, ask-dont-invent, conflict-check, refuse-outside-role, ingest-example, teach, orchestrate-subagents.

Those needs are covered by Work Items + registered workflows + continue / journal-keeper / operator-qa / remember / `MyRole.txt` / rules-operations.

## Role jobs

See `docs/role/work-item-method.md` and `.claude/workflows/`. Default new job: `estimate-from-rate-file`.
