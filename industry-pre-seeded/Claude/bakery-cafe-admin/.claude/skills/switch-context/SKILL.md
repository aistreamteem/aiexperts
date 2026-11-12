---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX" or a pack name. Updates the active-context pointer so journals and facts target the right Work Item.
---

## Switch Context

Switches the active bakery-cafe Work Item.

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to 2026-11-08-bake-list" or another pack name

## Instructions

1. **Parse user request:**
 - Extract ID
 - If it starts with `WID-` or looks like a pack name, `context_type=work-item`
 - If ambiguous: ask for a Work Item id or bake-date / pack name

2. **Check if context exists:**
 - Check `work-items/<id>/`
 - If missing: "This Work Item doesn't exist yet. Create it? (yes/no)"
 - If yes: **workflow-selector** to initialize
 - If no: Exit

3. **Read current context** from `.claude/active-context.txt` and show it.

4. **Confirm switch** unless they already named a clear target and there is no conflicting active pack.

5. **Write new context:**
 - `.claude/active-context.txt` as `work-item:<id>` (do not write the legacy `.claude/active-work-item.txt`)
 - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord
 - Do not move `active` in this skill

6. **Confirm:**

 Switched to Work Item {id}
 Root path: work-items/{id}/
 Journal: journals/work-items/{id}/progress.md
 Workflow: {workflow_type}
 Next action: {next_action}

7. Display current phase, next action, and open questions. Ask if they want to **continue**.

## Error Handling

- Missing folder: offer to create
- Invalid id: re-prompt
- No active context: treat as new initialization

## Examples

**Switch to an existing Tuesday bake list**

```
User: "switch to work item 2026-11-08-bake-list"
Agent: "Current: 2026-11-07-wholesale. Switch to 2026-11-08-bake-list? (yes/no)"
```

**Doesn't exist**

```
User: "switch to work item 2026-11-09-cakes"
Agent: "That Work Item doesn't exist yet. Create it? (yes/no)"
User: "yes"
Agent: [workflow-selector]
```

## Notes

- Switching does not lose the previous pack
- Each bake date / wholesale day / cake board keeps its own journal
