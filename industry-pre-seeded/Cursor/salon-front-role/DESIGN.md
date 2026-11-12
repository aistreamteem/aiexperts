# Expert — skill design

**Updated:** 2026-11-11  
**Folder:** Salon / spa front role expert.

This expert uses the **journals / work-items / operations memory** architecture plus **role workflows**.

Use ordinary words with the person. Finished work is a pack under the Work Item `out/` folder. Look in saved files before starting. Multi-step work is a **work map**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

Role method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` and the active Work Item journal. One ready workflow step. Continue is not a yes. |
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

## Not used on this role

Developer-pipeline skills (hld-writer, dd-writer, task-breakdown, git-workflow, spec-parser, scaffold-project, implement-feature, iterative-feature, refactor, diagram-generator) are not part of this salon front role. Role work uses registered workflows plus continue / journal-keeper / operator-qa / remember / Work Item folders.

## How a salon-role job runs

1. **define-role** only while role status is pending (this seed is already defined).
2. **workflow-selector** + Work Item under `work-items/<id>/`.
3. Read operations memory and the matching `docs/tools/` file.
4. Walk the YAML work map in `.cursor/workflows/<job>.md` — one ready step per continue unless they asked for the whole named job.
5. Checks exit 0 on files in this Work Item’s `work/` or `out/`.
6. **journal-keeper** after the step. **remember** when they correct how this shop works.

## Work map shape

See `.cursor/workflows/README.md`. Data moves only as named files. `in/` / `work/` / `out/` / `evidence/` are inside `work-items/<id>/`.
