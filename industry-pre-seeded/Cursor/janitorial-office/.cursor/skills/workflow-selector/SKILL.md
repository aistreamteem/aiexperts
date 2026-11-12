---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled role job."
disable-model-invocation: false
---

# Workflow Selector

Presents the janitorial-office role job menu and records the selection in the journal.

When to use

- Called by continue when the Work Item journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.cursor/active-context.txt` to get `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.cursor/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a workflow that is not in the registry. Do not offer software-build or incident-response pipelines.

 Role jobs live under `.cursor/workflows/`. Until the operator picks another job, the registry default is `complaint-callback`. Recurring nightly assignment is usually `night-board`.

4. **Accept user input:**
 - A number matching the menu, or a workflow name / id (`night-board`, `Night Board`, `complaint-callback`, …)

5. **Validate selection:** Ensure the workflow exists in the registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - "What is the Work Item ID or pack name? (e.g., WID-21411151 or `2026-09-15-clinic-night`)"
 - "Any source files already dropped? (site list, schedule CSV, par sheet, SDS index, quality form, complaint log, key log, contract PDFs)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.
 - Next action should be the first step of the selected workflow file (for example `sites` on night-board), not a deleted process skill.

8. **Write active context file:**
 - Write `.cursor/active-context.txt` as `<context_type>:<context_id>`
 - Do not write `.cursor/active-work-item.txt` (legacy; read-only fallback elsewhere)

9. **Confirm to user:**

 Work Item initialized with \<workflow-name>
 Initial phase: first step of that workflow
 Next action: follow `.cursor/workflows/<id>.md` (one ready step) → journal-keeper

## Workflow-Specific Fields to Record

**Role job:**
- Job id (registry key)
- Work Item folder `work-items/<id>/`
- Source files the operator named

## Notes

- Called by continue when journal is missing workflow type
- If a journal has "Pipeline" but no "Workflow type", map leftover generic pipeline names to `night-board` unless they name another registered job
