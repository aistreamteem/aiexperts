---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---
## Switch Context

Switches the active Work Item context on this janitorial-office role.

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a Work Item or pack name (`2026-09-15-clinic-night`)

## Instructions

1. **Parse user request:**
 - Extract ID from user message
 - If it starts with "WID-" or looks like a pack/site-night name → `context_type=work-item`
 - If ambiguous: ask for a Work Item ID or pack name

2. **Check if context exists:**
 - Check `work-items/<id>/`
 - If missing: "This Work Item doesn't exist yet. Create it? (yes/no)"
 - If yes: **workflow-selector** to initialize
 - If no: Exit

3. **Read current context** from `.cursor/active-context.txt` and display it.

4. **Confirm switch.** If no, exit.

5. **Write new context:**
 - `.cursor/active-context.txt` as `work-item:<id>`
 - Do not write `.cursor/active-work-item.txt` (legacy; read-only fallback elsewhere)
 - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord. Do not move `active` in this skill.

6. **Confirm:**
```
Switched to Work Item {id}
Root path: work-items/{id}/
Journal: journals/work-items/{id}/progress.md
Workflow: {workflow_type}
Next action: {next_action}
```

7. Display journal status (current step, open questions). Ask: "Would you like to continue from here? (say 'continue' to proceed)"

## Examples

**Existing pack**
```
User: "switch to work item 2026-09-15-clinic-night"
Agent: "Current context: Work Item WID-100000001. Switch to 2026-09-15-clinic-night? (yes/no)"
User: "yes"
Agent: "Switched. Workflow: night-board. Next action: pack. Would you like to continue?"
```

**Doesn't exist**
```
User: "switch to work item WID-999999999"
Agent: "Work Item WID-999999999 doesn't exist yet. Create it? (yes/no)"
User: "yes"
Agent: [workflow-selector]
```

## Notes

Switching does not lose the previous pack. State stays in that Work Item’s journal.
