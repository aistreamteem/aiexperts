---
name: continue
description: >-
  Use when the user says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active journal and performs the next janitorial-office workflow step.
  Does NOT mean approval of a gate or an answer to an open question.
disable-model-invocation: false
---

# Continue

Resumes the role from the journals. Use when the user says "continue", "start", or "resume".

## When to use

- User says "continue", "start", or "resume"
- User asks to pick up where the pack left off
- When the next action is waiting for an answer or approval, "continue" means re-prompt, not "user answered"

## Instructions

**Do not** treat the user saying "continue" as an answer to a question or as approval/waiver of a gate. "Continue" means only: read the journal and perform the next step. If that step is waiting for an answer or for approval, re-prompt and do **not** advance until the user gives a substantive answer or explicitly approves.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the user said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context Initialization (Steps 0a-0e)

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151` or `work-item:2026-09-15-clinic-night`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.claude/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? Give a Work Item ID (WID-XXXXXXXX) or a site-night / pack name (for example `2026-09-15-clinic-night`)." Parse response and write `.claude/active-context.txt` as `work-item:<id>`. Do not write the legacy `.claude/active-work-item.txt`.

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - Journal notes live under `journals/work-items/<context_id>/` (flat `progress.md`, `state.json`, `nodes/`). Do not invent a `work-items/<id>/journal/` path.

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → user selects a registered role job → reload journal
 - If a legacy **Pipeline** field exists and no Workflow type: map leftover generic pipeline names to `night-board` unless they named another registered job
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md`
 - Follow that file’s phases, artifacts, and human gates. Do not look for deleted process skills.

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy structure from `work-items/_TEMPLATE/`
 - Ensure `in/`, `work/`, `out/`, and `evidence/` exist under the Work Item
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.

### Facts and Rules Loading (Step 0f)

0f. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`. Load `<root_path>/facts/facts.md` and `<root_path>/facts/rules.md` when present. Filter Expert Role entries by `**Workflows:**` (include `all` or the current role job id). Log how many facts/rules loaded. This role’s default memory is **operations**, not developer or incident.

### Pipeline Execution (Steps 1-8)

1. Read `<journal_path>`. If missing or empty, initialize from template, set workflow from 0d, set next action to the first step of that workflow.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask those questions. **The word "continue" is not an answer.**
3. **Blockers / Last failure:** Describe the block, discuss how to proceed, wait for agreement. Do not skip.
4. **Wait for approval:** If next action is waiting for operator approval (missing-file confirmation, which calendar wins, treat-starter-as-this-shop, and similar gates in the workflow file), re-surface the item. Do not advance on the word continue.
5. **Done or empty:** If next action is empty or "done", stop and optionally ask what they want next. Offer **promote-facts-rules**.
6. **Otherwise perform the single next step** using the loaded workflow file:
 - Paths are relative to `<root_path>` (`work-items/<id>/`).
 - Read the tool doc named by the step (`docs/tools/…`).
 - Produce the named artifact under `work/` or `out/`.
 - Run the named check (from the expert root, with paths pointing at the Work Item files, or `cd` into the Work Item first). Retry at most 3 times on fail, then ask. Never invent a pass.
 - Do not start a step whose `needs` files are missing.
 - Pass produced files, not chat summaries.

7. After the step, **journal-keeper**: phase/step completed, next action, artifacts, facts/rules loaded, checks run.
8. At session end, write **Last session summary** in the Work Item journal and refresh `<root_path>/STATUS.md`.
9. When the Work Item is done, ask whether to promote facts/rules.

Always follow the workflow file’s step order. Do not skip steps unless the journal says the step is complete and the artifact exists.
