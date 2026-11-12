---
name: respond
description: "Use when the next action is run respond, after response approval."
trigger: Next action is "run respond"
---

# Respond

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskQuestion for a fixed choice.

1. Confirm the journal records response approval and which option was chosen. If not, return to the gate.
2. Write `docs/escalations/response.md`: the decision, who was told, the message, and the immediate actions.
3. Do not accept a milestone yourself when a named approver is recorded.
4. Carry out only communication and records this expert can write. Do not take over work that belongs to someone else; name that owner in the response.
5. Set next action to "run monitor-situation".
