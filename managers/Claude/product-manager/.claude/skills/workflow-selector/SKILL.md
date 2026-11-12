---
name: workflow-selector
description: "Use when the journal has no workflow type. Offers only the workflows enabled for this role."
trigger: Journal is missing Workflow type
---

# Workflow selector

1. Read `.claude/workflows/workflow-registry.json`. Offer only those workflows. If `.claude/role-skills.md` exists, do not offer a workflow the role definition disabled.
2. Ask which workflow applies:

   1. Product Initiative — Use when a user problem needs an outcome, a now-versus-later cut, and stakeholder alignment.
   2. Product Escalation — Use for a launch problem, a priority conflict, or a user issue that changes the outcome.

   Include a third line only when the registry contains one.
3. Accept a number or a name. If the choice is not in the registry, ask again.
4. Ask for any external references (notes, tickets, decision threads).
5. For `product-escalation`, also ask: who is affected, and what decision is needed now?
6. Write `Workflow type` on `journals/work-items/<id>/progress.md` when it is missing. Do not replace `active`. Put the next action on the active node. Also record: `Workflow type`, context id, initial phase, and next action (`run intake` for `product-initiative`, `run assess-situation` for `product-escalation`).
7. Confirm the workflow name, the initial phase, and the next action.
