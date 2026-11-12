---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled role job."
disable-model-invocation: false
---

# Workflow Selector

Presents this role’s job menu and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.cursor/active-context.txt` for `context_type` and `context_id`
 - If `context_type=work-item`: working on a church-office role job

2. **Read workflow registry:**
 - Read `.cursor/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a job that is not in the registry. Do not offer software-build or incident pipelines.

 Until the operator changes it, the registry contains the church-office admin jobs. Default workflow: `week-calendar`.

 Typical matches:
 - Background dates vs date-required volunteer roles → Background Dates As File
 - Board/session folder vs packet list → Board Pack
 - Outside facility use missing a COI → Facility COI Missing
 - Named giving batch vs signed count sheet → Giving Batch From Export
 - Blank or unknown fund codes → Missing Fund Codes
 - Pledge sheet vs gifts counted toward it → Pledge vs Received
 - Contribution-statement run from their process file → Statement Run List — Their Process
 - Ministry team list from their export → Volunteer Roster
 - Week’s room and building pack → Week Calendar

4. **Accept input:** a number, a registry id, or a display name.

5. **Validate:** If invalid, re-prompt.

6. **Ask:**
 - "What is the Work Item ID? (e.g., WID-20261108)"
 - "Any external references? (chat threads, Sunday date, batch name, source files)"

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

- If both Workflow type and a legacy Pipeline field are missing, default to `default_workflow` from the registry (`week-calendar`) and prompt to confirm or change
- Never coerce an unknown name into a software-build or incident pipeline
