---
name: verify
description: "Use when the next action is run verify. Records acceptance, sign-off, and the risk review."
trigger: Next action is "run verify"
---

# Verify

Write `work-items/<id>/docs/verification/verification.md`.

Checks for this role:

- Success criteria checked
- Stakeholder sign-off
- Risk review

1. Compare the checks to the charter and the plan. Cite the success measure.
2. Record stakeholder sign-off as yes, no, or waiting. If waiting, say who.
3. List risks still open.
4. If a check fails, say so and set the next action back to the execute task that must be repeated. Do not close out a failed check unless the operator records an exception.
5. When the checks pass or an exception is recorded, set next action to "run close-out".
