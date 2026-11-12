---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled collision-shop office job."
disable-model-invocation: false
---

# Workflow Selector

Presents this role’s job menu and records the selection in the Work Item journal.

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

 Role jobs live under `.claude/workflows/`. Until the operator picks another job, the default is `assignment-intake`.

 Typical mapping (also in `docs/role/work-item-method.md`):
 - New assignment / claim open → `assignment-intake`
 - Photo folder to index → `photo-index`
 - Write or pack an estimate from their files → `estimate-from-files`
 - Procedure PDFs vs operations → `oem-procedure-present`
 - Auth vs estimate dollars → `authorization-missing`
 - First-write vs later dollars → `supplement-log`
 - PO sheet vs estimate lines → `parts-order-vs-estimate`
 - Insurer vs deductible vs customer-pay → `customer-pay-vs-insurer`
 - Stage dates / keys-to-keys list → `cycle-time-list`

4. **Accept user input:**
 - A number matching the menu, or a workflow name (id such as `estimate-from-files`, display name such as `Estimate From Files`)

5. **Validate selection:** Ensure the workflow exists in the registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - "What is the Work Item ID or job folder? (e.g., WID-21411151 or 2026-09-15-ro-2104)"
 - "Any external references? (assignment sheet, estimate export, photo folder, portal screenshot)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>` on that flat journal
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.

8. **Write active context file:**
 - Write `.claude/active-context.txt` as `<context_type>:<context_id>`


9. **Confirm to user:**

 Work Item initialized with \<workflow-name>
 Initial phase: first YAML step in that workflow file (see `docs/role/work-item-method.md`)
 Next action: continue — walk one ready step, write under `work-items/<id>/`, journal-keeper

## Workflow-Specific Fields to Record

**Role job:**
- Job id (registry key)
- Work Item folder `work-items/<id>/`
- No coding-pipeline or incident-session fields

## Notes

- Called by continue when journal is missing workflow type
- Backward compatibility: If user has "Pipeline" but no "Workflow type", map it to `assignment-intake` unless they name another registered job
