---
name: action-breakdown
description: "Use when the next action is run action-breakdown. Writes TODOS.md from the approved plan."
trigger: Next action is "run action-breakdown"
---

# Action breakdown

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

1. Read the approved plan. If plan approval is not recorded, stop.
2. Write `TODOS.md` with these sections, in this order:
   - Setup
   - Dependencies and asks
   - Kickoff — include Integrated tracker, RAID log, Steering cadence, Stakeholder list
   - Execution — include concrete actions of these kinds: Status report, RAID update, Dependency chase, Steering pack, Decision record
   - Verification — Milestone acceptance by the named approver, Steering sign-off, Open-risk review
   - Communication and close-out
3. Setup and kickoff come before execution.
4. Every execution line has an owner slot and a done check.
5. Set next action to "run kickoff".
6. Update the journal with the task count.
