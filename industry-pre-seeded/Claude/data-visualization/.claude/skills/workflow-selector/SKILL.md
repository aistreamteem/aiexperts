---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled chart pack."
disable-model-invocation: false
---

# Workflow Selector

Presents the chart-pack menu from the registry and records selection in the journal.

When to use

- Called by continue when the Work Item journal is missing "Workflow type"
- On new Work Item or pack initialization

## Instructions

1. **Determine context type:**
   - Read `.claude/active-context.txt` to get `context_type` and `context_id`

2. **Read workflow registry:**
   - Read `.claude/workflows/workflow-registry.json`
   - Default job is `default_workflow` (`describe-csv` unless the registry says otherwise)

3. **Present menu from the registry only:**

   List each workflow in `workflow-registry.json` as a numbered line: name, then the description. Do not offer a workflow that is not in the registry. Do not offer developer, HLD/DD, incident, or leftover umbrella jobs.

4. **Accept user input:**
   - A number matching the menu, or a workflow name / filename stem (flexible parsing: "describe-csv", "Describe CSV", "histogram", "time series")

5. **Validate selection:** Ensure the workflow exists in the registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
   - "What is the Work Item ID?" (WID-…, or a dated slug such as `2026-11-08-sales-by-week`)
   - "What is the question, the source file, the columns, and the date range?" (see `docs/role/work-item-method.md`)

7. **Open the Work Item folder if needed:**
   - Create `work-items/<id>/` from `work-items/_TEMPLATE/` (include `in/`, `work/`, `out/`, `evidence/`, `facts/`, `STATUS.md`, `TODOS.md`)
   - Create `journals/work-items/<id>/` from `journals/work-items/_TEMPLATE/`
   - Put dropped source files in `in/` (or ask them to)

8. **Record in journal:**
   - Write `Workflow type` on `journals/work-items/<id>/progress.md`
   - Set Next action to the workflow’s first ready step (usually confirm question / intake), **not** a deleted process skill
   - Set `Context ID` on that journal

9. **Write active context file:**
   - Write `.claude/active-context.txt` as `work-item:<id>`
   - Set **Current work item** on `journals/expert/progress.md` when they asked to start this pack

10. **Confirm to user:**

    Work Item `<id>` initialized with `<workflow-name>`
    Initial phase: question (then intake)
    Next action: confirm question, source file, and columns, then the first map step in `.claude/workflows/<id>.md`

## Notes

- Live maps live under `.claude/workflows/<id>.md` and are self-contained
- If an old journal says "Pipeline", `operations`, or `developer`, map it to `default_workflow` and confirm
- Method note: `docs/role/work-item-method.md`
