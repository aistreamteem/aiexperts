# Role work-item method — Dog daycare / boarding office

**Role:** Dog daycare / boarding office  
**Industry:** US dog daycare and boarding kennel front office (not a veterinary hospital, not the playgroup handler on the floor)  
**Research date:** 2026-11-08

This role produces **files** (boarding/occupancy lists, missing-vaccine-file lists, feeding sheets as written, meds-to-give lists as written, pickup-authorization lists, waiver-missing lists, waitlist order, incident-routing completeness). It does **not** diagnose, decide a vaccine is due as a clinician, prescribe or change a dose, interpret a titer, give a boarding legal opinion, or release a dog from the lobby.

## Industry funnel (research)

Typical US daycare/boarding office work, from kennel SOP and check-in/check-out guides (night-before roster → intake role → stay tasks → authorized pickup):

1. **Pre-arrival / overnight prep** — Pull tomorrow’s reservation or boarding roster; confirm every expected dog; flag missing vaccine pages, unsigned waivers, and blank emergency contacts; note feeding and meds-to-give as already written; compare expected headcount to the capacity file and handler schedule. Offices treat vaccine/form gates as present-or-missing before the lobby rush — not as a medical due-date call.
2. **Capacity and room plan** — Confirm an open run/suite or daycare slot for the stay dates from **their** capacity file. Do not raise a cap to fit a friend. Waitlist exists because the number is theirs.
3. **Arrival / intake role** — Match owner and dog to the reservation; confirm the boarding card packet; copy feeding, allergies, and meds lines exactly as written; list inbound belongings; confirm pickup window and authorized pickup names from their file. Completeness of vaccines, waiver, vet-on-file, and vet-release is a checklist, not a clinical clearance.
4. **Stay handoff files** — Kennel card / occupancy list, feeding sheet, meds-to-give list, crate or playgroup as **they** stored. Floor playgroup sorting and health glances stay with the handler they name.
5. **During stay** — Feeding as written; meds log page present or missing; incident form present or missing and routed to the person they name. Do not adjudicate blame, diagnose a wound, or declare a dangerous dog.
6. **Pickup / checkout pack** — Build today’s pickup list against occupancy; authorized names only from their file; belongings return as listed. This expert never releases a dog from the lobby.
7. **Side paths** — Waitlist in their existing order; missing-vaccine-file chase; missing-waiver chase; capacity vs booked for a named date.

Sources used for orientation (not this shop’s policy): PupCheckr morning check-in / daily-notes guides; Petunia boarding check-in and check-out role verification; Goodstay daily opening workflow (roster, vaccination alerts, daycare roster); Wagnur kennel check-in pre-arrival gates; ToolFluency pet-boarding booking and vaccination SOP; CanineOps boarding intake and occupancy-cap practice; Animal Friends OS boarding intake checklist. Payments and deposits appear in industry checklists; this role still never sends money or invents a fee.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the stay date, patient-dog, occupancy day, waitlist pull, or incident packet. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two stays. |
| 2. Intake source files | Drop boarding exports, cards, vaccine index, waiver folder, capacity file, and PDFs into `in/`. Read operations facts/rules. Do not invent fees, capacity, pickup names, or feeding. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (board, capacity, missing-files, feeding, pickup) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or checklist to `out/`. Journal the artifacts. Completeness packs are not clinical or release decisions. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase a missing rabies page, reprint a card, hand the pickup list to the closer). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Stay roster from boarding export | Boarding Day | `boarding-day` (default) |
| Capacity file vs booked for a date | Capacity Vs Booked | `capacity-vs-booked` |
| Feeding transcribed as written | Feeding From Cards | `feeding-from-cards` |
| Incident log + form present/missing | Incident Routing | `incident-routing` |
| Meds-to-give copied as written; log page present | Meds To Give List As Written | `meds-to-give-list-as-written` |
| Required vaccine pages missing/unreadable/wrong dog | Missing Vaccine Files | `missing-vaccine-files` |
| Pickup names vs occupancy | Pickup List | `pickup-list` |
| Waitlist order, dates, stay type | Waitlist | `waitlist` |
| Waiver unsigned/undated/wrong version/missing pages | Waiver Missing | `waiver-missing` |

Belongings lists, camera-privacy flags, photo-release, eval flags, and after-hours routing live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never diagnose or release) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **daycare/boarding office** role, not a veterinarian, not a playgroup handler, and not a payments clerk.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Industry “verify vaccines are current” is implemented here as **file present or missing**, never as a medical overdue decision.
- Payments, deposits, and refunds appear in public kennel checklists; this role still never sends money or invents a fee.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
