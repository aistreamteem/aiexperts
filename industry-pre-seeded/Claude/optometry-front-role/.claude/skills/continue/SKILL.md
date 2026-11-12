---
name: continue
description: >-
  Resume from journals/expert and the active Work Item when they say continue,
  resume, or start. Continue is not a yes and not an answer. Walks one ready
  optometry-role work-map step when a job is active.
---

# Continue

Resumes this optometry front-role expert from the journal. Use when the operator says "continue", "start", or "resume". Continue is **not** approval of a gate and **not** an answer to an open question.

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When the next action is waiting for an answer or approval, "continue" means re-prompt, not "operator answered"

## Instructions

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the operator said "define my role", run **define-role** and stop.
 - If `Role status` is `pending` or the field is missing, run **define-role** and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context initialization

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-21411151`)
 - If file exists: parse type and id
 - If file missing: check `.claude/active-work-item.txt` → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? (work item WID-XXXXXXXX, or name the clinic day / pack)". Parse response:
 - If starts with "WID-": `context_type=work-item`, `context_id=WID-XXXXXXXX`
 - Otherwise treat the named pack as a Work Item id once they confirm the folder name
 - Write `.claude/active-context.txt` as `<type>:<id>`

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<context_id>/`
 - Journal notes live under `journals/work-items/<context_id>/` only.

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke **workflow-selector** → operator selects a registered optometry-role job → reload journal
 - If a legacy **Pipeline** field exists and no Workflow type: map to `day-list` unless they name another registered job
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md`
 - Method overview: `docs/role/work-item-method.md`

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy `work-items/_TEMPLATE/` to `work-items/<context_id>/`
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.

### Facts and rules

0f. Load memory for this optometry role:
 - Always first: `facts/MEMORY-INDEX.md`
 - Expert Role: `facts/facts-operations.md` and `facts/rules-operations.md`
 - Work Item: `work-items/<id>/facts/facts.md` and `.../rules.md` when present
 - Filter Expert Role entries by `**Workflows:**` (`all` or the current registered job id)
 - Follow rules. Facts inform the work. Log load counts in the journal.

### Execution

1. Read `<journal_path>`. If empty, set next action to the first step of the selected workflow.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask those questions and stop. The word "continue" is not an answer.
3. **Blockers:** If Blockers or Last failure is set, describe the block and wait for operator agreement. Do not skip or invent a pass.
4. **Wait for approval:** If next action waits for staff/operator/doctor review, re-prompt with the file path. Do not treat "continue" as approval.
5. **Done or empty:** If next action is empty or done, ask what they want next.
6. **Otherwise perform one ready work-map step:**
 - Paths `work/` and `out/` in the workflow YAML mean **inside** `work-items/<id>/`
 - Do not start a step whose `needs` files are missing — ask for the export or prior artifact
 - Read the named `docs/tools/` file
 - Write `produce_path` under the Work Item
 - Run the step `check` (typically `python docs/tools/checks/...` with paths under the Work Item)
 - On fail: retry at most 3 times, then ask
 - Pass the produced file to later steps; do not skip with a chat summary
 - One step per continue unless they asked to run the whole named job (then walk remaining ready steps until complete or blocked)
7. After the step, run **journal-keeper**: artifacts, checks, blockers, next ready step.
8. At session end, write **Last session summary** in the Work Item journal and optionally refresh `work-items/<id>/STATUS.md`.
9. When the Work Item reaches done, ask whether to run **promote-facts-rules**.

The selected workflow file plus this skill is enough to walk the job.
