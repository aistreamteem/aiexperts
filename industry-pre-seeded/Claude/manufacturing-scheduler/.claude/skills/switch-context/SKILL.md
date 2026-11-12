---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active pack. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---

## Switch Context

Switches the active production-scheduler Work Item (pack).

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a Work Item or dated pack name (e.g. `2026-11-08-dispatch`)

## Instructions

1. **Parse user request:**
   - Extract ID from user message
   - Treat as `context_type=work-item` (this role only uses Work Item packs)
   - If ambiguous: ask for a Work Item id or pack name

2. **Check if context exists:**
   - Check `work-items/<id>/`
   - If missing: Ask "This pack doesn't exist yet. Create it? (yes/no)"
   - If yes: **workflow-selector** to initialize
   - If no: Exit

3. **Read current context** from `.claude/active-context.txt`. Display: "Current pack: {current_id}"

4. **Confirm switch.** If no, exit.

5. **Write new context:**
   - `.claude/active-context.txt` as `work-item:<id>` only (do not write the legacy `.claude/active-work-item.txt`)
   - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord. Read `journals/work-items/<id>/state.json`. Do not move `active` in this skill.

6. **Confirm:**

```
Switched to Work Item {id}
Root: work-items/{id}/
Journal: journals/work-items/{id}/progress.md
Workflow: {workflow type from journal}
Next action: {next action}
```

7. Display journal status (phase, next action, open questions). Ask if they want to **continue**.

## Examples

**Switch to an existing dispatch pack**
```
User: "switch to work item 2026-11-08-dispatch"
Agent: "Current pack: WID-100000001. Switch to 2026-11-08-dispatch? (yes/no)"
User: "yes"
Agent: "Switched. Workflow: dispatch-list. Next action: wait for WO export. Say continue to proceed."
```

**Pack doesn't exist**
```
User: "switch to work item WID-999999999"
Agent: "WID-999999999 doesn't exist yet. Create it? (yes/no)"
User: "yes"
Agent: [workflow-selector]
```

## Notes

- Switching does not lose the previous pack. Journals stay in place.
- This is a shop pack switch, not a software-delivery gate.

