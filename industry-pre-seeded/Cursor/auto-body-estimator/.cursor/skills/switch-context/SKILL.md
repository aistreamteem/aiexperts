---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
disable-model-invocation: false
---
## Switch Context

Switches the active Work Item (assignment / RO / claim pack).

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a work item or shop folder name

## Instructions

1. **Parse user request:**
 - Extract ID from user message
 - If it starts with "WID-" or looks like a claim/RO folder name → `context_type=work-item`
 - If ambiguous: ask for the Work Item id (WID-XXXXXXXX or `YYYY-MM-DD-ro-or-claim`)

2. **Check if context exists:**
 - Check `work-items/<id>/`
 - If missing: Ask "This Work Item doesn't exist yet. Create it? (yes/no)"
 - If yes: **workflow-selector** to initialize
 - If no: Exit

3. **Read current context** from `.cursor/active-context.txt` and tell the operator the current id.

4. **Confirm switch:** "Switch from {current} to {new}? (yes/no)"

5. **Write new context:**
 - `.cursor/active-context.txt` as `work-item:<id>`

 - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord. Read `journals/work-items/<id>/state.json`. Do not move `active` in this skill.

6. **Confirm:**
```
Switched to Work Item {id}
Root path: work-items/{id}/
Journal: journals/work-items/{id}/progress.md
Workflow: {workflow type from journal}
Next action: {next action}
```

7. Display current phase, next action, and open questions. Ask: "Say continue to walk the next ready step."

## Error Handling

- **Context doesn't exist:** Offer to create or cancel
- **Invalid ID:** Re-prompt
- **No active context:** Treat as new initialization

## Examples

**Example 1: Switch to existing work item**
```
User: "switch to work item 2026-09-15-ro-2104"
Agent: "Current context: Work Item WID-100000001. Switch to 2026-09-15-ro-2104? (yes/no)"
User: "yes"
Agent: "Switched. Current job: estimate-from-files. Next action: walk step pack. Say continue to proceed."
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
- Journals stay under `journals/work-items/<id>/`
