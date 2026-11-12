---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled catering role job."
disable-model-invocation: false
---

# Workflow Selector

Presents the catering-job menu from the registry and records the selection in the journal.

When to use

- Called by continue skill when journal is missing "Workflow type" field
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` to get `context_type` and `context_id`
 - Jobs live under `work-items/<id>/`

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json` to get available workflows.
 - Instruction files live under `.claude/workflows/<job-id>.md`.
 - Default job is `default_workflow` in the registry (`week-of-events` for this role).

3. **Present menu to user from the registry only:**

 List each workflow in `workflow-registry.json` as a numbered line: name, then the description from the registry. Do not offer a workflow that is not in the registry. Do not offer developer, HLD/DD, or production-incident pipelines. define-role rewrites the registry when the user approves a role, so this menu is the enabled set.

4. **Accept user input:**
 - A number matching the menu, or a workflow name / job id (flexible parsing: filename stem, display name, or any other name present in the registry)

5. **Validate selection:** Ensure workflow exists in registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - Which event, date, week, or pack is this job for?
 - Any files to use? (order PDFs, dietary sheets, rental POs, calendars, leftover-form folders)

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>` on that flat journal
 - Set `Next action` to the first ready step in the selected `.claude/workflows/<job-id>.md` file (create `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/` if needed)

8. **Write active context file:**
 - Write to `.claude/active-context.txt` as `<context_type>:<context_id>`

9. **Confirm to user:**

 Work Item initialized with <workflow-name>
 Initial phase: role-job
 Next action: first ready step in the selected catering workflow file

## Notes

- This skill is called by continue when the journal is missing workflow type
- Every registered job is a role job (`initial_phase`: `role-job`)
- Role memory: `facts/facts-operations.md` and `facts/rules-operations.md`
- Method: `docs/role/work-item-method.md`
