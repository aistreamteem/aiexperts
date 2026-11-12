# Role work-item method — Job coordinator in a trade shop

**Role:** Job coordinator in a trade shop  
**Industry:** US small/mid HVAC, plumbing, electrical (and similar) service or install shop  
**Research date:** 2026-11-08

This role produces **files** (daily board, packing lists, permit-number packs, closeout photo checklists, callback flags). It does **not** hold a trade license, pass an inspection, specify a design or load calc, diagnose over the phone, or pay the supply house.

## Industry funnel (research)

Typical US service-dispatcher / job-coordinator work, from contractor playbooks and dispatcher job descriptions (request → board → truck ready → live dispatch → closeout):

1. **Capture the request** — Record site, caller, job type, symptoms in their words, access, sold vs estimate, and any commitment already made. A quote is not a sold install until their file says sold.
2. **Classify priority** — Separate life-safety emergencies (gas smell, CO, sparking, freeze no-heat, active flood) from urgent and routine work. Emergencies are not membership color.
3. **Confirm readiness** — Before a truck rolls: packing list present, parts from sold PDF or them (not guessed SKUs), permit number on file if they marked the job as needing one, 811 locates if it digs, address/unit confirmed.
4. **Match tech and window** — Assign by skill/license first, geography second. Use the arrival window they sold. Do not invent a clock time.
5. **Control the live board** — Reshuffle for overruns and after-hours calls without silently dropping a promised slot. Weather holds and two-person SOP flags stay visible.
6. **Close or hand off** — Required photos present or listed missing; incomplete stays open with a reason code; callbacks flagged so they are not billed as new revenue unless they marked billable; warranty parts packs quote serial and install date from file only.

Sources used for orientation (not this shop’s policy): HVAC Dispatch Association seven-step workflow and daily checklist; SMBwiki dispatch process (board → skill match → work order → live reshuffle); ServiceTitan contractor playbook permit tracking; HelpingCo / Trust 1–style dispatcher duties (daily board, parts, closeout notes/photos/invoices, next-day confirmations).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the ticket, day-board, crew load, permit pack, or callback list. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two tickets. |
| 2. Intake source files | Drop schedule exports, sold PDFs, packing lists, permit scans, photo folders into `in/`. Read operations facts/rules. Do not invent SKUs, ETAs, permit numbers, or inspection results. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (jobs, gaps, parts, permit rows) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished board, packing list, permit pack, or photo checklist to `out/`. Journal the artifacts. Completeness packs are not inspection passes or sold-price rewrites. | `out/*.md` plus supporting CSVs | Operator uses the pack (call the customer, hold the truck, chase a permit). This expert does not license, inspect, or pay. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Today’s jobs, assigned tech, missing packing lists (typical start of day) | Daily Board | `daily-board` |
| Week view: PTO, overbook, sold installs without parts | Week Schedule | `week-schedule` |
| Life-safety / emergency-marked jobs | Emergency Queue | `emergency-queue` |
| One sold estimate → parts, schedule question, permit question | Quote To Job | `quote-to-job` |
| Packing list for one named job id | Parts Ready | `parts-ready` |
| Combined packing list for one tech/crew | Truck Load | `truck-load` |
| Permit number, AHJ, dates from their file | Permit File | `permit-file` |
| Required closeout photos present or missing | Closeout Photos | `closeout-photos` |
| Returns flagged warranty vs billable | Callback Triage | `callback-triage` (registry default) |
| Serial, install date, failed part, order question | Warranty Parts | `warranty-parts` |

811 locates, weather holds, two-person SOP, and “incomplete stays open” live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never claim a license or inspection pass) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **job-coordinator / dispatcher role**, not a licensed tech, engineer, AHJ, or CRM-product seller.
- Existing ten work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Registry default stays `callback-triage` as shipped. Typical start-of-day job is still **Daily Board**.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
