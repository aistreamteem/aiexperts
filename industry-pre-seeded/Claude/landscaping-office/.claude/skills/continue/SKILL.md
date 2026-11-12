---
name: continue
description: >-
  Use when the user says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active journal and performs the next landscaping-office workflow step.
  Does NOT mean approval of a gate or an answer to an open question.
disable-model-invocation: false
---

# Continue

Resume this landscaping / lawn-care office Expert from the journals. Perform **one ready step** of the selected registered workflow unless the operator asked to run the whole named job.

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When waiting for an answer (missing ticket, missing price, weather not called, extra-work auth, commercial PO), "continue" means **re-prompt**, not "they answered"

## Instructions

**Do not** treat "continue" as an answer or as approval. If the next step waits for a shop decision or a missing file, ask again and do not advance.

### Role gate

0. Read `MyRole.txt`.
   - If the operator said "define my role", run **define-role** and stop.
   - If `Role status` is `pending` or missing, run **define-role** and stop. Do not ask for a Work Item ID yet.
   - If `defined` or `skipped`, continue.

### Context

0a. Read `.claude/active-context.txt` (`<type>:<id>`, e.g. `work-item:WID-21411151` or `work-item:2026-09-15-crew-a`). If missing, check `.claude/active-work-item.txt`. If both missing, ask: "Which job is this? Give a Work Item id (crew day, property + date, ticket, or week)."

0b. For a work-item:
   - `root_path=work-items/<id>/`
   - `journal_path=journals/work-items/<id>/progress.md`
   - `map_path=journals/work-items/<id>/state.json`
   - There is no `work-items/<id>/journal/` pointer; use `journals/work-items/<id>/`.

0c. If `root_path` does not exist, copy `work-items/_TEMPLATE/` there. If `journals/work-items/<id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<id>/`. Write `Current work item: <id>` in `journals/expert/progress.md`.

### Workflow

0d. Read `<journal_path>` for **Workflow type**.
   - If missing, run **workflow-selector** and reload the journal.
   - If an old **Pipeline** field exists, map it to a registered role job: default `callback-list` unless they named another job from the registry.
   - Read `.claude/workflows/workflow-registry.json`. Load `.claude/workflows/<workflow-type>.md`.
   - Use `docs/role/work-item-method.md` for phase meaning. Do **not** use a software-build design pipeline.

### Memory

0e. Load `facts/MEMORY-INDEX.md`, then the shared pair `facts/facts-shared.md` and `facts/rules-shared.md`, then `work-items/<id>/facts/` if present. Follow rules; use facts as context. Log how many were loaded.

### Execute

1. Read `<journal_path>`. If empty, initialize from template, set next action to the first step of the selected workflow.
2. If Open questions (blocking) is non-empty, ask those questions. Stop. "Continue" is not an answer.
3. If Blockers / Last failure is set, describe the block and wait for the operator’s agreement before retrying.
4. If next action is waiting for operator (missing ticket, blank price, weather not called, extra-work auth, commercial PO, estimate-draft acceptance), re-surface the ask. Do not advance.
5. If next action is empty or done, stop and ask what they want next.
6. Otherwise perform **one ready step** from the loaded workflow file:
   - Do not start if `needs` files are missing under this Work Item.
   - Read the cited file in `docs/tools/`.
   - Write `produces` to `produce_path` **inside** `root_path` (so `work/` and `out/` mean `work-items/<id>/work/` and `.../out/`).
   - Run the listed `check` against those same paths. Retry at most 3 on failure, then ask.
   - Do not invent a ticket, price, dump fee, hours, wage, chemical mix, or weather call.
7. Run **journal-keeper**: step completed or blocked, artifacts, next ready step.
8. At session end, write **Last session summary** on the Work Item journal and optionally refresh `<root_path>/STATUS.md`.

If the operator asked to run the **whole named job**, keep walking ready steps until the map is complete or blocked. Still stop on blocking questions.

## Quick open

- "continue" with no Work Item → ask which crew day / ticket / week, then **workflow-selector**.
- Typical daily job → **crew-day**. Typical quote → **estimate-from-price**. Weather leftovers → **weather-postpone-list** only after they called weather.
