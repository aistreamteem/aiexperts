---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---
## Switch Context

Switches the active Work Item (chart pack) context.

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a work item or dated pack slug

## Instructions

1. **Parse user request:**
   - Extract ID from user message
   - Work Item ids are `WID-…` or a pack slug (`2026-11-08-sales-by-week`). `context_type=work-item`
   - If ambiguous: ask for the Work Item ID

2. **Check if context exists:**
   - Check if `work-items/<id>/` exists
   - If folder doesn't exist: Ask "This Work Item doesn't exist yet. Would you like to create it? (yes/no)"
   - If yes: Proceed to step 3 (or **workflow-selector** if no workflow is named)
   - If no: Exit skill

3. **Read current context:**
   - Read `.claude/active-context.txt`
   - Display: "Current context: Work Item {current_id}"

4. **Confirm switch:**
   - Ask: "Switch from {current_context} to {new_context}? (yes/no)"
   - If no: Exit skill

5. **Write new context:**
   - Write `.claude/active-context.txt` as `work-item:<id>`
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
   - Display current phase (question / intake / profile / prepare / chart / pack / review), next action, and open questions
   - Ask: "Would you like to continue from here? (say 'continue' to proceed)"

## Error Handling

- **Context doesn't exist:** Offer to create or cancel
- **Invalid ID:** Re-prompt
- **No active context:** Treat as new initialization, skip current context display

## Examples

**Example 1: Switch to existing pack**
```
User: "switch to work item WID-214111151"
Agent: "Current context: Work Item WID-100000001. Switch to Work Item WID-214111151? (yes/no)"
User: "yes"
Agent: "Switched to Work Item WID-214111151. Current phase: pack. Next action: write out/describe-csv.md. Would you like to continue?"
```

**Example 2: Context doesn't exist**
```
User: "switch to work item 2026-11-08-sales-by-week"
Agent: "Work Item 2026-11-08-sales-by-week doesn't exist yet. Would you like to create it? (yes/no)"
User: "yes"
Agent: [Invokes workflow-selector to initialize the new pack]
```

## Notes

- Switching does not lose work in the previous context
- Journals stay isolated per Work Item
- Do not use HLD-approval examples; this role’s gates are named question/columns, honest scales, and operator review of the pack
