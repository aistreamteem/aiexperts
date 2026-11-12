---
name: execute-action
description: "Use when the next action is execute-action (task K/N). Completes one management action from TODOS.md."
trigger: Next action is "execute-action (task K/N)"
---

# Execute action

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskQuestion for a fixed choice.

Complete one item from `TODOS.md`. This is management work. An example output is a steering pack that separates done, next, and blocked.

Outputs this role produces:

- Status report
- RAID update
- Dependency chase
- Steering pack
- Decision record

1. Load facts and rules. Follow every rule.
2. Do not accept a milestone yourself when a named approver is recorded.
3. Read the TODO. Write the output in the tracker, the decision log, or a note under `docs/notes/`. Mark that TODO done.
4. If you are blocked on a name, a file, or a decision, record the blocker and ask. Do not skip the item.
5. If a people-sensitive note was written, leave it on the work item. Do not copy it to expert-role memory unless the operator says to.
6. If this action changes a change to scope, date, or a dependency, stop and start change-request instead of editing the plan in place.
7. Set next action to "execute-action (task K+1/N)", or "run verify" when no items remain.
8. Update the journal.
