---
name: continue
description: >-
  Use when the operator says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active Work Item journal and performs the next ready HOA role-job step.
  Does NOT mean approval of a gate or an answer to an open question.
---

# Continue

Resumes HOA / association admin work from the expert journal and the active Work Item. Use when the operator says "continue", "start", or "resume".

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up where the role left off
- When the job is waiting for an answer or approval, "continue" means re-prompt, not "operator answered" or "operator approved"

## Instructions

**Do not** treat "continue" as an answer to a question or as approval/waiver of a human gate. "Continue" means only: read the journal and perform the next ready step. If that step is waiting for an answer or for approval (association name, as-of date, which meeting, which application, board/committee decision), re-prompt and do **not** advance until the operator gives a substantive answer or explicitly approves/waives. Role questions use the same rule: "I approve the role" or "Skip role definition" is the approval, not the word continue.

Method note: `docs/role/work-item-method.md`.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the operator said "define my role", run the **define-role** skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context Initialization (Steps 0a-0e)

0a. **Check for active context:**
 - Read `.claude/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.claude/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? (work item WID-XXXXXXXX, or a new HOA job such as this week's ACC packet, dues aging, or board files)". Parse response:
 - If starts with "WID-": `context_type=work-item`, `context_id=WID-XXXXXXXX`
 - If they described a job without an id: create a Work Item id (`WID-` plus an 8-digit stamp) and confirm the label
 - Write to `.claude/active-context.txt` as `<type>:<id>`

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - Do not look for a leftover role-journal folder at the Expert root or a top-level job pile outside `work-items/<id>/`.

0d. **Load or select workflow type:**
 - Read `<journal_path>` to check for "Workflow type" field
 - If missing: invoke **workflow-selector** → operator selects a registered HOA role job → reload journal
 - If "Pipeline" field exists but no "Workflow type": map only names that exist in `.claude/workflows/workflow-registry.json`. Never invent a software-build or incident-bridge workflow.
 - Read `.claude/workflows/workflow-registry.json`
 - Load `.claude/workflows/<workflow-type>.md`
 - Use `docs/role/work-item-method.md` for phases, artifacts, and human gates

0e. **Initialize folder structure:** If `<root_path>` does not exist:
 - Copy structure from `work-items/_TEMPLATE/`
 - If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`
 - Write `Current work item: <context_id>` in `journals/expert/progress.md`. If that file is missing, copy `journals/_TEMPLATE/expert/progress.md` first.

### Facts and Rules Loading (Step 0f)

0f. **Load facts and rules:**
 - Always load `facts/MEMORY-INDEX.md` first
 - Load `facts/facts-operations.md` and `facts/rules-operations.md` (this role's Expert Role memory)
 - Load `<root_path>/facts/facts.md` and `<root_path>/facts/rules.md` when they exist
 - Rules MUST be followed. Facts provide context. Do not invent how this association already works.

### Next-step execution

1. Read `journals/expert/progress.md` and `<journal_path>` plus the active node note named by `state.json` `active`.
2. If Open questions (blocking) is non-empty → ask those. Stop. Continue is not an answer.
3. If Next action is `define-role` → that skill.
4. If Next action is wait for operator / wait for approval → re-prompt. Stop.
5. Otherwise walk **one ready step** from the loaded workflow YAML (or the whole named job if they asked). For that step: read the cited `docs/tools/` file, write the produced file under the Work Item (`work/` or `out/`), run the listed check against those paths, copy logs to `evidence/`, then **journal-keeper**.
6. If next action is empty or the job is done → ask what they want next; offer **promote-facts-rules** when a pack is finished.

One step per continue unless they asked to run a whole named job (then walk remaining YAML steps until complete or blocked).
