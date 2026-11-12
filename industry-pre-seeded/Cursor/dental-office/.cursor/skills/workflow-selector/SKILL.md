---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled dental-role job."
disable-model-invocation: false
---

# Workflow Selector

Presents this office's registered role jobs and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.cursor/active-context.txt` for `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.cursor/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a workflow that is not in the registry.

 Dental-role jobs live under `.cursor/workflows/`. Until the operator picks another job, the default is `day-list` (morning chair list / huddle sheet).

4. **Accept input:**
 - A number, a job id such as `day-list`, or a display name such as `Day List`

5. **Validate:** If invalid, re-prompt.

6. **Ask context-specific questions:**
 - "What is the Work Item ID or job folder? (e.g., WID-21411151 or 2026-11-10-day-list)"
 - "Any source files? (schedule export, claim PDF, eligibility screenshot, EOB, recall CSV)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`

8. **Write active context file:**
 - Write `.cursor/active-context.txt` as `<context_type>:<context_id>`
 - Do not write `.cursor/active-work-item.txt` (legacy; hooks may still read it)

9. **Confirm:**

 Work Item initialized with \<workflow-name>
 Initial phase: intake (source files in `in/`)
 Next action: first ready map step in the selected `.cursor/workflows/<id>.md` → journal-keeper

## Workflow-specific fields

**Role job:**
- Job id (registry key)
- Work Item folder `work-items/<id>/`
- Source file names the operator pointed at
- Record only dental-role job fields

## Notes

- Called by continue when journal is missing workflow type
- Backward compatibility: If the journal has "Pipeline" but no "Workflow type", map it to `day-list` unless they name another registered job
