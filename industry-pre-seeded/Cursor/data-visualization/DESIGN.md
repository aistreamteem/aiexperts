# Expert — skill design

**Updated:** 2026-11-08
**Folder:** this Expert — **Data visualization from their files**.

Software-build pipeline skills are **not** part of this role. Old role-runtime process skills are **not** part of this role either. Process needs are covered by canonical expert skills plus role workflow files.

Use ordinary words with the person. Finished work is a **write-up file** under the current Work Item `out/` plus named PNG/CSV artifacts. Look in saved journals and operations memory before starting. Think in **parts**: question, columns, table behind the chart, picture, write-up. Do not invent missing parts. Multi-step work is a **registered workflow**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/`; one ready workflow step. Continue is not a yes. |
| **define-role** | Pending role only; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Expert vs Work Item journals under `journals/`. |
| **remember** | Facts/rules into operations memory or Work Item `facts/`. |
| **workflow-selector** | Menu from `.cursor/workflows/workflow-registry.json`. |
| **operator-qa** | Clarifying question, columns, or notes before persist. |
| **promote-facts-rules** | Elevate Work Item memory into operations files. |
| **switch-context** | Change active Work Item. |
| **integrate-docs** | Batch notes into operations memory. |
| **memory-optimize** | Health of operations memory files. |
| **visual-page** | Optional shared visual page beside chat. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Role how (not skills)

- Work Item method: `docs/role/work-item-method.md`
- Jobs: `.cursor/workflows/*.md` + `workflow-registry.json`
- Tools: `docs/tools/`
- Memory: `facts/facts-operations.md`, `facts/rules-operations.md`

## Not used on this role

Software-build pipeline skills and old role-runtime process skills were removed. Behavior lives in the method note, registered workflow files, `MyRole.txt`, operations rules, and the canonical expert skills above.

## Adding a repeating pack

If they approve a new job twice, add `.cursor/workflows/<id>.md`, register it, and point `MyRole.txt` / `AGENTS.md` at it.
