# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Auto shop service advisor role Expert.

This Expert keeps **universal expert infrastructure** (journals, Work Items, operations memory, canonical skills) and **this role's** RO-pack workflows. It does **not** keep a second layer of generic role-process skills from the old seeds. Canonical platform skills from the base expert remain available.

Use ordinary words with the person. No jargon. Finished work is a **file under the Work Item** (`out/` plus check logs in `evidence/`). Look in saved files before starting. Think in **parts**: concern, MPI copy, estimate lines, auth, parts, pickup. Do not invent missing parts.

## Canonical skills (keep)

| Skill | Role |
| --- | --- |
| **define-role** | First session if `MyRole.txt` is pending; stub workflows in the registry |
| **continue** | Resume from `journals/expert/progress.md` + active Work Item; one ready workflow step |
| **journal-keeper** | Expert journal vs Work Item journal under `journals/` |
| **remember** | Facts/rules into shared or operations memory under `facts/`, or Work Item `facts/` |
| **workflow-selector** | Registered role jobs only (`one-ro`, `open-ros`, `mpi-pack`, `estimate-pack`, `auth-gap`, `additional-findings`, `parts-status`, `comeback`, `pickup-invoice`) |
| **operator-qa** | Clarification before inventing shop practice |
| **promote-facts-rules** | Elevate Work Item learnings into shared or operations memory |
| **switch-context** | Change active Work Item |
| **integrate-docs** | Fold shop notes into shared/operations facts/rules |
| **memory-optimize** | Health of facts/rules memory files |
| **visual-page** | Optional visual beside chat |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not used (removed)

Old generic role-process glue is not part of this Expert. Canonical platform skills from the base expert remain. Replacement for deleted glue lives in **continue**, **workflow-selector**, role workflow files, **operator-qa**, **remember**, and `MyRole.txt`.

## Role method

See `docs/role/work-item-method.md`. Work maps live under `.claude/workflows/` and are listed in `workflow-registry.json`. Tools live under `docs/tools/`.
