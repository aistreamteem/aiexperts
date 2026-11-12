---
name: continue
description: >-
  Resume from the expert journal and active Work Item when they say continue,
  resume, or start. Continue is not a yes and not an answer. Walks one ready
  step of this landscaping-office job.
---

# Continue

Resume this landscaping / lawn-care office Expert from the journals. Perform **one ready step** of the selected registered workflow unless the operator asked to run the whole named job.

## When

They say continue / resume / start / pick up where we left off.

## Do not

Do not treat “continue” as an answer to an open question or as approval of a pack, exception, or gate. If the next step is waiting for a shop decision or a missing file (ticket, price, weather not called, extra-work auth, commercial PO), re-ask and stop.

## Do

### Role gate

0. Read `MyRole.txt`.
   - If they said “define my role”, run **define-role** and stop.
   - If `Role status` is `pending` or missing, run **define-role** and stop. Do not ask for a Work Item ID yet.
   - If `defined` or `skipped`, continue.

### Context

0a. Read `.cursor/active-context.txt` (`work-item:<id>`). If missing, read `.cursor/active-work-item.txt` (legacy read fallback only).
0b. If no active Work Item, ask: “Which job is this? Give a Work Item id (crew day, property + date, ticket, or week).” Parse WID- as `context_id`. Write `.cursor/active-context.txt` as `work-item:<id>` (do not write the legacy pointer).
0c. Paths:
   - `root_path=work-items/<id>/`
   - `journal_path=journals/work-items/<id>/progress.md`
   - `map_path=journals/work-items/<id>/state.json`
   - Node notes: `journals/work-items/<id>/nodes/<active leaf>.md`
0d. Read `journal_path` for **Workflow type**. If missing, run **workflow-selector**, then reload. If an old **Pipeline** field exists, map it to a registered role job: default `callback-list` unless they named another job from the registry. Load `.cursor/workflows/workflow-registry.json` and the instruction file. Follow `docs/role/work-item-method.md`. Do **not** use a software-build design pipeline.
0e. If `work-items/<id>/` is missing, copy `work-items/_TEMPLATE/` (include `in/`, `work/`, `out/`, `evidence/`). If the Work Item journal is missing, copy `journals/work-items/_TEMPLATE/` and set **Work item record** to `work-items/<id>/`. Set `Current work item:` in `journals/expert/progress.md`.
0f. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`, then `work-items/<id>/facts/` if present. Log counts in the journal. Default workflow memory is **operations** for this role.

### One ready step

1. Read the Work Item journal. If empty, set next action to the first step of the selected workflow.
2. If Open questions (blocking) is non-empty → ask those. Stop.
3. If Blockers or Last failure is set → describe the block, ask how to proceed, stop.
4. If next action is wait for operator / wait for pack review / wait for source files → re-prompt. Stop. “Continue” is not approval.
5. If next action is empty or done → ask what they want next.
6. Otherwise perform **one** ready step from the loaded workflow file (or the whole named job if they asked for the whole job):
   - Do not start if `needs` files are missing under this Work Item.
   - Read the cited file in `docs/tools/`.
   - Write `produces` to `produce_path` **inside** `root_path` (so `work/` and `out/` mean `work-items/<id>/work/` and `.../out/`).
   - Run the listed `check` against those same paths. Retry at most 3 on failure, then ask.
   - Do not invent a ticket, price, dump fee, hours, wage, chemical mix, or weather call.
7. After the step, **journal-keeper**: last completed, artifacts, next action, checks.
8. At session end, write Last session summary and optionally refresh `STATUS.md`.
9. When the Work Item is done, offer **promote-facts-rules**.

Paths in the workflow YAML (`work/`, `out/`) are relative to `work-items/<id>/`.

## Quick open

- "continue" with no Work Item → ask which crew day / ticket / week, then **workflow-selector**.
- Typical daily job → **crew-day**. Typical quote → **estimate-from-price**. Weather leftovers → **weather-postpone-list** only after they called weather.
