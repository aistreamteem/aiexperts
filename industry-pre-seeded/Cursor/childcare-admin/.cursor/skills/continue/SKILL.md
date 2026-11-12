---
name: continue
description: >-
  Use when the user says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  expert and Work Item journals and performs the next ready step on this
  childcare-office work map. Does NOT mean approval of a director gate or
  an answer to an open question.
---

# Continue

Resumes this childcare center office Expert from the journals. Use when the operator says "continue", "start", or "resume" so the agent reads the journal and performs the next ready work-map step.

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When the next step is waiting for an answer or a director gate, "continue" means re-prompt, not "operator answered" or "director approved"

## Do not

- Treat "continue" as an answer to a blocking question
- Treat "continue" as approval to start a child, release a child, interpret a court order, file a claim, or stamp the license
- Use a legacy shared job pile at the expert root instead of `work-items/<id>/`
- Run a software design-and-implement pipeline

## Instructions

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the operator said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context Initialization (Steps 0a-0e)

0a. **Check for active context:**
 - Read `.cursor/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151` or `work-item:2026-11-08-room-a-attendance`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.cursor/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? Give a Work Item ID (WID-XXXXXXXX) or a job label (for example `2026-11-08-room-a-attendance`)." Parse the reply and write `.cursor/active-context.txt` as `work-item:<id>`.

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - Artifacts live under `work-items/<context_id>/`. Journal notes live under `journals/work-items/<context_id>/`.

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → operator selects a registered role job → reload journal
 - If a legacy **Pipeline** field exists but no **Workflow type**: map `developer`, `operations`, and unknown names to `attendance-day` unless they named another registered job
 - Read `.cursor/workflows/workflow-registry.json`
 - Load `.cursor/workflows/<workflow-type>.md` and follow it as self-contained instructions
 - Default registered job: `attendance-day`

0e. **Initialize folder structure:** If `<root_path>` does not exist, copy `work-items/_TEMPLATE/`. If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`. Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.

### Facts and rules (Step 0f)

0f. Load memory for this role:
 - `facts/MEMORY-INDEX.md` first
 - `facts/facts-shared.md` and `facts/rules-shared.md` (always)
 - `facts/facts-operations.md` and `facts/rules-operations.md`
 - `work-items/<id>/facts/facts.md` and `.../rules.md` when present
 - Filter Expert Role entries by `**Workflows:**` (`all` or the current registered job id). Work Item entries are not filtered.
 - Rules must be followed. Facts inform the pack. Never invent how *this* center files.

### Blocking questions

If the Work Item journal or active node has open blocking questions (missing export, pickup mismatch, start-without-packet, director signature): **ask those and stop**. Continue is not an answer.

### Perform one ready step

1. Read the selected workflow file. A step is ready when every `needs` artifact exists on disk under the Work Item folder.
2. Read the named `docs/tools/` file. Produce the file at `produce_path` (relative to `work-items/<id>/`). Run the `check` from that folder.
3. On check fail: retry at most 3 times, then ask with **operator-qa**. Do not invent a pass.
4. **journal-keeper** after the one step: artifacts, check result, next ready step.
5. One step per continue unless the operator asked to run the whole named job — then walk remaining ready steps until the map is complete or blocked.

If `next_action` is empty or the map is done: ask what they want next. Offer **promote-facts-rules** when the pack is complete.
