---
name: continue
description: >-
  Use when the user says "continue", "start", or "resume" with no other
  instruction. Runs define-role while the role is pending, then reads the
  active journal and walks one ready fleet-dispatch workflow step. Does NOT
  mean approval of a gate or an answer to an open question.
---

# Continue

Resumes the fleet / delivery dispatcher role from the journals. Use when the user says "continue", "start", or "resume".

## When to use

- User says "continue", "start", or "resume"
- User asks to pick up where the role left off
- When the job is waiting for an answer or approval, "continue" means re-prompt, not "user answered" or "user approved"

## Instructions

**Do not** treat the user saying "continue" as an answer to a question or as approval/waiver of a gate. "Continue" means only: read the journal and perform the next step. If that step is waiting for an answer or for approval, re-prompt and do **not** advance until the user gives a substantive answer or explicitly approves/waives. Role questions use the same rule: "I approve the role" or "Skip role definition" is the approval, not the word continue.

### Role gate (before any Work Item)

0. Read `MyRole.txt` at the workspace root.
 - If the user said "define my role", run the define-role skill and stop.
 - If `Role status` is `pending` or the field is missing, run define-role and stop. Do not ask for a Work Item ID.
 - If `Role status` is `defined` or `skipped`, continue to step 0a.

### Context initialization

0a. **Check for active context:**
 - Read `.cursor/active-context.txt`
 - Format: `<type>:<id>` (e.g., `work-item:WID-214111151` or `work-item:2026-09-15-truck-14-route-a`)
 - If file exists: parse type and id, set `context_type` and `context_id`
 - If file missing: check `.cursor/active-work-item.txt` (legacy) → assume `context_type=work-item`
 - If both missing: proceed to step 0b

0b. **Prompt for context:** If no active context, ask: "What are you working on? Give a Work Item ID (WID-XXXXXXXX) or a dated pack name (for example 2026-09-15-truck-14-route-a)." Parse the reply, write `.cursor/active-context.txt` as `work-item:<id>`.

0c. **Set context paths:**
 - `root_path=work-items/<context_id>/`
 - `journal_path=journals/work-items/<context_id>/progress.md`
 - `map_path=journals/work-items/<context_id>/state.json`
 - There is no `work-items/<context_id>/journal/` folder; journals live under `journals/work-items/<context_id>/`.

0d. **Load or select workflow type:**
 - Read `<journal_path>` for **Workflow type**
 - If missing: invoke `workflow-selector` → user selects a registered role job → reload journal
 - If an old **Pipeline** field exists without **Workflow type**, map it to the registry `default_workflow` (`assignment-pack`) unless the operator names a specific role job
 - Read `.cursor/workflows/workflow-registry.json`
 - Load `.cursor/workflows/<workflow-type>.md` and `docs/role/work-item-method.md`

0e. **Initialize folder structure:** If `<root_path>` does not exist, copy `work-items/_TEMPLATE/`. If `journals/work-items/<context_id>/` does not exist, copy `journals/work-items/_TEMPLATE/` there and set **Work item record** to `work-items/<context_id>/`. Write `Current work item: <context_id>` in `journals/expert/progress.md`.

### Facts and rules

0f. Load `facts/MEMORY-INDEX.md` first, then the shared pair (`facts/facts-shared.md`, `facts/rules-shared.md`) and the operations pair (`facts/facts-operations.md`, `facts/rules-operations.md`). Load Work Item facts/rules under the active `work-items/<id>/facts/` folder when present. Filter Expert Role entries by `**Workflows:**` (include `all` or the current registered workflow id). Rules MUST be followed. Log load counts to the Work Item journal.

### Walk one ready step

1. Read `<journal_path>`. If empty, set workflow from 0d and next action to the first ready step of that map.
2. If Open questions (blocking) is non-empty, ask those questions and stop. **The word "continue" is not an answer.**
3. If Blockers or Last failure is set, describe the block and wait for agreement. Do not invent a pass.
4. If next action is wait for operator approval (assignment draft, exception language, HOS/fuel questions, treating a pack as dispatched or billed), re-surface the pack path and wait. Saying "continue" does not count.
5. If next action is empty or "done", stop and optionally ask what they want next.
6. Otherwise perform **one** ready step from the loaded workflow file:
 - Paths `in/`, `work/`, `out/`, `evidence/` are inside `<root_path>`
 - Read the step’s tool file under `docs/tools/`
 - Produce the file at `produce_path`
 - Run the step’s check against those Work Item paths
 - On fail: retry at most 3 times, then ask with **operator-qa**
 - Do not look for deleted process skills. The workflow file is the instruction.
 - If they asked to run the whole named job, walk remaining ready steps until the map is complete or blocked
7. After the step, **journal-keeper**: phase/step completed, artifacts, checks, next ready step, session summary on `STATUS.md` as needed.
8. When the Work Item reaches done, ask whether to run **promote-facts-rules**.

Always follow the selected work map. Do not skip steps unless the journal says the step already passed and the artifact exists.
