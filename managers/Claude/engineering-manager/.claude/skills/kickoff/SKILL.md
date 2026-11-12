---
name: kickoff
description: "Use when the next action is run kickoff. Creates the cadence, tracker, decision log, and stakeholder list."
trigger: Next action is "run kickoff"
---

# Kickoff

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

Create the working set from the approved plan before any execute action.

Create these:

- 1:1 cadence
- Delivery tracker
- Decision log
- Stakeholder list

Suggested paths under the work item:

- `docs/decisions/decision-log.md`
- `docs/trackers/tracker.md` for the tracker named in the kickoff list
- `docs/trackers/cadence.md`
- `docs/trackers/stakeholders.md`

1. If these already exist and match the plan, do not duplicate them. Set the next action to "execute-action (task 1/N)".
2. Otherwise create the missing files from the plan. A decision log starts with columns: date, decision, decider, consequence.
3. If a name or a forum is missing, ask. Do not invent stakeholders.
4. Set next action to "execute-action (task 1/N)" using the count in TODOS.md.
5. Update the journal.
