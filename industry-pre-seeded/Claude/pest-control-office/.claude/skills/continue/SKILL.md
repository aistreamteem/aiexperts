---
name: continue
description: >-
  Resume from the expert journal and active Work Item when they say continue,
  resume, or start. Continue is not a yes and not an answer. Walks one ready
  step on the selected pest-control office workflow.
---

# Continue

## When

They say continue / resume / start where we left off.

## Do not

Treat “continue” as an answer to an open question or as approval of a gate (missing ticket, missing log field, two disagreeing files, unlabeled target pest). Re-prompt and wait.

## Do

### Role gate

0. Read `MyRole.txt`.
   - If they said “define my role”, run **define-role** and stop.
   - If `Role status` is `pending` or missing, run **define-role** and stop. Do not ask for a Work Item ID.
   - If `defined` or `skipped`, continue.

### Context

0a. Read `.claude/active-context.txt` (`work-item:<id>`). If missing, read `.claude/active-work-item.txt` (legacy read-only fallback).
0b. If no active Work Item, ask: “Which pest-office job should we open? Give a Work Item id (WID-…) or a route day / ticket / pack name (for example 2026-09-15-ticket-118).” Write `.claude/active-context.txt` as `work-item:<id>`. Do not write `.claude/active-work-item.txt` (legacy; read-only fallback remains in hooks).
0c. Paths:
   - `root_path=work-items/<id>/`
   - `journal_path=journals/work-items/<id>/progress.md`
   - `map_path=journals/work-items/<id>/state.json`
   - Step notes live under `journals/work-items/<id>/nodes/`. Write through journal-keeper.
0d. If `work-items/<id>/` is missing, copy `work-items/_TEMPLATE/` (include `in/`, `work/`, `out/`, `evidence/`). If the journal folder is missing, copy `journals/work-items/_TEMPLATE/`. Set `Current work item:` in `journals/expert/progress.md`.
0e. Read the Work Item journal for **Workflow type**. If missing, run **workflow-selector** (registered pest-office jobs only; default `bait-map-index`). Load `.claude/workflows/<workflow-type>.md`.
0f. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`, then `work-items/<id>/facts/facts.md` and `rules.md` if present. Follow rules. Log load counts in the journal.

### One step

1. Read `<journal_path>` and the active node under `journals/work-items/<id>/nodes/`.
2. If Open questions (blocking) is non-empty → ask those. Stop.
3. If Blockers / Last failure is set → describe the block and wait for agreement. Do not invent a workaround.
4. If next action is wait for approval (missing ticket, missing log field, which file is live) → re-prompt. “Continue” does not approve.
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
