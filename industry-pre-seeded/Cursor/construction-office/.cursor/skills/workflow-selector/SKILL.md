---
name: workflow-selector
description: "Use when continue finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts for a construction office job."
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

   1. Change Register — Open potential changes and signed change orders from their register.
   2. Closeout Binder — Presence and absence of closeout files they named.
   3. Daily Log — Fill or extract today's log for one job number.
   4. Deliveries — List expected and received deliveries for one job.
   5. Look Ahead — From their schedule export, list the next window they named.
   6. Punch List — Room, item, owner, and done from their punch sheet for one job.
   7. RFI Status — From their RFI export, list open, overdue versus their due column, and returned.
   8. Sub COI — Roster plus certificate dates they already track.
   9. Submittal Aging — Status and aging from their submittal export.
   10. Weekly Minutes — Agenda plus open actions from last minutes they filed.

4. Accept a number or a name (`daily-log`, “Daily Log”). Validate against the registry.
5. Ask: “What is the Work Item ID? (WID-… or a job/pack id)” and “Any source files, job number, or export path?”
6. Write `Workflow type` on `journals/work-items/<id>/progress.md` when missing. Set Context ID. Put Next action on `nodes/work-item.md` only when `active` is still just `work-item` — first phase is **intake**.
7. Write `.cursor/active-context.txt` as `work-item:<id>` (do not write the legacy `.cursor/active-work-item.txt`).
8. Confirm:

   Work Item initialized with \<workflow-name\>
   Initial phase: intake
   Next action: confirm job number and source files in in/, then first extract step

Do not tell the operator to run deleted process skills. Method: `docs/role/work-item-method.md`.
