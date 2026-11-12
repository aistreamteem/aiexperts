---
name: switch-context
description: "Use when the operator says switch to work item WID-XXXXXXXX. Points later steps at that work item."
trigger: User says "switch to work item WID-..."
---

# Switch context

1. Parse the WID. If the folder does not exist, copy `work-items/_TEMPLATE/`, then run workflow-selector.
2. Confirm the switch with the operator.
3. Write `.claude/active-context.txt` as `work-item:<WID>` only. Do not write `.claude/active-work-item.txt`.
Change `Current work item:` in `journals/expert/progress.md` to that id. Read the active branch from `journals/work-items/<id>/state.json`. Do not move `active`.
4. Show workflow type, current phase, next action, and any open question or gate.
5. Offer "continue" as the way to take the next step. Do not take it in this turn unless the operator already asked you to continue.
