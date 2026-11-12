---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled role job."
trigger: Called by continue skill when journal missing workflow type
---

# Workflow Selector

Presents this role’s job menu and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` for `context_type` and `context_id`
 - If `context_type=work-item`: working on a print-shop coordinator role job

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a job that is not in the registry. Do not offer software-build or incident pipelines.

 Until the operator changes it, the registry contains the print-shop coordinator jobs. Default workflow: `job-board`.

 Typical matches:
 - Ticket sheet / daily production board → Job Board
 - Art/proof folder vs house checklist → Preflight Completeness
 - Proof type/status export vs folder → Proof Status
 - On-hand stock vs open tickets → Stock Vs Jobs
 - Mill-order sheet vs inventory → Mill Order Vs Stock
 - Ticket dues vs press calendar → Due Today
 - Finishing list after print → Bindery Queue
 - Delivery log for today → Delivery Today
 - Reprint tickets with reason text → Reprint Log

4. **Accept input:** a number, a registry id, or a display name.

5. **Validate:** If invalid, re-prompt.

6. **Ask:**
 - "What is the Work Item ID? (e.g., WID-20261108)"
 - "Any external references? (chat threads, MIS tickets, source files)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item` (first YAML step of the selected job, usually intake / first `needs: []` step)

8. **Write active context file:**
 - `.claude/active-context.txt` as `<context_type>:<context_id>`
 - Do not write `.claude/active-work-item.txt` (legacy; read fallback only)

9. **Confirm:**

 Work Item initialized with \<workflow-name\>
 Initial phase: isolate / intake
 Next action: first YAML step in that job’s instruction file

## Notes

- If both Workflow type and a legacy Pipeline field are missing, default to `default_workflow` from the registry (`job-board`) and prompt to confirm or change
- Never coerce an unknown name into a software-build or incident pipeline
