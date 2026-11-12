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
 - If `context_type=work-item`: working on a salon-role job

2. **Read workflow registry:**
 - Read `.cursor/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a job that is not in the registry. Do not offer software-build or incident pipelines.

 Until the operator changes it, the registry contains the salon / spa front-role jobs. Default workflow: `days-book`.

 Typical matches:
 - Today’s or tomorrow’s calendar export → Days Book
 - Guests due a confirmation (they send) → Reminder List
 - Open slots vs waitlist names → Waitlist Gaps
 - Booked services vs menu file → Menu Vs Book
 - Cancelled / no-show rows vs policy → No Show List
 - POS tenders, tips, voids → Closeout
 - Gift-card sales and remaining balances → Gift Card Recon
 - Retail on-hand / par sheet → Retail Count
 - House employees vs booth renters → Booth Split

4. **Accept input:** a number, a registry id, or a display name.

5. **Validate:** If invalid, re-prompt.

6. **Ask:**
 - "What is the Work Item ID? (e.g., WID-20261108)"
 - "Any external references? (chat threads, booking/POS files, source files)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item` (first YAML step of the selected job, usually intake / first `needs: []` step)

8. **Write active context file:**
 - `.cursor/active-context.txt` as `<context_type>:<context_id>` (do not write the legacy `.cursor/active-work-item.txt`)

9. **Confirm:**

 Work Item initialized with \<workflow-name\>
 Initial phase: isolate / intake
 Next action: first YAML step in that job’s instruction file

## Notes

- If both Workflow type and a legacy Pipeline field are missing, default to `default_workflow` from the registry (`days-book`) and prompt to confirm or change
- Never coerce an unknown name into a software-build or incident pipeline
