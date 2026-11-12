---
name: continue
description: >-
  Resume from the expert journal and active Work Item when they say continue,
  resume, or pick up where we left off. Continue is not a yes and not an
  answer. Walks one ready step of the selected collision-shop office workflow.
disable-model-invocation: false
---

# Continue

Resumes this Auto body estimator / office role from the journals. Use when the user says "continue", "start", or "resume". Continue is **not** approval of a gate and **not** an answer to an open question.

## When to use

- User says "continue", "start", or "resume"
- User asks to pick up where the role left off
- When the next step awaits an answer or approval, "continue" means re-prompt, not "user answered"

## Instructions

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the user said "define my role", run **define-role** and stop.
 - If `Role status` is `pending` or the field is missing, run **define-role** and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context initialization

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-21411151` or `work-item:2026-09-15-ro-2104`)
 - If missing: check `.claude/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "Which assignment / RO / claim is this? Give a Work Item id (for example WID-21411151 or 2026-09-15-ro-2104)." Parse the reply and write `.claude/active-context.txt` as `work-item:<id>`.

0c. **Set paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`


0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke **workflow-selector** → operator picks a registered job → reload journal
 - If an old **Pipeline** field exists without Workflow type: map it to `assignment-intake` unless they named another registered job
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md`
 - Use `docs/role/work-item-method.md` for phase meaning, artifacts, and human gates

0e. **Initialize folders:** If `<root_path>` does not exist, copy `work-items/_TEMPLATE/`. If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`. Write `Current work item: <context_id>` in `journals/expert/progress.md` (copy `journals/_TEMPLATE/expert/progress.md` first if missing).

0f. **Load facts and rules:**
 - Always load `facts/MEMORY-INDEX.md` first
 - Load `facts/facts-shared.md` and `facts/rules-shared.md` (shared Expert Role memory; always)
 - Load `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md` when present
 - Rules must be followed. Facts inform work. Log conflicts in the journal.
 - Do **not** default to a coding-pipeline or incident-session memory pair.

### Execution

1. Read `<journal_path>`. If missing or empty, initialize from template, set workflow from 0d, set next action to the first YAML step of that workflow.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask those questions and stop. The word "continue" is not an answer.
3. **Blockers / Last failure:** Describe the block, what is needed (file, auth, VIN pick, procedure PDF), and wait for agreement. Do not skip or invent.
4. **Wait for a human gate:** If next action is wait for authorization, wait for missing-assignment answer, wait for procedure page, or similar, re-surface the gate. Do not advance until a substantive answer or explicit approval. "Continue" does not count.
5. **Done or empty:** If next action is empty or "done", stop and optionally ask what they want next. At Work Item completion, offer **promote-facts-rules**.
6. **Otherwise walk one ready YAML step** from the loaded workflow file:

   Path context: `in/`, `work/`, `out/`, `evidence/` in the workflow file mean **inside** `work-items/<id>/`.

   - Do not start a step whose `needs` files are missing. Ask for the file.
   - Read the cited `docs/tools/` file. Produce the `produce_path` under the Work Item folder.
   - Run the step `check` with those same paths. Exit 0 = pass. On fail, retry at most 3, then ask. Do not invent a pass.
   - If the step has no check, ask how to prove it; do not mark passed.
   - Pass the produced **file** to later steps, not a chat summary.
   - One step per continue unless they asked to run the whole named job (then walk until complete or blocked).

7. After the step, **journal-keeper**: phase/step completed, next action, artifacts, blockers, facts/rules loaded.
8. At session end, write **Last session summary** in the Work Item journal and optionally refresh `<root_path>/STATUS.md`.

Always follow the selected workflow’s step order. Do not skip steps unless the journal says the step already passed and the artifact exists.
