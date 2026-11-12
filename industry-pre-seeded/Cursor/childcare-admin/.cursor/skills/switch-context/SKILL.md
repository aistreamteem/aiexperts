---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---
## Switch Context

Switches the active Work Item context.

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a work item (including labels like `2026-11-08-room-a-attendance`)

## Instructions

1. **Parse user request:**
 - Extract ID from user message
 - If it starts with "WID-" or looks like a job label, `context_type=work-item`
 - If ambiguous: ask for a Work Item ID or job label

2. **Check if context exists:**
 - Check `work-items/<id>/`
 - If missing: "This Work Item doesn't exist yet. Create it? (yes/no)"
 - If yes: run **workflow-selector** to initialize
 - If no: Exit

3. **Read current context** from `.cursor/active-context.txt` and display it.

4. **Confirm switch.** If no, exit.

5. **Write new context:**
 - `.cursor/active-context.txt` as `work-item:<id>`
 - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord. Read the active branch from `journals/work-items/<id>/state.json`. Do not move `active` in this skill.

6. **Confirm:**
```
Switched to Work Item {id}
Root: work-items/{id}/
Journal: journals/work-items/{id}/progress.md
Workflow: {workflow type from journal}
Next action: {from active node}
```

7. Display current phase, next action, and open director questions. Ask: "Would you like to continue from here?"

## Examples

**Example 1:** Switch from today's attendance pack to a missing-forms job.

```
User: "switch to work item 2026-11-08-child-442-packet"
Agent: "Current context: 2026-11-08-room-a-attendance. Switch? (yes/no)"
User: "yes"
Agent: "Switched. Current phase: build-list. Next action: wait for director on missing photo-release page. Say continue to proceed."
```

**Example 2:** New id → workflow-selector (offer attendance-day, pickup-list-check, missing-enrollment-forms, …).

## Notes

- Switching does not lose work in the previous Work Item
- Do not use software-design approval examples on this role
