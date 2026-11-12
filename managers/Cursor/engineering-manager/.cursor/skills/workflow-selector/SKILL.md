---
name: workflow-selector
description: "Use when the journal has no workflow type. Offers only the workflows enabled for this role."
trigger: Journal is missing Workflow type
---

# Workflow selector

1. Read `.cursor/workflows/workflow-registry.json`. Offer only those workflows. If `.cursor/role-skills.md` exists, do not offer a workflow the role definition disabled.
2. Ask which workflow applies:

   1. Team Delivery — Use when a team objective needs an outcome, owners, and a cadence, such as a delivery commitment, a staffing plan, or a delegation change.
   2. Team Escalation — Use when delivery slips, a people decision is urgent, or a production issue lands on the team.

   Include a third line only when the registry contains one.
3. Accept a number or a name. If the choice is not in the registry, ask again.
4. Ask for any external references (notes, tickets, decision threads).
5. For `team-escalation`, also ask: who is affected, and what decision is needed now?
6. Write `Workflow type` on `journals/work-items/<id>/progress.md` when it is missing. Do not replace `active`. Put the next action on the active node. Also record: `Workflow type`, context id, initial phase, and next action (`run intake` for `team-delivery`, `run assess-situation` for `team-escalation`).
7. Confirm the workflow name, the initial phase, and the next action.
