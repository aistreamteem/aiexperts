---
name: execute-action
description: "Use when the next action is execute-action (task K/N). Completes one management action from TODOS.md."
trigger: Next action is "execute-action (task K/N)"
---

# Execute action

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

Complete one item from `TODOS.md`. This is management work. An example output is a delivery-risk update for the payments squad.

Outputs this role produces:

- 1:1 agenda
- Hiring-loop note
- Delivery-risk update
- Delegation note
- Stakeholder status

1. Load facts and rules. Follow every rule.
2. Do not approve headcount or offers unless the operator explicitly approves that action.
3. Read the TODO. Write the output in the tracker, the decision log, or a note under `docs/notes/`. Mark that TODO done.
4. If you are blocked on a name, a file, or a decision, record the blocker and ask. Do not skip the item.
5. If a people-sensitive note was written, leave it on the work item. Do not copy it to expert-role memory unless the operator says to.
6. If this action changes a change to scope, date, or staffing, stop and start change-request instead of editing the plan in place.
7. Set next action to "execute-action (task K+1/N)", or "run verify" when no items remain.
8. Update the journal.
