# Role work-item method — Veterinary front role (not the vet)

**Role:** Veterinary front role (not the vet)  
**Industry:** US small-animal / mixed-practice clinic reception (CSR), not the veterinarian  
**Research date:** 2026-11-08

This role produces **files** (day-book lists, missing-forms sheets, records-routing logs, reminder lists, price-file estimates, checkout line lists, boarding notes). It does **not** diagnose, treat, prescribe, interpret labs, triage as a veterinarian, take payment, or complete a DEA log.

## Industry loop (research)

Typical US veterinary receptionist / CSR work, from clinic job descriptions and daily-ops checklists (open the book → check-in paperwork → records routing → estimates → checkout → reminders / next-day confirmations):

1. **Open the day** — Print or export today’s appointment, drop-off, surgery, and boarding lists; flag emergency wording first; keep reason text as typed; doctor vs technician columns as labeled. Confirm the export date and site. Do not invent type lengths or move blocks to fill holes.
2. **Urgent interrupt** — Messages and book rows with emergency wording (not breathing, toxin, hit by car, collapse, seizure, unable to urinate) go to staff immediately. The role flags; it does not triage as a veterinarian or invent an ER number.
3. **New-client / check-in paperwork** — Completeness of registration PDFs, signatures, and required pages. Confirm client vs patient identity. Do not merge charts. Medical history answers are not read as a diagnosis.
4. **Records in / records out** — Log incoming PDFs (labs, films, transfers) without interpreting them. Log outgoing requests and whether an authorization file is present. Do not withhold records as a collections tactic. Do not stamp a health certificate or a VCPR.
5. **Reminders** — Produce a send list from **their** reminder / vaccine-due export. They send. Do not blast SMS/email from this folder. Copy stored communication preference.
6. **Estimates** — Fill **their** estimate template using only items and amounts on **their** price file. Do not add clinical lines. Unsigned estimates are not approval.
7. **Checkout list** — List invoice lines and tenders from **their** export. Do not take payment, store card numbers, or complete a controlled-drug log.
8. **Boarding / drop-off** — Copy pickup window, feeding, belongings, and meds **as written** on their form. Missing signatures stay missing. Do not convert units or add a drug.

Sources used for orientation (not this clinic’s policy): Vetstoria veterinary receptionist checklist; HubSpot Veterinary CSR Daily Checklist; Tilly veterinary front-role guide; MPAH-style receptionist job description; Elkins veterinary receptionist SOP; Provet CSR day-in-the-life; ForgeAgents boarding drop-off SOP templates.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the clinic date, patient/client pack, records request, estimate, or boarding drop-off. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two patients or two dates. |
| 2. Intake source files | Drop PIMS exports and PDFs into `in/`. Read shared facts/rules. Do not invent hours, prices, ER numbers, or type lengths. | Files in `in/` | Missing export/PDF → ask. Stale or undated book → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (day list, missing forms, routing log, estimate rows) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. Emergency wording stays at the top. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or checklist to `out/`. Journal the artifacts. Completeness packs are not clinical decisions or payment. | `out/*.md` plus supporting CSVs | Operator uses the pack (call the client, chase a missing form, hand the estimate to the vet). This expert does not decide care. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* clinic works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Open today’s book; emergency wording first | Day Appointments | `day-appointments` (default) |
| Interrupt: flag emergency words on book or message log | Emergency Flag | `emergency-flag` |
| New-client registration PDFs present/missing | New Client Forms | `new-client-forms` |
| Incoming labs/films/transfers as filenames | Records In | `records-in` |
| Outgoing records requests + authorization present | Records Out | `records-out` |
| Reminder / vaccine-due send list from their export | Reminder List | `reminder-list` |
| Estimate draft from their price file only | Estimate From Prices | `estimate-from-prices` |
| Invoice lines and tenders from their export | Checkout List | `checkout-list` |
| Boarding/drop-off notes as written on their form | Board Dropoff | `board-dropoff` |

Wait-list openings, no-shows, surgery-release completeness, certificate routing, and after-hours **routing** live in shared facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent clinic policy, never diagnose or take payment) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **veterinary CSR / front role** expert, not a veterinarian, technician, or hospital manager.
- Existing nine work maps already match the admin slices of the industry loop; no extra workflow was added.
- Default registered job is `day-appointments` (open the day book), matching typical clinic open-day practice.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this clinic.
- Copay / payment at the window is operator/clinic work; this expert only lists invoice lines and tenders from files they drop.
