---
name: charter-writer
description: "Use when the next action is run charter-writer. Writes the charter and asks for approval."
trigger: Next action is "run charter-writer"
---

# Charter writer

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

1. Ask whether the operator has a template. If not, ask charter depth:
   - **Standard** — outcome and scope
   - **Part 1** — Standard, plus stakeholders and dependencies
   - **Extended** — Part 1, plus risks, communications, and constraints
2. Write `docs/charter/charter.md`. The document title is **Charter**. Sections: Outcome, Scope, Stakeholders, Success, Constraints.
3. Apply expert-role rules. Do not invent a decision the operator has not made.
4. Draft Mermaid diagrams for: Stakeholder map, Operating cadence, RACI, Decision flow. Write them under `docs/diagrams/` and refresh `index.html`.
5. Set next action to "wait for charter approval". Tell the operator the path and that the reply must be "I approve the charter" or "Skip charter approval".
6. Update the journal, including charter depth.
