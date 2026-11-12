---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled landscaping-office job."
disable-model-invocation: false
---

# Workflow Selector

Presents the registered role jobs and records the selection in the Work Item journal.

## When to use

- Called by **continue** when the journal is missing **Workflow type**
- On new Work Item initialization

## Instructions

1. Read `.claude/active-context.txt` for `context_type` and `context_id`.

2. Read `.claude/workflows/workflow-registry.json`.

3. Present **only** registry jobs as a numbered list (name + description). Current jobs:
   - Callback List
   - Crew Day
   - Enhancement Ticket
   - Estimate From Price
   - Material Pull
   - Photo Pack
   - Route Pack
   - Seasonal Calendar
   - Weather Postpone List

   Default until they pick another: `callback-list`. Typical daily dispatch is **Crew Day**.

4. Accept a number, a registry id (`crew-day`), or a display name (`Crew Day`).

5. Validate against the registry. If invalid, re-prompt.

6. Ask:
   - "What is the Work Item ID or job folder? (e.g. `2026-09-15-crew-a` or WID-…)"
   - "Any files to use? (route CSV, roster, price file, tickets, photos)"

7. Record on `journals/work-items/<id>/progress.md`:
   - `Workflow type: <registry-id>`
   - Context id
   - Next action = first step of that workflow file (or `role-job` if the file uses that initial phase)

   Put Next action on `nodes/work-item.md` only when `active` is still just `work-item`.

8. Write `.claude/active-context.txt` as `work-item:<id>` (do not write the legacy `.claude/active-work-item.txt` pointer).

9. Confirm:

```
Work Item initialized with <workflow-name>
Initial phase: first step in .claude/workflows/<id>.md
Next action: continue → one ready step → journal-keeper
```

Do not offer software-build or incident-response workflows. Only registry jobs.
