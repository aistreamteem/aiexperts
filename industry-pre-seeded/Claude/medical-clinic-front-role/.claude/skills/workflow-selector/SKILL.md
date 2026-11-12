---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the operator to select an enabled clinic-role job."
disable-model-invocation: false
---

# Workflow Selector

Presents this role’s registered jobs and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context:**
 - Read `.claude/active-context.txt` for `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a workflow that is not in the registry.

 Clinic-role jobs live under `.claude/workflows/`. Until the operator picks another job, the default is `day-list` (open the day from the schedule export). See `docs/role/work-item-method.md` for which job covers which phase.

4. **Accept input:**
 - A number matching the menu, or a workflow id / display name in the registry (`day-list`, `Day List`, `eligibility-from-screenshot`, and so on)

5. **Validate:** If invalid, re-prompt.

6. **Ask:**
 - "What is the Work Item ID or pack name? (e.g., WID-21411151 or `2026-11-10-day-list`)"
 - "Any source files for `in/`? (EHR export, eligibility screenshot, intake PDFs, ROI folder, close report)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.

8. **Write active context:**
 - `.claude/active-context.txt` as `work-item:<context_id>`
 - Do not write the legacy `.claude/active-work-item.txt`

9. **Confirm:**

 Work Item initialized with \<workflow-name>
 Initial phase: first step in that workflow file (see work-item-method)
 Next action: follow `.claude/workflows/<id>.md` → produce the first artifact under `work-items/<id>/` → journal-keeper

## Workflow-specific fields

**Role job:**
- Job id (registry key)
- Work Item folder `work-items/<id>/`
- No software-build or incident-response fields

## Notes

- Called by continue when journal is missing workflow type
- Backward compatibility: If a journal has "Pipeline" but no "Workflow type", map leftover software-build or incident names to `day-list` unless they name another registered job
