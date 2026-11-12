---
name: assess-situation
description: "Use when the next action is run assess-situation. Opens an escalation assessment."
trigger: Next action is "run assess-situation"
---

# Assess situation

Write `docs/escalations/assessment.md`.

This escalation must cover: Impact on the outcome, the options, who decides, and what users or stakeholders are told.

1. Ask what is known and what is still unknown. Unknowns that block the assessment are blocking questions.
2. Do not turn an execute action into a build task.
3. Set next action to "run analyze-impact".
