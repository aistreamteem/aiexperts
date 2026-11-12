---
name: diagram-generator
description: "Use when diagrams must be created or rebuilt from the charter and the plan."
trigger: Next action is run diagram-generator, or the charter or plan changed
---

# Diagram generator

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

Rebuild `work-items/<id>/docs/diagrams/` from the charter and the plan.

Diagrams for this role:

- Journey
- Prioritization
- Stakeholder map
- Decision flow

1. Read `docs/charter/charter.md` and, when it exists, `docs/plan/operating-plan.md`.
2. Write one `.mmd` file per diagram. Use Mermaid flowcharts. Stakeholder and RACI views may be a flowchart or a simple table expressed as a Mermaid block.
3. Write `docs/diagrams/index.html` that lists each diagram and loads Mermaid so the operator can open the file locally.
4. If the next action was "run diagram-generator" inside the planned pipeline, set the next action to "run action-breakdown". If you were only refreshing, leave the next action as it was and note the refresh in the journal.
