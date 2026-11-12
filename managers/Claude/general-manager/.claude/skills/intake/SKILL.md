---
name: intake
description: "Use when the next action is run intake. Writes the brief and raises blocking questions."
trigger: Next action is "run intake"
---

# Intake

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskUserQuestion for a fixed choice.

Load work-item and expert-role facts and rules before writing.

1. Read the journal and any brief the operator pointed at.
2. Ask these questions if the answers are not already in Resolved Q&A. They are blocking:

- What outcome is needed?
- Who is affected and who decides?
- What does success look like?
- What cadence already exists?

3. The word continue is not an answer. Record each answer in the same turn.
4. Write `work-items/<id>/docs/charter/brief.md` with the answers, the unknowns, and the risks.
5. Set next action to "run charter-writer".
6. Update the journal.
