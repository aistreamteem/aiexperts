---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled TC job."
trigger: Called by continue skill when journal missing workflow type
---

# Workflow Selector

Presents the registered TC jobs and records the selection in the Work Item journal.

## When to use

- **continue** finds no **Workflow type** on the Work Item journal
- New Work Item initialization

## Instructions

1. Read `.cursor/active-context.txt` for `context_type` and `context_id`.
2. Read `.cursor/workflows/workflow-registry.json`.
3. List each workflow as a numbered line: **name**, then the registry description. Do not offer a job that is not in the registry. Do not offer software-build pipelines.
4. Until the operator picks another job, the default is **`dates-calendar`**.
5. Accept a number, a job id (`missing-docs`), or a display name (`Missing Docs`).
6. Ask:
   - Work Item ID or label (WID-… or address + buy/list side)
   - Transaction file label as they named it
   - Source files already in `in/` or still needed (executed contract, amendments, checklists, PDF folders)
7. Write **Workflow type** on `journals/work-items/<id>/progress.md` when missing. Do not replace `active`. Set **Next action** on `nodes/work-item.md` to the workflow’s first step when `active` is still just `work-item`.
8. Write `.cursor/active-context.txt` as `work-item:<id>` only (do not write the legacy `.cursor/active-work-item.txt`).
9. Confirm:

```
Work Item initialized: <name>
Method: docs/role/work-item-method.md
First step: follow .cursor/workflows/<id>.md (intake / first map step)
Next: continue walks that step, then journal-keeper
```

## Fields to record

- Job id (registry key)
- Transaction file label
- Source files expected
- No software-build fields

## Notes

If an old journal has a **Pipeline** field but no **Workflow type**, map it to `dates-calendar` unless they name another registered job.
