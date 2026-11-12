---
name: continue
description: >-
  Resume from journals/ and the active Work Item when they say continue, resume,
  or start. Continue is not a yes and not an answer. Walks one ready gym role
  job step from the selected workflow file.
---

# Continue

Resumes gym / fitness front role work from the journal. Use when the operator says "continue", "start", or "resume".

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role job left off
- When the job is waiting for an answer or approval, "continue" means re-prompt, not "operator answered" or "operator approved"

## Instructions

**Do not** treat "continue" as an answer to a question or as approval/waiver of a gate. If the next action is waiting for an answer or approval, re-prompt and do **not** advance until the operator gives a substantive answer or explicitly approves or waives. Role questions use the same rule: "I approve the role" or "Skip role definition" is the approval, not the word continue.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the operator said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context initialization (Steps 0a-0e)

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151` or `work-item:2026-11-08-close`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.claude/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What role job are you working on? Give a Work Item id (WID-XXXXXXXX or a day/member/class label such as 2026-11-08-check-in)." Parse response:
 - Write to `.claude/active-context.txt` as `work-item:<id>`
 - Do not write the legacy `.claude/active-work-item.txt`

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → operator selects a registered role job → reload journal
 - If a legacy **Pipeline** field exists but no **Workflow type**, map `developer` / `operations` / unknown to `check-in-day` unless they named another registered job
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md`
 - Follow `docs/role/work-item-method.md` for phases and human gates

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy structure from `work-items/_TEMPLATE/`
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.
 - Ensure `in/`, `work/`, `out/`, and `evidence/` exist under the Work Item.

### Facts and rules (Step 0f)

0f. Load memory for this gym role:
 - Always first: `facts/MEMORY-INDEX.md`
 - Then shared: `facts/facts-shared.md` + `facts/rules-shared.md`
 - Then Expert Role operations: `facts/facts-operations.md` + `facts/rules-operations.md`
 - Then Work Item: `work-items/<context_id>/facts/facts.md` and `work-items/<context_id>/facts/rules.md` when present
 - Filter Expert Role entries by `**Workflows:**` (`all` or the current role job id)
 - Rules MUST be followed. Starter notes are guesses until this club corrects them.
 - Log loaded counts in the Work Item journal

### Execute the next step

1. Read `<journal_path>`. If missing, initialize from template (0e), set workflow from 0d, set next action to the first YAML step of the selected workflow.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask those questions. **The word "continue" is not an answer.** Record answers in Resolved Q&A in the same turn, then re-evaluate.
3. **Blockers / Last failure:** Describe the block, discuss how to proceed, do not skip or invent a pass.
4. **Wait for approval:** If next action is wait-for-approval (missing policy file, override, freeze/cancel application, check proposal), re-surface the item. Do not treat `continue` as approval.
5. **Done or empty:** If next action is empty or `done`, stop and optionally ask what they want next. Offer **promote-facts-rules** when the Work Item is complete.
6. **Otherwise perform one ready workflow step:**
 - Read the loaded `.claude/workflows/<job>.md` YAML map.
 - A step is ready when every `needs` artifact exists on disk under `<root_path>` (resolve `work/` and `out/` inside the Work Item).
 - Do not start a step whose needed files are missing — ask for the file or record a blocker.
 - Read the step's `tool` file under `docs/tools/`. Follow it. Write `produce_path` under `<root_path>`.
 - Run the step `check` from the Work Item root (or repo root if the check path is `docs/tools/checks/...` with Work Item-relative file arguments). Save stdout/stderr and exit code under `<root_path>/evidence/`.
 - On check fail: retry the tool and check at most 3 times, then ask. Do not invent a pass.
 - If the operator asked to run the **whole named job**, walk ready steps until the map is complete or blocked; otherwise **one** ready step.
7. After the step, **journal-keeper**: last completed, next action (next YAML `next` id, wait, or `done`), artifacts, evidence logs.
8. At session end, write **Last session summary** and optionally refresh `<root_path>/STATUS.md`.

Always follow the selected role job's step order. Do not skip a step unless the journal says it already passed and the artifact exists.
