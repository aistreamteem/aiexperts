---
name: change-request
description: "Use when the operator wants to change an approved plan. Covers impact, approval, plan update, execution, and verification."
trigger: User asks for a change request, or next action is run change-request
---

# Change request

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

Use this for a change to scope, date, or a dependency.

1. Give the change an id. Create `docs/changes/<change-id>/impact.md` describing what changes, who is affected, and what stays the same.
2. Set next action to "wait for change approval". The phrase is "I approve the change" or "Skip change approval". Continue does not approve.
3. After approval, update `docs/plan/operating-plan.md` and the diagrams. Note the change id in the decision log.
4. Adjust `TODOS.md`. Execute only the actions the change requires, then run verify.
5. Update the journal: mode change-request, current change id.
