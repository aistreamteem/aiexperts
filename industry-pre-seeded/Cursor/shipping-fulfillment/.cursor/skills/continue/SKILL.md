---
name: continue
description: >-
  Use when the user says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active journal and performs the next shipping-fulfillment work-map step.
  Does NOT mean approval of a gate or an answer to an open question.
---

# Continue

Resumes the active shipping Work Item from the journals. Use when the operator says "continue", "start", or "resume".

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When the job is waiting for an answer or a file, "continue" means re-prompt, not "they answered"

## Instructions

**Do not** treat "continue" as an answer to a question or as approval of a gate. It means only: read the journal and perform the next ready step. If that step waits for an answer (which scale export is live, whether a hold may release, and so on), re-prompt and do **not** advance until they give a substantive answer. Role questions use the same rule: "I approve the role" or "Skip role definition" is the approval, not the word continue.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the user said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context initialization (steps 0a–0e)

0a. **Check for active context:**
 - Read `.cursor/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-20261108`)
 - If file exists: parse type and id
 - If file missing: check `.cursor/active-work-item.txt` (legacy read fallback only)
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? (work item WID-XXXXXXXX — one wave, order, truck, day, or RMA batch)". Parse response:
 - If starts with "WID-": `context_type=work-item`, `context_id=WID-XXXXXXXX`
 - Write `.cursor/active-context.txt` as `work-item:<id>` only (do not write the legacy pointer)

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - Node notes: `journals/work-items/<context_id>/nodes/<active leaf>.md`
 - Background notes: `journals/work-items/<context_id>/agent-notes/`

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → operator selects a registered role job → reload journal
 - Read `.cursor/workflows/workflow-registry.json`
 - Load `.cursor/workflows/<workflow-type>.md`
 - Default if they decline to choose: `bol-pack` (confirm first)
 - Do not map unknown names to a developer or incident pipeline

0e. **Initialize folders:** If `<root_path>` does not exist:
 - Copy `work-items/_TEMPLATE/`
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md` (copy from `journals/_TEMPLATE/expert/progress.md` if missing)
 - Create `in/`, `work/`, `out/`, and `evidence/` under the Work Item if missing

### Facts and rules (step 0f)

0f. Load in this order:
 - `facts/MEMORY-INDEX.md`
 - `facts/facts-shared.md` and `facts/rules-shared.md` (always)
 - `facts/facts-operations.md` and `facts/rules-operations.md` (this role’s job memory; filter `**Workflows:**` to `all` or the current registry id)
 - `work-items/<id>/facts/facts.md` and `.../rules.md` when those files exist
 - Log loaded counts in the Work Item journal
 - Follow rules. Ask when shop procedure is missing. Do not invent weight, DIM, NMFC class, PRO, or tracking.

### Execution (steps 1–8)

1. **Read** `<journal_path>` and the active node under `journals/work-items/<id>/nodes/`. If empty, set next action to the first YAML step of the selected workflow.
2. **Blocking questions:** If Open questions (blocking) is non-empty, ask those questions. **The word "continue" is not an answer.**
3. **Blockers:** If Blockers or Last failure is set, describe the block (missing PDF, check failed, hold not released) and wait for agreement. Do not skip.
4. **Wait for a human gate:** If next action is waiting for a file, a “which file is live” choice, or explicit okay to publish a list, re-surface that ask. Do not treat continue as approval.
5. **Done or empty:** If next action is empty or "done", stop and ask what they want next. Optionally offer **promote-facts-rules**.
6. **Otherwise perform one ready YAML step** from the loaded workflow file:
 - Resolve `in/`, `work/`, `out/`, `evidence/` as paths under `work-items/<id>/`
 - Do not start the step if any `needs` artifact is missing on disk
 - Read the step’s `tool` file under `docs/tools/`
 - Produce the file at `produce_path` inside this Work Item
 - Run the step’s `check` command against those same paths (from the Work Item root, or adjust relative paths so they hit this item)
 - On check fail: retry at most 3, then ask
 - Do not mark the step passed on a chat summary
 - One step per continue unless they asked to run the **whole named job** — then walk remaining ready steps until the map is complete or blocked
7. **journal-keeper**: what ran, artifacts, check result, next action.
8. At session end, write Last session summary and refresh `STATUS.md`.
