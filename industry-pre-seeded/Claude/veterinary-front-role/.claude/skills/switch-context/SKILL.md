---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---
## Switch Context

Switches the active Work Item context for this clinic role.

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a work item (including a clinic-date pack name)

## Instructions

1. **Parse user request:**
 - Extract ID from user message
 - Determine context type by the **shape of the ID first**, then fall back to keywords:
 - If starts with "WID-" or looks like a pack name (`2026-11-10-day-appointments`) → `context_type=work-item`
 - If ambiguous: ask for a Work Item ID or pack name

2. **Check if context exists:**
 - Check if `work-items/<id>/` exists
 - If folder doesn't exist: Ask "This Work Item doesn't exist yet. Would you like to create it? (yes/no)"
 - If yes: Proceed to step 3
 - If no: Exit skill

3. **Read current context:**
 - Read `.claude/active-context.txt`
 - Display: "Current context: Work Item {current_id}"

4. **Confirm switch:**
 - Ask: "Switch from {current_context} to {new_context}? (yes/no)"
 - If no: Exit skill
 - If yes: Proceed to step 5

5. **Write new context:**
 - Write to `.claude/active-context.txt` as `work-item:<id>`
 - Do not write the legacy `.claude/active-work-item.txt`
 - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord. Read the active branch from `journals/work-items/<id>/state.json`. Do not move `active` in this skill.

6. **Confirm to user:**
```
Switched to Work Item {id}
Context: work-item:{id}
Root path: work-items/{id}/
Journal: journals/work-items/{id}/progress.md
Workflow: {workflow_type}
Next action: {next_action}
```

7. **Display journal status:**
 - Read the Work Item journal
 - Display current phase, next action, and any open questions/blockers
 - Ask: "Would you like to continue from here? (say 'continue' to proceed)"

## Error Handling

- **Context doesn't exist:** Offer to create new context or cancel
- **Invalid ID format:** Re-prompt
- **No active context:** Treat as new context initialization, skip current context display

## Examples

**Example 1: Switch to existing work item**
```
User: "switch to work item WID-214111151"
Agent: "Current context: Work Item 2026-11-10-day-appointments. Switch to Work Item WID-214111151? (yes/no)"
User: "yes"
Agent: "Switched to Work Item WID-214111151. Current workflow: records-out. Next action: quote screenshot. Would you like to continue?"
```

**Example 2: Context doesn't exist**
```
User: "switch to work item 2026-11-12-day-appointments"
Agent: "Work Item 2026-11-12-day-appointments doesn't exist yet. Would you like to create it? (yes/no)"
User: "yes"
Agent: [Invokes workflow-selector to initialize the new Work Item]
```

## Notes

- Switching contexts does NOT lose work in the previous context
- All context state is preserved in their respective journals
- You can switch back and forth between contexts as needed
