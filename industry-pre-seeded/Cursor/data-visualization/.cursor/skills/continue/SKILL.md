---
name: continue
description: >-
  Resume from journals/expert/progress.md and the active Work Item journal
  when they say continue, resume, or pick up where we left off. Continue is
  not a yes and not an answer. Walks one ready step of the selected chart
  workflow.
disable-model-invocation: false
---

# Continue

## When

They say continue / resume / start where we left off.

## Do

1. Read `MyRole.txt`. If **Role status** is `pending`, run **define-role** and stop.
2. Read `journals/expert/progress.md`. Read `.cursor/active-context.txt` / `.cursor/active-work-item.txt` if present.
3. If there is no active Work Item, run **workflow-selector** (offer registered chart jobs only). Stop after that skill records the job, unless they already named the job and source file in this message.
4. Read `journals/work-items/<id>/progress.md` and `journals/work-items/<id>/state.json`. Load `facts/MEMORY-INDEX.md`, then shared facts/rules, then operations facts/rules, then this Work Item’s facts/rules.
5. If Open questions / blocking questions are non-empty → ask those. Stop. Continue is not an answer.
6. If Next action is wait for operator / wait for approval → re-prompt for the answer or explicit approval. Do not advance.
7. Read the selected workflow file from `.cursor/workflows/` (see `workflow-registry.json`). Find the next ready step: needs are present as files under `work-items/<id>/`, the step is not yet passed, and its gate (named question, columns, file, package) is clear.
8. Do **one** ready step: read the tool doc, produce the file at `produce_path` inside the Work Item folder, run the check from that folder. On failure retry at most three times, then report the blocker.
9. **journal-keeper** after the one step.

One step per continue unless they asked to run a whole named job (then walk remaining steps until the map is complete or blocked). Live state is `journals/expert/` plus `journals/work-items/<id>/`. Job files live under `work-items/<id>/`.
