---
name: continue
description: >-
  Resume from the expert journal and active Work Item when they say continue,
  resume, or start. Continue is not a yes and not an answer. Walks one ready
  workflow step when a role job is selected.
disable-model-invocation: false
---

# Continue

Resumes the real-estate transaction-coordinator role from the journal. Use when the user says "continue", "start", or "resume" so the agent reads the journal and performs the next step.

## When to use

- User says "continue", "start", or "resume"
- User asks to pick up where the transaction file left off
- When the workflow is waiting for an answer or approval, "continue" means re-prompt, not "user answered" or "user approved"

## Instructions

**Do not** treat the user saying "continue" as an answer to a question or as approval of a gate. "Continue" means only: read the journal and perform the next step. If that step is waiting for an answer or for approval, re-prompt and do **not** advance until the user gives a substantive answer or explicitly approves or waives. The word "continue" by itself is not an answer and is not approval.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the user said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context Initialization (Steps 0a-0d)

0a. **Check for active context:**
 - Read `.cursor/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-4412`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.cursor/active-work-item.txt` (legacy read fallback only) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "Which transaction Work Item? (WID-XXXXXXXX or address + buy/list side)". Parse response:
 - Treat the id as a Work Item: `context_type=work-item`, `context_id=<id>`
 - Write `.cursor/active-context.txt` as `work-item:<id>` only (legacy `.cursor/active-work-item.txt` is read, never written).

0c. **Set context paths:**
 - Active work item: `.cursor/active-context.txt`, formatted `work-item:<id>`.
 - Artifacts (in/work/out/evidence, STATUS, facts): `work-items/<context_id>/`.
 - Journal: `journals/work-items/<context_id>/progress.md` for item-wide fields, `state.json` for the branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action. Write through journal-keeper.

0d. **Load or select workflow type:**
 - Read `<journal_path>` to check for "Workflow type" field
 - If missing: invoke `workflow-selector` skill → user selects a registered role job → reload journal
 - If "Pipeline" field exists but no "Workflow type": map old names to the default role job `dates-calendar` unless they named another registered job.
 - Read `.cursor/workflows/workflow-registry.json`
 - Load `.cursor/workflows/<workflow-type>.md`
 - Use that file for phase sequence, human gates, and artifact paths. Also read `docs/role/work-item-method.md`.

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy structure from `work-items/_TEMPLATE/`
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.

### Facts and Rules Loading (Step 0f)

0f. **Load facts and rules at session start:**
 - Read `facts/MEMORY-INDEX.md` first
 - Load `facts/facts-operations.md` and `facts/rules-operations.md` (this role’s only live Expert Role pair)
 - Read `<root_path>/facts/facts.md` and `<root_path>/facts/rules.md` when present
 - **Filter Expert Role facts/rules by workflow:** Include an entry if `**Workflows:**` is `all` or lists the current role job (or is missing — treat as all)
 - Rules MUST be followed; facts provide context
 - Log to journal: loaded counts for this workflow
 - If rules conflict, note under "Rule violations / conflicts"

### Pipeline Execution (Steps 1-8)

1. **Read context journal:** Read `<journal_path>`. If missing or empty, initialize from template, set workflow from step 0d, set next action to the first step of the selected workflow, and proceed.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask those questions and do not advance until they are answered. **The word "continue" is not an answer.**
3. **Blockers / Last failure:** If Blockers or Last failure is set, describe the block, discuss how to proceed, and wait for agreement. Do not skip or invent a shop workaround.
4. **Wait for approval:** If next action is a human gate (blank effective date, missing exhibit, conflicting executed pages, guessed labels), re-surface the ask. Do not treat "continue" as approval. Never invent a deadline, never promise a close, never send wire instructions.
5. **Done or empty:** If next action is empty or "done", stop and optionally ask what they want next. Offer **promote-facts-rules** when the Work Item is complete.
6. **Otherwise perform the single next step** from the loaded workflow file:
 - Paths in the YAML (`work/`, `out/`) are relative to `<root_path>`
 - Read the step’s tool under `docs/tools/`
 - Do not start if `needs` files are missing
 - Run the step `check` from `<root_path>`
 - On fail: retry at most 3, then ask
 - One step per continue unless they asked to run the whole named job (then walk remaining steps until complete or blocked)

7. After the step, update the Work Item journal (journal-keeper behavior): phase completed, next action set, artifacts updated.
8. At session end, write **Last session summary** in the context journal and optionally refresh `<root_path>/STATUS.md`.
9. When context reaches "done", ask whether to promote Work Item facts/rules to Expert Role level.

Always follow the selected workflow’s step order. Do not skip steps unless the journal says the step is already complete and the artifact exists.
