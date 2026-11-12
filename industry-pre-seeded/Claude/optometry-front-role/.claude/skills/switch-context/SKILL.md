---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---
## Switch Context

Switches the active Work Item context for this optometry front role.

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a work item or dated pack (for example `2026-11-10-day-list`)

## Instructions

1. **Parse user request:**
 - Extract ID from user message
 - If it starts with "WID-" or names an existing `work-items/<id>/` folder → `context_type=work-item`
 - If ambiguous: ask for a Work Item ID or pack folder name

2. **Check if context exists:**
 - Check `work-items/<id>/`
 - If missing: Ask "This Work Item doesn't exist yet. Create it? (yes/no)"
 - If yes: Proceed (workflow-selector will pick the optometry-role job)
 - If no: Exit

3. **Read current context:**
 - Read `.claude/active-context.txt`
 - Display: "Current context: Work Item {current_id}"

4. **Confirm switch:**
 - Ask: "Switch from {current} to {new}? (yes/no)"

5. **Write new context:**
 - Write `.claude/active-context.txt` as `work-item:<id>`
 - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord. Do not move `active` in this skill.

6. **Confirm:**

 Switched to Work Item {id}
 Root path: work-items/{id}/
 Journal: journals/work-items/{id}/progress.md
 Workflow: {workflow_type}
 Next action: {next_action}

7. **Display journal status** (current phase, next action, blockers). Ask: "Say continue to pick up this pack."

## Examples

**Switch to an existing day list**
```
User: "switch to work item 2026-11-10-day-list"
Agent: "Current context: Work Item WID-100000001. Switch to 2026-11-10-day-list? (yes/no)"
User: "yes"
Agent: "Switched. Current phase: staff-review. Next action: wait for operator review of out/day-list.md."
```

**Create if missing**
```
User: "switch to work item WID-999999999"
Agent: "Work Item WID-999999999 doesn't exist yet. Create it? (yes/no)"
User: "yes"
Agent: [workflow-selector]
```

## Notes

- Switching does not lose work in the previous Work Item
- This role uses registered optometry jobs (day list, eligibility screenshot, frame/lens completeness, and the other maps in the registry)
