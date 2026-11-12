---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---
## Switch Context

Switches the active Work Item context.

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a work item

## Instructions

1. **Parse user request:**
 - Extract ID from user message
 - If it starts with "WID-" → `context_type=work-item`
 - If ambiguous: ask for a Work Item ID (WID-XXXXXXXX)

2. **Check if context exists:**
 - Check `work-items/<id>/`
 - If missing: Ask "This Work Item doesn't exist yet. Create it? (yes/no)"
 - If yes: **workflow-selector** to initialize
 - If no: Exit

3. **Read current context** from `.cursor/active-context.txt` and show it.

4. **Confirm switch.** If no, exit.

5. **Write new context:**
 - `.cursor/active-context.txt` as `work-item:<id>`
 - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord. Read `active` from `journals/work-items/<id>/state.json`. Do not move `active` in this skill.

6. **Confirm** with journal path, workflow type, and next action.

7. **Display journal status** (current map step, open questions, blockers). Ask: "Would you like to continue from here? (say 'continue' to proceed)"

## Examples

**Example 1: Switch to an existing assignment-board job**
```
User: "switch to work item WID-20261108"
Agent: "Current context: Work Item WID-20261101. Switch to Work Item WID-20261108? (yes/no)"
User: "yes"
Agent: "Switched to WID-20261108. Workflow: assignment-board. Next action: produce the board CSV. Say continue to proceed."
```

**Example 2: Context doesn't exist**
```
User: "switch to work item WID-999999999"
Agent: "Work Item WID-999999999 doesn't exist yet. Create it? (yes/no)"
User: "yes"
Agent: [workflow-selector]
```

## Notes

- Switching does not lose work in the previous Work Item
- Each assignment week, timesheet period, or credential pack keeps its own folder
