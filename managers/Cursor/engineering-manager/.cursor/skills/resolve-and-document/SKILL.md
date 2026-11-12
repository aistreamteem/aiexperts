---
name: resolve-and-document
description: "Use when the next action is run resolve-and-document. Writes the management record of the escalation."
trigger: Next action is "run resolve-and-document"
---

# Resolve and document

Write `docs/escalations/resolution.md`.

Include:

- What was decided
- Who was told, and what they were told
- What remains open, and the next check
- Whether a lasting change should become a change request on the planned pipeline

Set next action to "done". Ask whether to promote any non-sensitive facts or rules.
