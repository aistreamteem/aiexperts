# Role work-item method — Facilities / plant maintenance planner

**Role:** Facilities / plant maintenance planner  
**Industry:** US in-house plant or building-maintenance role (CMMS exports, crib sheets, procedure PDFs)  
**Research date:** 2026-11-08

This role produces **files** (dispatch lists, PM-due lists, parts-below-min packs, backlog-by-craft, downtime packs, LOTO-present indexes, contractor WO lists, warranty-due lists, after-hours emergency lists). It does **not** stamp OSHA, stamp PE drawings, pay vendors, diagnose as the technician beyond the words on their work order, sell a CMMS product, or store alarm/badge secrets.

## Industry funnel (research)

Typical US maintenance-planner work, from planner role descriptions and work-order planning flows (identify → plan → kit → ready-to-schedule → dispatch → execute → close):

1. **Work identification** — A request or PM due date becomes an individual work order. Gatekeeping / morning meeting turns requests into approved WOs. Standing “yearly boiler” tickets are not a control system; one WO per job.
2. **Plan the job** — Scope from the asset history and a field look: craft, steps, estimated hours from **their** file, safety permits (hot work, confined space, LOTO), tools, and materials. The planner progresses the WO to Ready to Schedule; they do not usually take daily emergency calls or assign named technicians (supervisor dispatch).
3. **Parts and kitting** — Reserve crib stock or requisition non-stock. Compare on-hand to stored min-qty. Do not invent a quantity or a min.
4. **Weekly schedule / daily dispatch** — Scheduler (often the planner) posts the week; craft supervisors adjust the day. This expert’s dispatch list is that board as a file from their WO CSV — not live radio dispatch.
5. **Execute and close** — Techs perform the work, write what they did, return leftovers. Quote the completion note as typed. Do not hide downtime. Do not invent a failure code.
6. **PM calendar** — Time- or meter-based PMs generate WOs from **their** interval and calendar file. Due/overdue lists join the asset list. Do not invent an interval or mark complete from a photo.
7. **Side paths this role also files** — Contractor / outside-service WOs; warranty-end vs pack date; emergency / after-hours vendor list; LOTO procedure PDF present/missing; backlog grouped by stored craft.

Sources used for orientation (not this shop’s policy): IDCON detailed work-order planning flow; Plant Services requester → gatekeeper → planner → scheduler → supervisor → craftsperson workflow; SMRP / SwainSmith maintenance-planner role (plan to Ready to Schedule; supervisor owns daily assignment; planner is not the OSHA inspector or reliability engineer).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the dispatch day, PM week, crib pull, downtime period, or pack. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two WOs or two weeks. |
| 2. Intake source files | Drop CMMS exports, crib CSVs, and procedure PDFs into `in/`. Read operations facts/rules. Do not invent intervals, mins, hours, criticality, or downtime codes. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (WO, PM calendar, crib, downtime, indexes) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or completeness pack to `out/`. Journal the artifacts. Completeness packs are not OSHA stamps, PE stamps, or dispatch assignments. | `out/*.md` plus supporting CSVs | Operator uses the pack (assign techs, order parts, chase a missing LOTO PDF). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* plant works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Daily / weekly in-house WO board | Dispatch List | `dispatch-list` (default) |
| PM calendar due / overdue | PM Due | `pm-due` |
| Crib on-hand vs stored min | Parts Below Min | `parts-below-min` |
| Approved open WOs by craft | Backlog By Craft | `backlog-by-craft` |
| Outage rows without hiding open downtime | Downtime Log | `downtime-log` |
| Night / weekend / holiday tickets + on-call names | Emergency After Hours List | `emergency-after-hours-list` |
| Machine-specific lockout PDF present/missing | LOTO Form Present | `loto-form-present` |
| Contractor / outside-service open WOs | Contractor WO List | `contractor-wo-list` |
| OEM / installer warranty-end vs pack date | Asset Warranty Due | `asset-warranty-due` |

Permit-to-work, hot-work, confined-space, and inspection **completeness** live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline. Do not add a field-scope / job-plan-writing workflow unless they ask; this seed files lists from exports, it does not write isolation steps or diagnose as the tech.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never OSHA/PE stamp, never pay, never diagnose as tech) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **planner/admin role**, not a craft supervisor, field-trade dispatcher, construction GC office, OSHA inspector, PE, or CMMS vendor.
- Existing nine work maps already match the file-producing slices of the industry funnel; no extra workflow was added.
- Default job is `dispatch-list` (the pack this role’s “done looks like” leads with).
- Step checks stay as Python file/CSV checks the operator can replace when they correct this plant.
