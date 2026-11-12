---
name: plan-writer
description: "Use when the next action is run plan-writer, after the charter is approved."
trigger: Next action is "run plan-writer"
---

# Plan writer

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

1. Read the approved charter and the brief. If charter approval is not recorded, stop and return to the gate.
2. Ask whether the operator has a plan template.
3. Write `docs/plan/operating-plan.md`. The document title is **Product Plan**. Sections: Scope now, Scope later, Success metrics, Risks, Rollout narrative, Open decisions.
4. Update the diagrams so they match the plan: Journey, Prioritization, Stakeholder map, Decision flow.
5. Set next action to "wait for plan approval". The reply must be "I approve the plan" or "Skip plan approval".
6. Update the journal.
