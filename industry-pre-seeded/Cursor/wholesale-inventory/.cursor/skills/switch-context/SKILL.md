---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---

# Switch Context

Switches the active Work Item (one receipt, count date, pick, transfer, RMA, or reorder pull).

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a work item or pack folder name

## Instructions

1. Parse the id. If it starts with `WID-` or matches an existing `work-items/<id>/`, `context_type=work-item`. If ambiguous, ask for the Work Item id or short name.
2. If `work-items/<id>/` does not exist, ask whether to create it. If yes, copy `work-items/_TEMPLATE/` and run **workflow-selector**. If no, stop.
3. Read `.cursor/active-context.txt`. Show “Current context: Work Item {current_id}”.
4. Confirm the switch. If no, stop.
5. Write `.cursor/active-context.txt` as `work-item:<id>` only (do not write the legacy `.cursor/active-work-item.txt` pointer). Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching on purpose. Do not move `active` in `state.json`.
6. Confirm paths: root `work-items/<id>/`, journal `journals/work-items/<id>/progress.md`. Show current workflow, next action, and open questions. Ask if they want to **continue**.

## Examples

**Switch to existing job**
```
User: "switch to work item WID-20261108"
Agent: "Current context: Work Item WID-20261101 (cycle-count aisle B). Switch to WID-20261108? (yes/no)"
User: "yes"
Agent: "Switched. Workflow: receiving-match. Next action: wait for PO PDF. Say continue to resume."
```

Switching does not lose the previous job. Journals stay in each Work Item.
