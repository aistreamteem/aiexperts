---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled role job."
disable-model-invocation: false
---

# Workflow Selector

Presents workflow type menu to user and records selection in journal.

When to use

- Called by continue skill when journal is missing "Workflow type" field
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` to get `context_type` and `context_id`
 - If `context_type=work-item`: working on a role job

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json` to get available workflows.

3. **Present menu to user from the registry only:**

 List each workflow in `workflow-registry.json` as a numbered line: name, then the description from the registry. Do not offer a workflow that is not in the registry. define-role rewrites the registry when the user approves a role, so this menu is the enabled set.

 Until that approval changes it, the registry contains the role jobs for this seed (default `boarding-day`): boarding-day, capacity-vs-booked, feeding-from-cards, incident-routing, meds-to-give-list-as-written, missing-vaccine-files, pickup-list, waitlist, waiver-missing.

4. **Accept user input:**
 - Work item: a number matching the menu, or a workflow name (flexible parsing: job id such as "boarding-day", display name such as "Boarding Day", and any other name present in the registry)

5. **Validate selection:** Ensure workflow exists in registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - **Work item (all workflows):** "What is the Work Item ID? (e.g., WID-21411151 or a named role job folder)"
 - **All contexts:** "Any external references? (chat threads, occupancy date, patient-dog label, documentation pages)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>` on that flat journal
 - Set workflow-specific fields on that flat journal
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.

8. **Write active context file:**
 - Write to `.claude/active-context.txt` as `<context_type>:<context_id>`
 - Do not write `.claude/active-work-item.txt` (legacy; read fallback only)

9. **Confirm to user:**

 ✅ Work Item initialized with <workflow-name>
 Initial phase: isolate / intake
 Next action: <first YAML step or wait for file>

## Workflow-Specific Fields to Record

**Role job:**
- Stay date or occupancy day if the chosen map names them
- Patient-dog label if this pack is for one dog

## Notes

- This skill is called by continue when the journal is missing workflow type
- Do not offer software-build or incident-response pipelines
- Backward compatibility: If user has existing journal with "Pipeline" field but no "Workflow type", map old pipeline names to the matching role job id, or to `default_workflow` (`boarding-day`)
