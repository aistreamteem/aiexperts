---
name: continue
description: >-
  Use when the user says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active Work Item journal and performs the next rental-role job step.
  Does NOT mean approval of a gate or an answer to an open question.
---

# Continue

Resumes the equipment-rental role from the journal. Use when the operator says "continue", "start", or "resume".

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When the job is waiting for an answer or approval, "continue" means re-prompt, not "operator answered" or "operator approved"

## Instructions

**Do not** treat "continue" as an answer to a question or as approval of a gate. If the next step waits for an answer or approval, re-prompt and do **not** advance until the operator gives a substantive answer or explicit approval (for example "I approve this pack" or "Skip the COI hold"). The word "continue" by itself is not an answer and is not approval.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the operator said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context initialization

0a. **Check for active context.** Read `.cursor/active-context.txt`. Format: `<type>:<id>` (e.g. `work-item:WID-214111151`). If missing, check `.cursor/active-work-item.txt`. If both missing, go to 0b.

0b. **Prompt for context** if none is active: "What are you working on? (work item WID-XXXXXXXX, or name the contract / day / pack)". If the reply starts with `WID-`, use that id. Otherwise mint a Work Item id from the job name (keep it filesystem-safe) and confirm it. Write `.cursor/active-context.txt` as `work-item:<id>` only (do not write the legacy `.cursor/active-work-item.txt`).

0c. **Set paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - Step notes live under `journals/work-items/<context_id>/nodes/`. Write through journal-keeper.

0d. **Load or select the registered job.** Read `<journal_path>` for **Workflow type**. If missing, run **workflow-selector** and reload. If an old **Pipeline** field exists (`developer`, `operations`, `adhoc-incident`), map it to the default role job `contract-completeness` unless the operator names another registered job. Read `.cursor/workflows/workflow-registry.json` and load `.cursor/workflows/<workflow-type>.md`.

0e. **Initialize folders.** If `work-items/<id>/` is missing, copy `work-items/_TEMPLATE/`. If `journals/work-items/<id>/` is missing, copy `journals/work-items/_TEMPLATE/` and set **Work item record** to `work-items/<id>/`. Write `Current work item: <id>` in `journals/expert/progress.md`.

0f. **Load memory.** Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`, then `work-items/<id>/facts/facts.md` and `rules.md` when they exist. Filter Expert Role entries by `**Workflows:**` (include `all` or the current job id). Log how many facts/rules loaded. Follow rules; facts inform decisions.

### Perform the next step

1. Read `<journal_path>`. If empty, set next action to the first step of the selected workflow.
2. If Open questions (blocking) is non-empty, ask those questions and stop. **Continue is not an answer.**
3. If Blockers or Last failure is set, describe the block and wait for agreement. Do not skip.
4. If next action is wait-for-approval (gate hold, pack review, missing-file hold), re-surface the ask. Do not treat "continue" as approval.
5. If next action is empty or `done`, stop and ask what they want next.
6. Otherwise perform **one ready step** from the loaded `.cursor/workflows/<id>.md` file:
 - Do not start a step whose `needs` files are missing from `work-items/<id>/`.
 - Read the named tool under `docs/tools/`.
 - Write the `produce_path` inside `work-items/<id>/` (so `work/` and `out/` in the map are Work Item paths).
 - Run the step’s `check` command against those same paths. Retry at most 3 times on failure, then ask.
 - If the operator asked to run the whole named job, keep going until the map is complete or blocked; otherwise **one step**.
7. Run **journal-keeper**: phase/step completed, artifacts, checks, next action, session summary as needed.
8. When the Work Item is done, offer **promote-facts-rules**.

Always follow the selected job’s step order. Do not skip a step unless the journal says it already passed and the artifact exists.
