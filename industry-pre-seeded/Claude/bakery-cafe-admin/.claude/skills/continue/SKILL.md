---
name: continue
description: >-
  Use when the user says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  expert and Work Item journals and performs the next bakery-cafe job step.
  Does NOT mean approval of a gate or an answer to an open question.
---

# Continue

Resumes the bakery / cafe production-office job from the journals. Use when the operator says "continue", "start", or "resume".

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When the job is waiting for an answer or a missing file, "continue" means re-prompt, not "they answered"

## Instructions

**Do not** treat "continue" as an answer to a question or as approval of a pack. "Continue" means only: read the journals and perform the next ready step. If that step waits for a missing formula, missing case count, missing receiving file, or operator confirmation, re-prompt and do **not** advance.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the user said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context Initialization (Steps 0a-0e)

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151` or `work-item:2026-11-08-bake-list`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.claude/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? Give a Work Item id (WID-XXXXXXXX) or a bake-date / pack name (for example `2026-11-08-bake-list`)." Parse response, then write `.claude/active-context.txt` as `work-item:<id>` only (do not write the legacy `.claude/active-work-item.txt`).

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - Step notes live in `journals/work-items/<context_id>/nodes/`. Do not invent a `work-items/<context_id>/journal/` path.

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → operator selects a registered bakery-cafe job → reload journal
 - If a leftover **Pipeline** field exists from an older template, map it to `bake-list-day` unless they named another registered job
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md`
 - Use that file for phase sequence, gates, tools, and checks. Do not look up a separate process skill to walk the map.

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy structure from `work-items/_TEMPLATE/`
 - Ensure `in/`, `work/`, `out/`, and `evidence/` exist under the Work Item
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.

### Facts and Rules Loading (Step 0f)

0f. **Load facts and rules:**
 - Always load `facts/MEMORY-INDEX.md` first
 - Then load the shared pair `facts/facts-shared.md` and `facts/rules-shared.md`
 - Then load `facts/facts-operations.md` and `facts/rules-operations.md` (this role’s job memory)
 - Then load Work Item facts under `<root_path>/facts/` when those files exist
 - Filter Expert Role entries by `**Workflows:**` (include `all` or the current job id)
 - Rules MUST be followed; facts provide context
 - Log to journal: facts/rules loaded for this job
 - Do **not** load software-design or incident-bridge memory files; they are not this role

### Perform the next step

1. **Read** `<journal_path>` and the active leaf note under `journals/work-items/<context_id>/nodes/`. If the flat journal is missing, initialize from template (0e), set workflow from 0d, set next action on the active node to the first step of the selected job.
2. **Blocking questions:** If Open questions (blocking) on the active node (or flat journal leftovers) is non-empty, ask those questions. Stop. "Continue" is not an answer.
3. **Blockers:** If Blockers or Last failure is set on the active node, describe the block, ask how to proceed, and wait. Do not invent a formula, par, or quantity to unblock.
4. **Wait for a human gate:** If next action is wait for a missing formula, missing case count, missing file, allergen-sheet fight, or pack confirmation, re-surface the ask and stop. Do not treat "continue" as confirmation.
5. **Done or empty:** If next action is empty or "done", or flat journal Completion status is done, stop and ask what they want next. Offer **promote-facts-rules** if the pack just closed.
6. **Otherwise perform the single next ready step** from the loaded workflow file:
 - Paths `work/`, `out/`, `in/`, `evidence/` are **inside** `<root_path>`
 - Read the step’s `docs/tools/` file
 - Do not start the step if `needs` files are missing — ask for them
 - Write `produce_path`, run the listed `check` with working directory = `<root_path>`
 - Check must exit 0. On fail, retry at most 3 times from the tool doc, then ask via **operator-qa**. Never invent a pass
 - Keep shorts, stales, missing formulas, and blank allergen cells visible on the pack
7. After the step, run **journal-keeper**: last completed, next action, artifacts, open questions.
8. At session end, write **Last session summary** and optionally refresh `<root_path>/STATUS.md`.

Always follow the selected job’s step order. Do not skip a step unless the journal says it already passed and the artifact exists.
