---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled role job."
disable-model-invocation: false
---

# Workflow Selector

Presents the role-job menu and records selection in the Work Item journal.

When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` to get `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a workflow that is not in the registry.

 Role jobs live under `.claude/workflows/`. Until the operator picks another job, the default is `dates-calendar`.

4. **Accept user input:**
 - A number matching the menu, or a workflow name (id such as `missing-docs`, display name such as `Missing Docs`)

5. **Validate selection:** Ensure the workflow exists in the registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - "What is the Work Item ID or file label? (e.g., WID-4412 or 12-oak-buy)"
 - "Any files to use? (executed contract PDF, amendments, title/HOA packet, their TC checklist)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.

8. **Write active context file:**
 - Write `.claude/active-context.txt` as `work-item:<context_id>`
 - Do not write `.claude/active-work-item.txt` (legacy read-only)

9. **Confirm to user:**

 Work Item initialized with <workflow-name>
 Initial phase: role-job (see `docs/role/work-item-method.md`)
 Next action: first step in `.claude/workflows/<id>.md` → journal-keeper

## Workflow-Specific Fields to Record

**Role job:**
- Job id (registry key)
- Work Item folder `work-items/<id>/`
- No software-build or incident-response fields

## Notes

- Called by continue when the journal is missing workflow type
- Backward compatibility: If the journal has "Pipeline" but no "Workflow type", map it to `dates-calendar` unless they name another registered job
