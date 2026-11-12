---
name: close-out
description: "Use when the next action is run close-out. Writes the status narrative, decision log pointer, and handoff."
trigger: Next action is "run close-out"
---

# Close-out

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

A status narrative that leads with risk, the decision log, and a handoff into the next cadence.

1. Confirm verification exists.
2. Write `docs/close-out/close-out.md` with the status narrative, a link to `docs/decisions/decision-log.md`, and the handoff note (who owns the work next, and what cadence continues).
3. Journal fields to set: status narrative path, decision-log path, handoff note. Do not invent a branch or a review request.
4. Set next action to "done".
5. Ask whether to promote facts and rules.
