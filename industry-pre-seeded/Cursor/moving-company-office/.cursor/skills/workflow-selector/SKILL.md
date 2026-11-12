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
 - Read `.cursor/active-context.txt` for `context_type` and `context_id`
 - If `context_type=work-item`: working on a moving-office role job

2. **Read workflow registry:**
 - Read `.cursor/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a job that is not in the registry. Do not offer software-build or incident pipelines.

 Until the operator changes it, the registry contains the moving-company office jobs. Default workflow: `estimate-from-rate-file`.

 Typical matches:
 - Rate file + inventory / quote draft → Estimate From Rate File
 - Survey sheet vs rooms / PBO vs CP → Inventory Completeness
 - High-value form required by their PDF → High Value List Check
 - Carton/crate pull → Materials List
 - Today’s trucks and names → Crew Day
 - Unit/date collisions → Truck Calendar
 - Dest windows / spreads → Delivery Window List
 - Scale slips → Weigh Ticket Pack
 - Claim photos / BOL number → Claims Routing

4. **Accept input:** a number, a registry id, or a display name.

5. **Validate:** If invalid, re-prompt.

6. **Ask:**
 - "What is the Work Item ID? (e.g., WID-20261108)"
 - "Any external references? (chat threads, estimate numbers, source files)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item` (first YAML step of the selected job, usually intake / first `needs: []` step)

8. **Write active context file:**
 - `.cursor/active-context.txt` as `<context_type>:<context_id>`
9. **Confirm:**

 Work Item initialized with \<workflow-name\>
 Initial phase: isolate / intake
 Next action: first YAML step in that job’s instruction file

## Notes

- If both Workflow type and a legacy Pipeline field are missing, default to `default_workflow` from the registry (`estimate-from-rate-file`) and prompt to confirm or change
- Never coerce an unknown name into a software-build or incident pipeline
