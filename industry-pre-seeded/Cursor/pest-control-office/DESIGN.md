# Expert — skill design

**Updated:** 2026-11-08
**Folder:** Pest control office role expert.

This expert uses the **journals / work-items / operations memory** architecture plus **role workflows**.

Use ordinary words with the person. Finished work is a pack under the Work Item `out/` folder. Look in saved files before starting. Think in **parts**: route rows, tickets, skips, callbacks, log fields, inventory names, bait-map ids, WDO form pages. Do not invent missing parts. Multi-step work is a **work map**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Role method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` and the active Work Item journal. One ready pest-office step. Continue is not a yes. |
| **define-role** | If role status is pending, ask and write `MyRole.txt` plus workflow stubs. |
| **journal-keeper** | Update expert vs Work Item journals and node notes after each step. |
| **remember** | Save facts/rules into operations memory or Work Item `facts/`. |
| **workflow-selector** | Offer only jobs in `.cursor/workflows/workflow-registry.json`. |
| **operator-qa** | Clarification sessions under `qa-sessions/`. |
| **promote-facts-rules** | Elevate Work Item learnings into `facts-operations` / `rules-operations`. |
| **switch-context** | Change active Work Item id. |
| **integrate-docs** | Batch-ingest shop notes into operations memory. |
| **memory-optimize** | Health check on operations memory files. |
| **visual-page** | Optional picture of a list or flow when they ask to see it. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Role jobs (not skills)

Pest control office jobs live in `.cursor/workflows/` and the registry. Method: `docs/role/work-item-method.md`.

bait-map-index, callback-list, chemical-log-completeness, device-count, estimate-from-price, inventory-chem-vs-log, route-day, skip-list, wdo-form-completeness.

## Not used on this role

Role work uses registered workflows plus continue / journal-keeper / operator-qa / remember / Work Item folders.

## How a pest-office job runs

1. **define-role** only while role status is pending (this seed is already defined).
2. **workflow-selector** + Work Item under `work-items/<id>/`.
3. Read operations memory and the matching `docs/tools/` file.
4. Walk the YAML work map in `.cursor/workflows/<job>.md` — one ready step per continue unless they asked for the whole named job.
5. Checks exit 0 on files in this Work Item’s `work/` or `out/`.
6. **journal-keeper** after the step. **remember** when they correct how this shop works.

## Work map shape

See `.cursor/workflows/README.md`. Data moves only as named files. `in/` / `work/` / `out/` / `evidence/` are inside `work-items/<id>/`.

## Memory

- Index: `facts/MEMORY-INDEX.md`
- Facts: `facts/facts-operations.md`
- Rules: `facts/rules-operations.md`
- Tools: `docs/tools/`
