---
name: continue
description: >-
  Resume from journals when they say continue, resume, start, or pick up
  where we left off. Continue is not a yes and not an answer. Walks one ready
  catering-job step when a Work Item and workflow are active.
---

# Continue

## When

They say continue / resume / start where we left off.

## Do

1. Read `MyRole.txt`. If **Role status** is `pending`, run **define-role** and stop.
2. Read `.cursor/active-context.txt` for `work-item:<id>` (legacy read fallback: `.cursor/active-work-item.txt`). Also read `journals/expert/progress.md`. Prefer the pointer file when both exist.
3. If a Work Item is active, read `journals/work-items/<id>/progress.md` and `journals/work-items/<id>/state.json`. Read only the note files named by `active`.
4. If blocking / open questions are waiting → ask those. Stop. Continue is not an answer and not approval of a human gate.
5. If the journal has no workflow type, run **workflow-selector**, then stop unless they already named a job.
6. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`. Load Work Item facts/rules if present.
7. Open the registered instruction file `.cursor/workflows/<workflow-id>.md`. Follow **one ready step** (needs met, check not yet passed) unless they asked to run the whole named job.
8. Rewrite `work/` and `out/` paths to sit under `work-items/<id>/`. Read the named tool doc. Produce the file. Run the check. On fail, retry at most 3 times, then ask.
9. Run **journal-keeper**: record artifacts, check result, next ready step.

If there is no Work Item and they named a typical catering job (week board, pack-out, count versus guarantee, dietary list, rentals, staffing, leftover forms, change-after-cutoff), run **workflow-selector** to open one.

If `next_action` is empty or done → ask what they want next.

One step per continue unless they asked to run a whole named job (then walk remaining ready steps until complete or blocked).
