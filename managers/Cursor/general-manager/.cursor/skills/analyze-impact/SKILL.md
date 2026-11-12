---
name: analyze-impact
description: "Use when the next action is run analyze-impact. Writes options and waits for response approval."
trigger: Next action is "run analyze-impact"
---

# Analyze impact

Write `docs/escalations/impact.md`.

1. State the impact in the terms of this role: The stuck decision, the people affected, the options, and the next communication.
2. List options and who decides. Include "do nothing yet" when that is honest.
3. Set next action to "wait for response approval". Tell the operator to reply "I approve the response" or "Skip response approval", and to name which option.
4. Do not carry out the response in this step.
