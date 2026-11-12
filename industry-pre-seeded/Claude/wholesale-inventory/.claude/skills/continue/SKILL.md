---
name: continue
description: >-
  Resume from the expert journal and active Work Item when they say continue,
  resume, or start. Continue is not a yes and not an answer. Walks one ready
  step on the selected wholesale-inventory workflow.
---

# Continue

## When

They say continue / resume / start where we left off.

## Do not

Treat “continue” as an answer to an open question or as approval of a gate (which on-hand file is live, variance flag-only, publish list). Re-prompt and wait.

## Do

### Role gate

0. Read `MyRole.txt`.
   - If they said “define my role”, run **define-role** and stop.
   - If `Role status` is `pending` or missing, run **define-role** and stop. Do not ask for a Work Item ID.
   - If `defined` or `skipped`, continue.

### Context

0a. Read `.claude/active-context.txt` (`work-item:<id>`). If missing, read `.claude/active-work-item.txt` (legacy fallback only).
0b. If no active Work Item, ask: “Which inventory job should we open? Give a Work Item id (WID-…) or name one receipt, count date, pick, transfer, RMA, or reorder pull.” Write `.claude/active-context.txt` only (do not write the legacy pointer).
0c. Paths:
   - `root_path=work-items/<id>/`
   - `journal_path=journals/work-items/<id>/progress.md`
   - `map_path=journals/work-items/<id>/state.json`
0d. If `work-items/<id>/` is missing, copy `work-items/_TEMPLATE/` (include `in/`, `work/`, `out/`, `evidence/`). If the journal folder is missing, copy `journals/work-items/_TEMPLATE/`. Set `Current work item:` in `journals/expert/progress.md`.
0e. Read the Work Item journal for **Workflow type**. If missing, run **workflow-selector** (registered inventory jobs only; default `receiving-match`). Load `.claude/workflows/<workflow-type>.md`.
0f. Load `facts/MEMORY-INDEX.md`, then `facts/facts-shared.md` and `facts/rules-shared.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`, then `work-items/<id>/facts/facts.md` and `rules.md` if present. Follow rules. Log load counts in the journal.

### One step

1. Read `<journal_path>` and the active node under `journals/work-items/<id>/nodes/`.
2. If Open questions (blocking) is non-empty → ask those. Stop.
3. If Blockers / Last failure is set → describe the block and wait for agreement. Do not invent a workaround.
4. If next action is wait for approval (file choice, variance handling, publish list) → re-prompt. “Continue” does not approve.
5. If next action is empty or done → ask what they want next. At pack completion, offer **promote-facts-rules**.
6. Otherwise perform **one ready step** from the loaded workflow file:
   - Map `in/`, `work/`, `out/`, `evidence/` onto `work-items/<id>/`.
   - Do not start a step whose `needs` files are missing; ask for the source file instead.
   - Read the named tool under `docs/tools/`.
   - Write `produce_path` inside this Work Item.
   - Run the `check`. On fail, retry at most three times, then record the blocker and ask.
   - Do not skip a step with a chat summary.
7. **journal-keeper** after the step: artifacts, checks, next ready step, session summary if stopping.
8. One step per continue unless they asked to run the whole named job — then keep walking steps until the map is complete or blocked.

Method reference: `docs/role/work-item-method.md`.
