# Expert — skill design

**Updated:** 2026-11-11  
**Folder:** Fleet / delivery dispatcher role Expert.

This expert keeps the universal expert architecture (journals, work items, shared/operations facts/rules, registered workflows) and this fleet’s role content. Software-build skills and old role process-glue skills are **not** part of this Expert.

Use ordinary words with the person. No jargon and no confusing analogies. Finished work is a **pack** under the current Work Item `out/`. Look in saved files before starting. Think in **parts**: what each part is, how parts connect, assemble or reassemble a solution. Do not invent missing parts. Multi-step work is a **work map**: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` and the active Work Item journal. One ready workflow step. Continue is not a yes. |
| **define-role** | Ask what this Expert is for; write `MyRole.txt` and stub workflows (including what a command would see if done). |
| **journal-keeper** | Updates expert vs Work Item journals under `journals/`. |
| **remember** | Saves facts, rules, or tool pointers into shared/operations memory or Work Item `facts/`. |
| **workflow-selector** | Offers only jobs in `.claude/workflows/workflow-registry.json`. |
| **operator-qa** | Recorded Q&A under `qa-sessions/`. Forward actions → next dispatch-method step, remember, or a new Work Item. |
| **promote-facts-rules** | Elevate Work Item knowledge into shared or operations Expert Role memory. |
| **switch-context** | Change the active Work Item id. |
| **integrate-docs** | Batch shop notes into shared/operations memory. |
| **memory-optimize** | Health check on shared/operations memory files. |
| **visual-page** | Optional shared visual page. |

## Not used (removed from this seed)

Developer SDLC pipeline skills and old-seed generic process-glue skills are gone. Those needs are covered by continue, journal-keeper, workflow-selector, operator-qa, remember, integrate-docs, MyRole, and the registered workflow files.

## Role method

See `docs/role/work-item-method.md`. Registered jobs live under `.claude/workflows/`. Tools live under `docs/tools/`.

**Later if needed:** archive old rules that never get used.
