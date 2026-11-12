---
name: continue
description: >-
  Use when the operator says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active Work Item journal and performs the next clinic-role workflow step.
  Does NOT mean approval of a gate or an answer to an open question.
disable-model-invocation: false
---

# Continue

Resumes this clinic front-role Work Item from the journal. Use when the operator says "continue", "start", or "resume".

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When the workflow is waiting for an answer or approval, "continue" means re-prompt, not "operator answered" or "operator approved"

## Instructions

**Do not** treat the operator saying "continue" as an answer to a question or as approval/waiver of a gate. "Continue" means only: read the journal and perform the next ready step. If that step is waiting for an answer or for approval, re-prompt and do **not** advance until the operator gives a substantive answer or explicitly approves/waives. Role questions use the same rule: "I approve the role" or "Skip role definition" is the approval, not the word continue.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the operator said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context initialization (Steps 0a-0e)

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151` or `work-item:2026-11-10-day-appointments`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.claude/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? Give a Work Item ID (WID-XXXXXXXX) or a clinic-date / pack name (for example `2026-11-10-day-appointments`)." Parse response, set `context_type=work-item`, `context_id=<id>`. Write `.claude/active-context.txt` as `work-item:<id>`. Do not write the legacy `.claude/active-work-item.txt`.

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → operator selects a registered role job → reload journal
 - If an old "Pipeline" field exists but no Workflow type: map leftover software-build or incident names to the default role job `day-appointments` unless they already named another registered job
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md`
 - Also read `docs/role/work-item-method.md` for this role’s phases and gates

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy structure from `work-items/_TEMPLATE/`
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.
 - Ensure `in/`, `work/`, `out/`, and `evidence/` exist under the Work Item.

### Facts and rules (Step 0f)

0f. Load memory for this clinic role:
 - Always first: `facts/MEMORY-INDEX.md`
 - Then shared: `facts/facts-shared.md` + `facts/rules-shared.md`
 - Then Expert Role operations: `facts/facts-operations.md` + `facts/rules-operations.md`
 - Then Work Item: `work-items/<context_id>/facts/facts.md` and `work-items/<context_id>/facts/rules.md` when present
 - Filter Expert Role entries by `**Workflows:**` (`all` or the current role job id)
 - Rules MUST be followed. Starter notes are guesses until this clinic corrects them.
 - Log loaded counts in the Work Item journal

### Perform one ready step

1. If the journal has open blocking questions → ask those. Stop. **The word "continue" is not an answer.**
2. If next action is wait for operator / approval → re-prompt. Stop.
3. Open the selected workflow file. Find the first step whose `needs` files exist under this Work Item and whose produced file is not yet present (or whose check has not passed).
4. Read the named tool doc under `docs/tools/`. Produce the file at `produce_path` resolved **inside** `work-items/<id>/`. Run the listed `check` from that Work Item folder if present.
5. On check fail: retry at most three times, then ask. Do not invent a pass.
6. Run **journal-keeper**: record artifacts, checks, decisions, next action.
7. One step per continue unless the operator asked to run the whole named job — then walk remaining ready steps until blocked or the map is complete.

If no ready step remains and required outputs exist, set next action to complete (or promote-facts-rules if the operator wants a promotion review).
