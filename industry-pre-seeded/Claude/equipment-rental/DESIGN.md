# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Equipment rental role Expert.

This Expert uses the **canonical expert skills** plus **role workflows** for the rental role. Software-build pipeline skills are **not** part of this Expert. Old generic role-runtime glue is **not** part of this Expert.

Use ordinary words with the person. Finished work is a **pack** in the Work Item `out/` folder. Look in saved files before starting. Think in **parts**. Do not invent missing parts. Multi-step work is a **registered job** under `.claude/workflows/`: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

The Work Item method is `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role in this Expert |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` and the active Work Item journal. One ready workflow step. Continue is not a yes. |
| **define-role** | First session if role is pending; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Update expert and Work Item journals after steps, answers, and session end. |
| **remember** | Save facts/rules into `facts/facts-shared.md` / `facts/rules-shared.md` or the Work Item `facts/` files. |
| **workflow-selector** | Offer only jobs in `.claude/workflows/workflow-registry.json`. |
| **operator-qa** | Clarification and assumption checks under `qa-sessions/`. |
| **promote-facts-rules** | Move durable Work Item notes into shared memory. |
| **switch-context** | Change the active Work Item id. |
| **integrate-docs** | Fold operator docs into operations facts/rules. |
| **memory-optimize** | Health of shared memory files. |
| **visual-page** | Optional visual of a process, timeline, or fleet picture. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not in this Expert

Software-build pipeline skills are not used. Old generic role-runtime glue is not used. Their *behavior* is covered by continue, journal-keeper, workflow-selector, operator-qa, remember, integrate-docs, `MyRole.txt`, `facts/rules-shared.md`, and the role workflow files. Canonical platform skills from the base expert (including pipeline skills) are kept.

## Role jobs

Registered in `.claude/workflows/workflow-registry.json`. Default: `contract-completeness`.

Contract completeness, delivery tickets, maintenance due, meter exceptions, outgoing inspection, renter COI missing, reservation day, return damage, utilization.

## Memory and filing

- Operations facts/rules: `facts/facts-shared.md`, `facts/rules-shared.md`
- Index: `facts/MEMORY-INDEX.md`
- Work Items: `work-items/<id>/` with journals at `journals/work-items/<id>/`
- Tools: `docs/tools/`
