---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the operator to select an enabled role job."
trigger: Called by continue skill when journal missing workflow type
---

# Workflow Selector

Presents the registered nonprofit-office jobs and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` to get `context_type` and `context_id`
 - If `context_type=work-item`: working on a named role job

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow in `workflow-registry.json` as a numbered line: name, then the description. Do not offer a workflow that is not in the registry.

 Until define-role changes it, offer: Board Pack, Donor List, Funder Gap, Gift Ack Draft, Grant Deadlines, Grant Report, In Kind List, Minutes Index, Restricted Ask. Default if they do not choose: `board-pack`. Do not offer a software-build pipeline.

4. **Accept operator input:**
 - A number matching the menu, or a workflow name (job id or display name)

5. **Validate selection:** Ensure the workflow exists in the registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - "What is the Work Item ID? (e.g., WID-21411151, or a meeting/grant/batch name we can use as the folder)"
 - "Which source files? (grant PDF, donor CSV, minutes folder, board folder, restricted-fund sheet, ack template)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.
 - Next action is the first step of the selected workflow (usually intake / first YAML step), not a design-approval gate.

8. **Write active context file:**
 - Write `.claude/active-context.txt` as `<context_type>:<context_id>`

9. **Confirm:**

 Work Item initialized with <workflow-name>
 Initial phase: intake / first ready step
 Next action: <next-action>

## Workflow-Specific Fields to Record

- Job id from `workflow-registry.json`
- Work Item folder `work-items/<id>/`
- Source files named by the operator
- Human gate reminder from `docs/role/work-item-method.md` (they circulate, sign, send, submit)

## Notes

- Called by continue when journal is missing workflow type
- Do not invent extra pipelines. Add jobs only through define-role or an explicit operator request plus registry update
