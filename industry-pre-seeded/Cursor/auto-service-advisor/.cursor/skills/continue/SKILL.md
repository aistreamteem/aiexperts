---
name: continue
description: >-
  Resume from journals/expert/progress.md and the active Work Item journal
  when they say continue, resume, or start. Continue is not a yes, not an
  answer, and not customer authorization. Walks one ready step of the
  selected service-advisor workflow.
disable-model-invocation: false
---

# Continue

## When

They say continue / resume / start / pick up where we left off.

## Do

1. Read `MyRole.txt`. If **Role status** is `pending`, run **define-role** and stop.
2. Read `journals/expert/progress.md`.
3. Read `.cursor/active-context.txt` (fallback `.cursor/active-work-item.txt`) for the active Work Item id.
4. If no Work Item is active, run **workflow-selector** so the operator picks a registered role job and a Work Item id. Stop if they still need to choose.
5. Read `journals/work-items/<id>/progress.md` and `journals/work-items/<id>/state.json`. Load only the node notes named by `active`. Do not invent a missing path.
6. If open or blocking questions exist → ask those. Stop. Continue is not an answer, not estimate approval, and not a waiver of missing files.
7. If `Workflow type` is missing → **workflow-selector**.
8. Load `facts/MEMORY-INDEX.md`, then the shared pair (`facts/facts-shared.md`, `facts/rules-shared.md`) and the operations pair (`facts/facts-operations.md`, `facts/rules-operations.md`), and the selected file under `.cursor/workflows/`. See `docs/role/work-item-method.md`.
9. Perform **one ready step** from that workflow (or the whole named job if they asked). Rewrite `work/` and `out/` (and checks) to sit under `work-items/<id>/`. Read the tool doc named on the step. Produce the artifact. Run the check. Do not invent VIN, diagnosis, book time, parts ETA, or authorization.
10. **journal-keeper** after the step.

If the next action is wait for auth, a missing export, or operator approval, re-prompt and stop.
