---
name: continue
description: >-
  Use when the user says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active journal and performs the next moving-office workflow step. Does NOT
  mean approval of a gate or an answer to an open question.
---

# Continue

Resumes the moving-company office role from the journals. Use when the user says "continue", "start", or "resume" so the agent reads the journal and performs the next ready step.

## When to use

- User says "continue", "start", or "resume"
- User asks to pick up where the role left off
- When the job is waiting for an answer or approval, "continue" means re-prompt, not "user answered" or "user approved"

## Instructions

**Do not** treat the user saying "continue" as an answer to a question or as approval/waiver of a gate. "Continue" means only: read the journal and perform the next step. If that step is waiting for an answer or for approval, re-prompt and do **not** advance until the user gives a substantive answer or explicitly approves/waives. The word "continue" by itself is not an answer and is not approval.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the user said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context Initialization (Steps 0a-0e)

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151` or `work-item:2026-09-15-est-9021`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.claude/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "Which move, estimate, or pack is this? Give a Work Item id (WID-… or a folder name like 2026-09-15-est-9021)." Parse response, write `.claude/active-context.txt` as `work-item:<id>`. Do not write the legacy `.claude/active-work-item.txt`.

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → operator picks a registered job → reload journal
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md`
 - Use that file for phase sequence, human gates, artifacts, and checks
 - Default new job when the operator has not named one: `estimate-from-rate-file`

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy structure from `work-items/_TEMPLATE/`
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.

### Facts and Rules Loading (Step 0f)

0f. Load memory for this moving-office role:
 - Read `facts/MEMORY-INDEX.md` first
 - Load shared: `facts/facts-shared.md` + `facts/rules-shared.md`
 - Load operations: `facts/facts-operations.md` + `facts/rules-operations.md`
 - Read `work-items/<context_id>/facts/facts.md` and `work-items/<context_id>/facts/rules.md` when present
 - Filter Expert Role entries by `**Workflows:**` (include `all` or the current job id)
 - Follow rules; use facts as context. Log conflicts in the journal

### Execution

1. **Read context journal:** `<journal_path>`. If missing or empty, initialize from template, set workflow from 0d, set next action to the first step of that workflow.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask those questions and do not advance. **The word "continue" is not an answer.**
3. **Blockers / Last failure:** Describe the block, what is needed, and wait for agreement. Do not invent a rate, weight, cube, crew name, or delivery hour to work around a missing file.
4. **Wait for approval / operator action:** If next action is waiting (live rate file, binding type, send estimate, dispatch, collect high-value list, name claims owner), re-surface the ask. Do not treat "continue" as approval.
5. **Done or empty:** If next action is empty or "done", stop and optionally ask what they want next.
6. **Otherwise perform the single next step** from the loaded workflow file:
 - Paths are under `<root_path>` (`in/`, `work/`, `out/`, `evidence/`)
 - Read the named `docs/tools/` file
 - Produce the artifact at `produce_path`
 - Run the check command from `<root_path>` (or with paths relative to it). Exit 0 = pass
 - On fail: retry at most 3, then record the blocker and ask
 - One step per continue unless they asked to run the whole named job (then walk remaining steps until complete or blocked)
7. After the step, **journal-keeper**: last completed, next action, artifacts, checks, decisions.
8. At session end, write **Last session summary** in the context journal and optionally refresh `<root_path>/STATUS.md`.
9. When the Work Item reaches done, ask whether to run **promote-facts-rules**.

Role method: `docs/role/work-item-method.md`. Do not look for `journal/state.json`, `items/`, or deleted process skills.
