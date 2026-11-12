---
name: continue
description: >-
  Use when the operator says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active journal and performs the next nonprofit-office workflow step.
  Does NOT mean approval of a gate or an answer to an open question.
---

# Continue

Resumes the active Work Item from the journals. Use when the operator says "continue", "start", or "resume".

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When the workflow is waiting for an answer or approval, "continue" means re-prompt, not "operator answered" or "operator approved"

## Instructions

**Do not** treat "continue" as an answer to a question or as approval/waiver of a gate. If the next action waits for an answer or for approval, re-prompt and do **not** advance until the operator gives a substantive answer or explicitly approves/waives. Role questions use the same rule: "I approve the role" or "Skip role definition" is the approval, not the word continue.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the operator said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context Initialization (Steps 0a-0e)

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151`)
 - If file exists: parse type and id
 - If file missing: check `.claude/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? (work item WID-XXXXXXXX, or name the meeting / grant / gift batch)". Parse response:
 - If starts with "WID-": `context_type=work-item`, `context_id=WID-XXXXXXXX`
 - Otherwise mint or reuse a filesystem-safe Work Item id and still store it as `work-item:<id>`
 - Write `.claude/active-context.txt` as `<type>:<id>`

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - Node notes: `journals/work-items/<context_id>/nodes/<active leaf>.md`
 - Do not recreate `work-items/<context_id>/journal/progress.md`

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → operator selects a registered role job → reload journal
 - Do **not** map unknown pipelines to a software-build default
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md` (and `docs/role/work-item-method.md`)
 - Default workflow if they do not name a job: `board-pack`

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy `work-items/_TEMPLATE/` to `work-items/<context_id>/`
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.

### Facts and Rules Loading (Step 0f)

0f. Load memory for this nonprofit-office role:
 - Read `facts/MEMORY-INDEX.md`
 - Read `facts/facts-shared.md` and `facts/rules-shared.md`
 - Read `<root_path>/facts/facts.md` and `<root_path>/facts/rules.md` when present
 - Filter Expert Role entries by `**Workflows:**` (include `all` or the current workflow id)
 - Rules must be followed. Facts do not authorize invention.
 - Log loaded counts in the journal. Note conflicts under "Rule violations / conflicts"

### Pipeline Execution

1. **Read context journal:** `<journal_path>`. If missing, initialize from template (0e), set workflow from 0d, set next action to the first ready step of that workflow.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask those questions and do not advance. **The word "continue" is not an answer.**
3. **Blockers / Last failure:** Describe the block, discuss how to proceed, wait for agreement. Do not skip or invent a workaround.
4. **Wait for approval:** If next action waits for operator review (packet review, fiscal-year answer, restriction coding, send/submit confirmation), re-surface the item. Do not record approval until they say so explicitly. Continue is not permission to send, submit, spend, or certify.
5. **Done or empty:** If next action is empty or "done", stop and optionally ask what they want next. Offer **promote-facts-rules** when the Work Item is done.
6. **Otherwise perform the single next ready step** from the loaded workflow file:
 - Paths `in/`, `work/`, `out/`, `evidence/` are inside `<root_path>`
 - Read the tool doc on the step under `docs/tools/`
 - Do not start a step whose `needs` files are missing
 - Produce the step’s `produce_path`; run its `check` against the Work Item paths
 - On check fail: retry at most three times, then set Last failure and ask
 - Pass produced files to later steps; do not skip with a chat summary
 - One step per continue unless they asked to run the whole named job (then walk remaining ready steps until blocked or complete)
7. After the step, **journal-keeper**: last completed, next action, artifacts, facts/rules loaded, blockers.
8. At session end, write **Last session summary** and optionally refresh `<root_path>/STATUS.md`.
9. When the Work Item reaches done, ask whether to promote Work Item facts/rules to Expert Role shared memory.

Always follow the selected workflow’s step order. Do not skip phases unless the journal says the step is already complete and the artifact exists.
