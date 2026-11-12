# Role work-item method — Construction office coordinator

This role produces **daily and weekly paper packs** for a small US general contractor or remodeler office: logs, registers, aging lists, and packs that **quote the operator’s files**. It does not design, stamp, price, pay, or give legal or OSHA advice.

Industry sources for this method (typical coordinator / document-control practice, not this shop until they confirm):

- Construction office management: RFI log, submittal register, change-order log, punch tracking, closeout binder (O&M, warranties, as-builts, lien waivers).
- Project coordinator duties: weekly/OAC minutes and action follow-up; drawing-set currency; subcontractor COI / insurance collection; look-ahead from the schedule export; pay-app backup as files they already keep.
- Field-to-office daily record: weather, crews, work performed, deliveries, visitors, safety notes — locked to what the superintendent wrote.

Starter notes in shared memory are **typical US practice until they confirm this shop**.

## Shared phases (every Work Item)

Use these phases on every registered job. The YAML in `.claude/workflows/<id>.md` is the step list for that job; paths are inside `work-items/<id>/`.

| Phase | What happens | Typical artifacts | Human gate |
| --- | --- | --- | --- |
| **1. Intake** | Confirm job number / pack id. Collect the export, sheet, PDF, or photo the operator dropped into `in/`. Do not start if the needed file is missing. | `in/` source files; journal job number | Operator names the job and points at the file |
| **2. Extract** | Copy columns and status words from their file into `work/`. Their headers win. Blank stays blank. | `work/*.csv` or notes | Ask if a required column is missing |
| **3. Exception pass** | Age, match, or flag only when that job’s map has the step (overdue RFIs, missing tickets, expired COIs, closeout presence). Date compare against printed dates. | `work/*-aged.csv`, flags, ticket notes | Ask on expired COI, blank extra-work, unreadable stamp |
| **4. Pack** | Write `out/` so a later check can see the list. Quote source filenames, job number, and their status words. | `out/*.md` pack | Pack must name the source file |
| **5. Operator review** | Stop for missing files, incidents, verbal extras, or anything the rules send to them. Do not invent a pass. | Journal open questions; `evidence/` check logs | Explicit answer or “pack looks right” |
| **6. Close** | Mark the Work Item done when steps and checks pass or exceptions are recorded. Offer promote-facts-rules for durable shop knowledge. | `STATUS.md`; optional promotions | Optional promotion choices |

**Continue** means one ready step in this sequence (or the whole named job if they asked). It is not approval of a gate.

## Which registered workflows cover which work

| Recurring office job | Workflow id | Phases it covers |
| --- | --- | --- |
| Daily construction record (weather, manpower, notes) | `daily-log` | Intake → extract today’s log → pack |
| Receiving / tickets | `deliveries` | Intake → extract list → match tickets → pack |
| Short-interval plan from their schedule | `look-ahead` | Intake → extract window → pack (plan vs actual labeled) |
| Weekly / OAC coordination | `weekly-minutes` | Intake → agenda → open actions → pack |
| RFI document control | `rfi-status` | Intake → pull log → age open/overdue/returned → pack |
| Submittal register | `submittal-aging` | Intake → list → age → pack (no approval) |
| Change paper (PCO / COR / CO status) | `change-register` | Intake → list from register → pack (no pricing) |
| Subcontractor insurance dates | `sub-coi` | Intake → roster → flag missing/past dates → pack |
| Deficiency tracking near completion | `punch-list` | Intake → items from their sheet → pack |
| Closeout presence/absence | `closeout-binder` | Intake → checklist → photo note → pack |

Default registry workflow when none is named: `daily-log` (the usual daily construction record). Use another registered job when they name it.

## Human gates (do not skip)

- **Source file missing** — wait. Do not rebuild a day from photos or last week.
- **Incident / injury / serious near miss** — flag the line they wrote and stop; this is not a safety investigation.
- **Verbal extra / blank extra-work rule** — flag; ask their extra-work rule. Do not say it is billable.
- **COI missing or past** — ask. Do not type “in force.”
- **Unreadable submittal stamp / mixed drawing revisions** — quote what is on the file and ask which governs.
- **Finished pack** — operator confirms the list quotes their files. Saying “continue” is not that confirmation.

## Canonical expert skills (process)

Starting work → `workflow-selector` + Work Item under `work-items/<id>/` + `continue`.  
Stepping a job → the workflow file above + `continue` / `journal-keeper`.  
Clarification → `operator-qa`.  
Durable notes → `remember` / `integrate-docs`.  
Scope → `MyRole.txt` + `facts/rules-shared.md`.

## What this method is not

Not a software-build method. Not an outage-response role. Not SAM.gov / GoNoGo. Not paying subs, stamping drawings, or answering RFIs as the architect.
