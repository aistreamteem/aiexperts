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
 - If `context_type=work-item`: working on a named role job (one RO pack, board list, MPI, estimate, auth gap, findings, parts, comeback, or pickup)

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json` to get available workflows.
 - If the journal has no workflow type, use `default_workflow` (`one-ro`) when the operator does not pick another job.

3. **Present menu to user from the registry only:**

 List each workflow in `workflow-registry.json` as a numbered line: name, then the description from the registry. Do not offer a workflow that is not in the registry. define-role rewrites the registry when the user approves a role, so this menu is the enabled set.

 This seed's role jobs: one-ro, open-ros, mpi-pack, estimate-pack, auth-gap, additional-findings, parts-status, comeback, pickup-invoice.

4. **Accept user input:**
 - Work item: a number matching the menu, or a workflow name (flexible parsing: job id, display name, and any other name present in the registry)

5. **Validate selection:** Ensure workflow exists in registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - **Work item (all workflows):** "What is the Work Item ID? (e.g., WID-21411151 or the RO / pack name)"
 - **All contexts:** "Any external references? (RO export, MPI form, parts file, invoice PDF)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>` on that flat journal
 - Set `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.
 - Initial phase is `role-job` for every registered role job.

8. **Write active context file:**
 - Write to `.claude/active-context.txt` as `<context_type>:<context_id>`
 - Do not write the legacy `.claude/active-work-item.txt` pointer.

9. **Confirm to user:**

 Work Item initialized with \<workflow-name\>
 Initial phase: role-job
 Next action: continue the first ready step in `.claude/workflows/<id>.md` (artifacts under `work-items/<id>/`)

## Notes

- This skill is called by continue when journal missing workflow type
- Do not offer leftover developer or incident names. Those are not in the registry.
- Backward compatibility: If user has existing journal with "Pipeline" or "Workflow type" of `operations` or `developer`, map those to `one-ro` (the default role job) unless they name another registered job.
- Method note: `docs/role/work-item-method.md`
