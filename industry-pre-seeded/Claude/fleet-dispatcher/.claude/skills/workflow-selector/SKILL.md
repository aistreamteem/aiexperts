---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled role job."
trigger: Called by continue skill when journal missing workflow type
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

 List each workflow in `workflow-registry.json` as a numbered line: name, then the description from the registry. Do not offer a workflow that is not in the registry.

 Until that approval changes it, the registry contains these role jobs (default: `assignment-pack`):

 1. Assignment Pack — Who is on which unit from the roster for the date.
 2. Breakdown — Unit down pack from their exception or GPS export.
 3. Detention — In and out times from their scan, route sheet, or site file.
 4. DVIR Gap — Which units on today’s roster have a DVIR file.
 5. Exceptions — Late, breakdown, failed, and missing-POD rows from the day’s files.
 6. Fuel Outliers — Compare the fuel CSV to units on the roster; odd gallons are questions.
 7. HOS Questions — List gaps from their ELD export as questions.
 8. POD Check — Match required stops to files in the POD folder.
 9. Today's Routes — Stops and missing PODs from their sheet for one service date.

4. **Accept user input:**
 - Work item: a number matching the menu, or a workflow name (flexible parsing: "assignment-pack", "Assignment Pack", and any other name present in the registry)

5. **Validate selection:** Ensure workflow exists in registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - **Work item (all workflows):** "What is the Work Item ID? (e.g., WID-21411151 or a dated pack name such as 2026-09-15-truck-14-route-a)"
 - **All contexts:** "Any external references? (chat threads, TMS tickets, ELD/GPS export dates, documentation pages)"
 - Optional: service date, unit, driver, or source file for the pack

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>` on that flat journal
 - Set workflow-specific fields on that flat journal
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.

8. **Write active context file:**
 - Write to `.claude/active-context.txt` as `<context_type>:<context_id>`
 - Do not write `.claude/active-work-item.txt` (legacy; read-only fallback elsewhere)

9. **Confirm to user:**

 Work Item initialized with \<workflow-name\>
 Initial phase: see `docs/role/work-item-method.md` (intake / assignment / routes / DVIR / exceptions / POD / file questions)
 Next action: first ready step in `.claude/workflows/<workflow-id>.md`

## Workflow-Specific Fields to Record

**Role jobs:**
- No additional fields beyond Work Item ID unless the operator names a date, unit, driver, or source file for the pack.

## Notes

- This skill is called by continue when the journal is missing workflow type
- Backward compatibility: If user has existing journal with "Pipeline" field but no "Workflow type", map any leftover pipeline name to the registry `default_workflow` (`assignment-pack`) unless the operator names a specific role job
