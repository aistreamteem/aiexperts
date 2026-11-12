---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX", or otherwise asks to change the active context. Updates the active-context pointer so subsequent journal/facts/rules operations target the right Work Item.
trigger: User says "switch to work item WID-XXXXXXXX"
---

## Switch Context

Switches the active Work Item (move, estimate, day list, or claim pack).

## When to use

- User says "switch to work item WID-XXXXXXXX"
- User says "switch to {id}" where id is a work item or shop folder name

## Instructions

1. **Parse user request:** Extract ID. If it starts with `WID-` or looks like a dated job folder, `context_type=work-item`. If ambiguous, ask for the move / estimate / pack id.

2. **Check if context exists:** If `work-items/<id>/` is missing, ask whether to create it. Yes → **workflow-selector**. No → stop.

3. **Read current context** from `.claude/active-context.txt` and show it.

4. **Confirm switch.** If no, stop.

5. **Write new context:**
 - `.claude/active-context.txt` as `work-item:<id>`
 - Do not write the legacy `.claude/active-work-item.txt`
 - Change `Current work item:` in `journals/expert/progress.md` only when the operator is switching of their own accord. Read `journals/work-items/<id>/state.json`. Do not move `active` in this skill.

6. **Confirm:**

 Switched to Work Item {id}
 Root path: work-items/{id}/
 Journal: journals/work-items/{id}/progress.md
 Workflow: {workflow type from journal}
 Next action: {from journal}

7. Show current phase, next action, and open questions. Ask: "Would you like to continue from here? (say 'continue' to proceed)"

## Examples

**Existing job**

```
User: "switch to work item 2026-09-15-est-9021"
Agent: Current context: Work Item WID-100000001. Switch to 2026-09-15-est-9021?
User: yes
Agent: Switched. Workflow: estimate-from-rate-file. Next action: pack the estimate draft. Continue?
```

**Missing job**

```
User: "switch to Saturday-loads"
Agent: That Work Item doesn't exist yet. Create it?
User: yes
Agent: [workflow-selector]
```
