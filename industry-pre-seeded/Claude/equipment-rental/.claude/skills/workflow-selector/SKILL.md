---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled role job."
trigger: Called by continue skill when journal missing workflow type
---

# Workflow Selector

Presents the equipment-rental job menu and records the selection in the Work Item journal.

When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` to get `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a job that is not in the registry.

 Jobs live under `.claude/workflows/`. Until the operator picks another job, the default is `contract-completeness`.

 Typical matches (also in `docs/role/work-item-method.md`):
 - Today’s book / reserved vs available → `reservation-day`
 - Contract PDFs vs required fields → `contract-completeness`
 - Commercial insurance missing → `renter-coi-missing`
 - Units leaving the yard → `outgoing-inspection`
 - Drops and pickups → `delivery-tickets`
 - Hours / GPS vs inspection → `meter-exceptions`
 - PM due vs bookings → `maintenance-due`
 - Check-in vs outgoing → `return-damage`
 - On-rent percent / idle list → `utilization`

4. **Accept user input:** a number, a job id (`contract-completeness`), or a display name (`Contract Completeness`).

5. **Validate** against the registry. If invalid, re-prompt.

6. **Ask:**
 - "What is the Work Item ID or job folder? (e.g., WID-21411151 or a contract/day name)"
 - "Any files to use? (fleet export, rate file, contract PDFs, inspection sheets, photos, COI folder, zone sheet, PM file, meter export)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing.
 - Set `Context ID: <context_id>`
 - Set next action to the first step of the selected job’s instruction file (the first `steps[].id` in the YAML).
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`.

8. **Write active context file:** `.claude/active-context.txt` as `<context_type>:<context_id>`. Do not write the legacy `.claude/active-work-item.txt`.

9. **Confirm:**

 Work Item initialized with <workflow-name>
 Initial phase: first step of that job
 Next action: follow `.claude/workflows/<id>.md` (one ready step) → journal-keeper

## Workflow-specific fields

**Role job:**
- Job id (registry key)
- Work Item folder `work-items/<id>/`
- No developer or production-incident fields

## Notes

- If the operator has an old journal with "Pipeline" but no "Workflow type", map leftover `operations` / `developer` names to `contract-completeness` unless they name another registered job.
