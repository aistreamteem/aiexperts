---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled childcare-office job."
trigger: Called by continue skill when journal missing workflow type
---

# Workflow Selector

Presents this role’s registered jobs and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.cursor/active-context.txt` to get `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.cursor/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow in `workflow-registry.json` as a numbered line: name, then the description from the registry. Do not offer a workflow that is not in the registry. Do not offer a software-build pipeline.

 Role jobs live under `.cursor/workflows/` (one instruction file per job). Until the operator picks another job, the default is `attendance-day`.

 Typical choices on this role:
 - Attendance Day — daily present/absent list
 - Pickup List Check — authorized adults vs sign-out
 - Missing Enrollment Forms — packet completeness
 - Ratio From Their Posted — their posted numbers only
 - Tuition From File — rates and ledger they dropped
 - Waitlist — openings they control
 - Licensing Packet Completeness — binder pages present/missing
 - Incident Routing — forms that still need a director signature
 - Holiday Calendar Pack — closures and tuition-charged days from their calendar

4. **Accept user input:**
 - A number matching the menu, or a workflow name (flexible parsing: job id such as `attendance-day`, display name such as `Attendance Day`)

5. **Validate selection:** Ensure workflow exists in registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - **All workflows:** "What is the Work Item ID or job label? (e.g., WID-21411151 or `2026-11-08-room-a-attendance`)"
 - **All contexts:** "Any source files to use? (attendance export, enrollment PDFs, pickup list, calendar file, tuition sheet, licensing checklist)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>` on that flat journal
 - Set **Current phase** to `intake` unless they already named a later phase
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.

8. **Write active context file:**
 - Write to `.cursor/active-context.txt` as `<context_type>:<context_id>`

9. **Confirm to user:**

 Work Item initialized with `<workflow-name>`
 Initial phase: intake (then gather-sources → build-list → director-gate → pack-out)
 Next action: follow `.cursor/workflows/<id>.md` one ready step → journal-keeper

## Workflow-Specific Fields to Record

**Role job:**
- Job id (registry key)
- Work Item folder `work-items/<id>/`
- Source files they named for `in/`
- No software-build or SEV-bridge fields

## Notes

- This skill is called by continue when journal missing workflow type
- Backward compatibility: If user has existing journal with "Pipeline" field but no "Workflow type", map `operations` and `developer` to `attendance-day` unless they name another registered job
