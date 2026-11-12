---
name: workflow-selector
description: "Use when continue finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts for a trade shop job."
trigger: Called by continue skill when journal missing workflow type
---

# Workflow Selector

Presents this role’s jobs from the registry and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. Read `.claude/active-context.txt` for `context_type` and `context_id`. Role packs are `work-item`.
2. Read `.claude/workflows/workflow-registry.json`. Offer **only** those jobs. Do not offer software-build or outage-role jobs.
3. Present the menu (name + description). Until the operator changes the registry, the jobs are:

   1. Callback Triage — List returns to recent jobs; flag warranty versus billable per their marks.
   2. Closeout Photos — Required photos present or missing for jobs they mark complete.
   3. Daily Board — From their schedule file, today's jobs, assigned tech, missing packing lists.
   4. Emergency Queue — Jobs they marked emergency or that match their life-safety words.
   5. Parts Ready — Build or check a packing list for one job id they name.
   6. Permit File — Permit number, AHJ, dates for jobs they marked as needing a permit.
   7. Quote To Job — One sold estimate: parts from the PDF, schedule and permit questions.
   8. Truck Load — Jobs on one tech or crew, combined packing list, missing special orders.
   9. Warranty Parts — Serial, install date, failed part from their file, order question.
   10. Week Schedule — Week view: crew PTO, overbook, sold installs without parts.

4. Accept a number or a name (`daily-board`, “Daily Board”). Validate against the registry.
5. Ask: “What is the Work Item ID? (WID-… or a job/pack id)” and “Any source files, job id, or export path?”
6. Write `Workflow type` on `journals/work-items/<id>/progress.md` when missing. Set Context ID. Put Next action on `nodes/work-item.md` only when `active` is still just `work-item` — first phase is **intake**.
7. Write `.claude/active-context.txt` as `work-item:<id>` (do not write the legacy `.claude/active-work-item.txt`).
8. Confirm:

   Work Item initialized with \<workflow-name\>
   Initial phase: intake
   Next action: confirm job id / site and source files in in/, then first extract step

Do not tell the operator to run deleted process skills. Method: `docs/role/work-item-method.md`.
