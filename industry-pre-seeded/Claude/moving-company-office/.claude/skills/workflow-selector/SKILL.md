---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled moving-office job."
---

# Workflow Selector

Presents the registered moving-office jobs and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` for `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json`

3. **Present menu from the registry only.** List each workflow as a numbered line: name, then description. Do not offer a job that is not in the registry. Do not offer developer, HLD/DD, or production-incident pipelines.

 Until the operator picks another job, the default is `estimate-from-rate-file`.

 Typical mapping (also in `docs/role/work-item-method.md`):
 - New quote / survey on file → Estimate From Rate File
 - Room sheet holes → Inventory Completeness
 - Articles of high value → High Value List Check
 - Cartons/crates to pull → Materials List
 - Who is on the truck tomorrow → Crew Day
 - Which unit is booked → Truck Calendar
 - Dest spread / window list → Delivery Window List
 - Scale slips → Weigh Ticket Pack
 - Loss/damage file → Claims Routing

4. **Accept user input:** a menu number, job id (`crew-day`), or display name (`Crew Day`).

5. **Validate** against the registry. If invalid, re-prompt.

6. **Ask:**
 - "What is the Work Item ID or job folder? (e.g., WID-21411151 or 2026-09-15-est-9021)"
 - "Any external references? (rate file, inventory export, calendar, scale tickets, claim photos)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item` (first step of the selected workflow file).

8. **Write active context:** `.claude/active-context.txt` as `work-item:<id>`. Do not write the legacy `.claude/active-work-item.txt`.

9. **Confirm:**

 ✅ Work Item initialized with <workflow-name>
 Initial phase: first step of that job (see the instruction file)
 Next action: follow `.claude/workflows/<id>.md` — one ready step via continue → journal-keeper

Do not tell the operator to run deleted process skills. The workflow file is the instruction.
