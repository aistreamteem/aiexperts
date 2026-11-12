---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled pipeline."
trigger: Called by continue skill when journal missing workflow type
---

# Workflow Selector

Presents workflow type menu to user and records selection in journal.

When to use

- Called by continue skill when journal is missing "Workflow type" field
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.cursor/active-context.txt` to get `context_type` and `context_id`
 - If `context_type=work-item`: working on a named role job

2. **Read workflow registry:**
 - Read `.cursor/workflows/workflow-registry.json` to get available workflows.

3. **Present menu to user from the registry only:**

 List each workflow in `workflow-registry.json` as a numbered line: name, then the description from the registry. Do not offer a workflow that is not in the registry. define-role rewrites the registry when the user approves a role, so this menu is the enabled set.

 Until that approval changes it, the registry contains the HOA / association admin role jobs (default: `acc-completeness`). Do not offer Developer Pipeline or an operations umbrella.

4. **Accept user input:**
 - Work item: a number matching the menu, or a workflow name (flexible parsing: "acc-completeness", "ACC Completeness", and any other name present in the registry)

5. **Validate selection:** Ensure workflow exists in registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - **Work item (all workflows):** "What is the Work Item ID? (e.g., WID-21411151)"
 - **All contexts:** "Any external references? (files, association name, meeting date, prior write-ups)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>` on that flat journal
 - Set workflow-specific fields on that flat journal
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.

8. **Write active context file:**
 - Write to `.cursor/active-context.txt` as `<context_type>:<context_id>`

9. **Confirm to user:**

 Work Item initialized with <workflow-name>
 Initial phase: identify / intake (see docs/role/work-item-method.md)
 Next action: first ready YAML step in `.cursor/workflows/<id>.md`

## Workflow-Specific Fields to Record

**Role jobs:**
- Association / community name if known
- As-of date, meeting date, lot, or project name if the job needs one
- Initial phase is `identify` then `intake` (method note). Registry `initial_phase` remains `role-job`.

## Notes

- This skill is called by continue when the journal is missing Workflow type
- Offer only keys in `workflow-registry.json`. Do not offer a software-build or incident-bridge pipeline.
- If a journal has a legacy "Pipeline" field but no "Workflow type", map only names that exist in the registry.
