---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled hotel-role job."
disable-model-invocation: false
---

# Workflow Selector

Presents the hotel-role job menu and records selection in the Work Item journal.

When to use

- Called by continue skill when journal is missing "Workflow type" field
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` to get `context_type` and `context_id`
 - If `context_type=work-item`: working on a named role job

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json` to get available workflows.

3. **Present menu to user from the registry only:**

 List each workflow in `workflow-registry.json` as a numbered line: name, then the description from the registry. Do not offer a workflow that is not in the registry. define-role rewrites the registry when the user approves a role, so this menu is the enabled set.

 Until that approval changes it, the registry contains the role jobs listed in `workflow-registry.json` (default: `arrivals-day`). Offer each registry key by name and description. Do not invent extra pipelines that are not in the registry. Do not offer `developer` or `production-incident`.

 Typical menu (keep in sync with the registry): Arrivals Day, Departures Due Out, Folio Exceptions, Group Block Vs Pickup, House Count, Night Audit File Check, No Show List, Ooo And Status, Tax Exempt Completeness.

4. **Accept user input:**
 - Work item: a number matching the menu, or a workflow name (flexible parsing: job id, display name, and any other name present in the registry)

5. **Validate selection:** Ensure workflow exists in registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - **Work item (all workflows):** "What is the Work Item ID? (e.g., WID-21411151)" If they only have a stay date, propose `WID-` plus a compact date label and confirm.
 - **All contexts:** "Any source files for this job? (PMS exports, folio PDFs, tax files, room-status sheets, group sheet, night-audit PDF)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>` on that flat journal
 - Set Next action to the workflow’s first step (from the instruction file)
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.

8. **Write active context file:**
 - Write to `.claude/active-context.txt` as `work-item:<context_id>`
 - Do not write the legacy `.claude/active-work-item.txt`
 - Update **Current work item:** on `journals/expert/progress.md`

9. **Create folders if needed:**
 - Ensure `work-items/<id>/{in,work,out,evidence,facts}` exist (copy from `work-items/_TEMPLATE/` when creating new).

10. **Confirm to user:**

 Work Item initialized with <workflow-name>  
 Initial phase: identify / intake (see `docs/role/work-item-method.md`)  
 Next action: <first step from the instruction file>  
 Drop source files in `work-items/<id>/in/`

## Workflow-Specific Fields to Record

**Role job:**
- Job id from `workflow-registry.json`
- Work Item folder `work-items/<id>/`
- Source files named by the operator (PMS export, folio PDF, tax file, room-status sheet)

## Notes

- This skill is called by continue.md when journal missing workflow type
- Backward compatibility: If user has existing journal with "Pipeline" field but no "Workflow type", map old pipeline names to registry ids when they match a role job.
