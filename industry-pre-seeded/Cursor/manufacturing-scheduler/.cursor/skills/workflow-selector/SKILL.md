---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select a registered production-scheduler job."
disable-model-invocation: false
---

# Workflow Selector

Presents the registered shop jobs and records the selection in the Work Item journal.

## When to use

- Called by **continue** when the journal is missing "Workflow type"
- On new Work Item initialization
- Operator asks to start a dispatch, kit, shortage, traveler, WIP, due-date, outside-process, machine-down, or pending-ECO pack

## Instructions

1. Read `.cursor/active-context.txt` for `context_type` and `context_id`. If missing, ask for a Work Item id (WID-… or a dated board name) and write `work-item:<id>` only to `.cursor/active-context.txt` (do not write the legacy `.cursor/active-work-item.txt`).

2. Read `.cursor/workflows/workflow-registry.json`.

3. Present **only** registry jobs as a numbered list (name + description). Default until they pick another: `dispatch-list`.

   Registered jobs: Dispatch List; Due Date List; Pending ECO as File; Kit List; Machine-Down versus WIP; Outside-Process Due List; Shortage List versus Inventory; Traveler Completeness Pack; WIP by Work Center.

4. Accept a number, a registry key (`dispatch-list`), or a display name.

5. Validate against the registry. If invalid, re-prompt.

6. Ask:
   - "What is the Work Item ID or pack name? (e.g., WID-21411151 or 2026-11-08-dispatch)"
   - "Which source files do you have? (work-order export, inventory export, calendar, traveler PDFs, ECO log, machine-status, outside-PO list)"

7. Ensure `work-items/<id>/` exists (copy `_TEMPLATE` if needed) and `journals/work-items/<id>/` exists.

8. Record on `journals/work-items/<id>/progress.md`:
   - **Workflow type:** `<registry key>`
   - Context ID
   - Pack description
   - Next action: first step of that workflow file (see `.cursor/workflows/<id>.md`)
   Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`.

9. Confirm:

```
Work Item initialized: <name>
Workflow: <registry key>
Initial phase: intake (see docs/role/work-item-method.md)
Next: put source files in work-items/<id>/in/, then continue the first ready step of .cursor/workflows/<id>.md
```

Offer only registry jobs. This role’s method is shop-control packs, not software delivery.
