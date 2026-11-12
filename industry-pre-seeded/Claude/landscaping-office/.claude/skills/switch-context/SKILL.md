---
name: switch-context
description: Use when the user says "switch to work item WID-XXXXXXXX" or names another job folder. Updates the active-context pointer.
trigger: User says "switch to work item WID-XXXXXXXX"
---

# Switch Context

Switches the active Work Item (crew day, ticket, week, pack).

## When to use

- "switch to work item WID-…"
- "switch to 2026-09-15-crew-a"
- "switch to {id}"

## Instructions

1. Parse the id. If it is a work-item id (WID-… or a shop folder name), `context_type=work-item`. If ambiguous, ask for the job id.

2. If `work-items/<id>/` does not exist, ask whether to create it. Yes → **workflow-selector**. No → stop.

3. Read `.claude/active-context.txt`. Show the current Work Item.

4. Confirm the switch. If no, stop.

5. Write `.claude/active-context.txt` as `work-item:<id>` . Update `Current work item:` in `journals/expert/progress.md` when the operator asked to switch. Do not move `active` in the branch map.

6. Confirm with journal path, workflow type, and next action from `journals/work-items/<id>/progress.md`. Ask if they want to **continue** from here.

## Examples

**Existing crew day**

```
User: switch to 2026-09-15-crew-a
Agent: Current: 2026-09-14-crew-a. Switch? (yes/no)
User: yes
Agent: Switched. Workflow: crew-day. Next action: pack. Say continue to proceed.
```

Do not describe software-build approval phases.

## Notes

Switching does not lose the previous job. Each Work Item keeps its own journal.
