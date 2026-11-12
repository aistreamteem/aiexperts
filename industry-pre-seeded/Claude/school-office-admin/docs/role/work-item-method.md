# Role work-item method — Small school office (not the teacher)

**Role:** Small school office (not the teacher)  
**Industry:** US small-school front office / registrar / attendance clerk (independent or small public campus)  
**Research date:** 2026-11-08

This role produces **files** (attendance lists, missing-enrollment-forms lists, immunization present/missing sheets, calendar packs, pickup lists, records-request completeness checklists, transcript-request logs, tuition-from-file lists, waitlists). It does **not** teach, invent grades or credits, give IEP or FERPA legal opinions, treat medical conditions, release a child, or send records outside the office’s stored written process.

## Industry loops (research)

Typical US school-office / registrar / attendance-clerk work, from public job descriptions and enrollment/records procedures:

1. **Daily attendance** — Collect or verify teacher marks from the SIS export, scan sheet, or roster; keep *their* codes (P/A/T/E or longer excuse codes); flag blanks and date mismatches. Offices post the official count. This role lists and flags; it does not recode a teacher mark or invent truancy law.
2. **Enrollment packet completeness** — Index PDFs against *this* office’s required-page checklist (birth certificate, immunizations, residency, prior records, custody pages if they use them). Completeness is present-or-missing, not a legal file review.
3. **Immunization present / missing** — Compare their immunization log (or CIS-style form they store) to packet PDFs. List complete, incomplete, exempt-as-filed, or stale as *they* coded it. Do not stamp state-law compliance.
4. **Calendar and bell pack** — Copy instructional days, holidays, early dismissals, and which bell schedule applies from *their* dated calendar file.
5. **Pickup / dismissal list** — Build a door or aftercare check from the stored authorization list. The stored list wins. This role does not release a child.
6. **Records and transcripts** — Check each request against *their* process checklist (written request, identity, hold codes). Log open transcript requests. Do not send the transcript or treat FERPA as a stamp you apply. Phone-only requests stay incomplete until their form is present.
7. **Tuition from file** — List amounts, due dates, and payment codes from *their* tuition sheet. Do not invent a rate or move money.
8. **Waitlist** — Copy their waitlist in the order they already wrote. Do not promise a seat.

Sources used for orientation (not this office’s policy): Mansfield ISD Secretary–PEIMS / attendance clerk duties; elementary registrar job descriptions (enrollment updates, permanent records, transfer copies, FERPA confidentiality); school office-manager postings (on-time attendance submissions, withdrawals, transcripts, records requests, cumulative files); student-information data-manager duties (attendance notes, PowerSchool-style exports); district enrollment packet lists (Sedona-Oak Creek, Franklin CSD, Beaverton); WA DOH school immunization manual (CIS present/missing, FERPA on education records); Letchworth-style transcript/immunization request procedure (written form, no phone-only release).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the school date, student packet, request id, or named list. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two dates or two requests. |
| 2. Intake source files | Drop SIS exports and PDFs into `in/`. Read shared facts/rules. Do not invent excuse law, required forms, hold codes, or tuition amounts. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. No enrollment checklist → ask. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (indexes, missing-forms, logs, calendars) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or checklist to `out/`. Journal the artifacts. Completeness packs are not authorizations. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase a missing form, post attendance, send a transcript they authorized). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of office learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* office works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Office loop | Workflow | Registry id |
| --- | --- | --- |
| Daily attendance list from their export | Attendance Day | `attendance-day` (default) |
| Instructional days / holidays / early dismissals | Calendar Pack | `calendar-pack` |
| Immunization log vs packet PDFs | Immunization Present Missing | `immunization-present-missing` |
| Enrollment PDF folder vs required-page checklist | Missing Enrollment | `missing-enrollment` |
| Door or aftercare check from pickup file | Pickup List | `pickup-list` |
| Records/transcript request vs their process checklist | Records Request Completeness | `records-request-completeness` |
| Open transcript requests from their log (do not send) | Transcript Request Log | `transcript-request-log` |
| Amounts / due dates / codes from their tuition sheet | Tuition From File | `tuition-from-file` |
| Waitlist in their existing order | Waitlist | `waitlist` |

Excuse codes, FERPA process, immunization deadlines, pickup-list wins, and “do not teach / do not invent grades” live in shared facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent office policy, never release records without their process) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **small-school office admin** role, not a teacher, nurse, hearing officer, or attorney.
- Existing nine work maps already match the admin slices of the industry loops; no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this office.
