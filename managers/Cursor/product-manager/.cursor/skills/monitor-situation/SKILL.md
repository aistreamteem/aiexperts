---
name: monitor-situation
description: "Use when the next action is run monitor-situation. Records what is watched and the next check."
trigger: Next action is "run monitor-situation"
---

# Monitor

Write `docs/escalations/monitor.md`.

1. Name the signal, the current reading if known, and the next check time.
2. If the operator does not know the next check time, ask. Do not invent one.
3. Set next action to "run resolve-and-document" when the watch plan is written. Leave the escalation open in the document until that later check is done; say so in the file.
