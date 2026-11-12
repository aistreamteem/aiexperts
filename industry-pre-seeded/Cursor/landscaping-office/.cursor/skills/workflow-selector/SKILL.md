---
name: workflow-selector
description: "Use when continue finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts for a landscaping-office job."
trigger: Called by continue skill when journal missing workflow type
---

# Workflow Selector

Presents this role’s jobs from the registry and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. Read `.cursor/active-context.txt` for `context_type` and `context_id`. Role packs are `work-item`.
2. Read `.cursor/workflows/workflow-registry.json`. Offer **only** those jobs. Do not offer software-build or outage-role jobs.
3. Present the menu (name + description). Until the operator changes the registry, the jobs are:

   1. Callback List — List open callbacks from tickets they coded as return or complaint.
   2. Crew Day — Build a day list from their roster and tickets: crew, property, service, window, dog and skip flags.
   3. Enhancement Ticket — Assemble one-time work from the enhancement ticket, price file, and sold proposal if present.
   4. Estimate From Price — Draft estimate lines from their price file and the proposal or takeoff they stored.
   5. Material Pull — Build a pull list from sold tickets and their material sheet.
   6. Photo Pack — Index photos they stored to ticket and property.
   7. Route Pack — Pull the route CSV and match each stop to a ticket.
   8. Seasonal Calendar — List upcoming seasonal extras from their calendar and match properties that already have tickets.
   9. Weather Postpone List — After they write a weather call, list postponed route stops and whether their note says next cycle or make-up.

   Default until they pick another: `callback-list`. Typical daily dispatch is **Crew Day**.

4. Accept a number or a name (`crew-day`, “Crew Day”). Validate against the registry.
5. Ask: “What is the Work Item ID? (WID-… or a crew day / property + date / ticket / week)” and “Any source files (route CSV, roster, price file, tickets, photos)?”
6. Write `Workflow type` on `journals/work-items/<id>/progress.md` when missing. Set Context ID. Put Next action on `nodes/work-item.md` only when `active` is still just `work-item` — first phase is the first step in that workflow file.
7. Write `.cursor/active-context.txt` as `work-item:<id>` (do not write the legacy `.cursor/active-work-item.txt`).
8. Confirm:

   Work Item initialized with \<workflow-name\>
   Initial phase: first step in `.cursor/workflows/<id>.md`
   Next action: confirm source files in in/, then first extract step

Do not tell the operator to run deleted process skills. Method: `docs/role/work-item-method.md`.
