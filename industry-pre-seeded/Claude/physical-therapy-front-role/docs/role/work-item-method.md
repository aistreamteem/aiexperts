# Role work-item method — Physical therapy front role

**Role:** Physical therapy front role (not the therapist)  
**Industry:** US outpatient physical-therapy clinic front office  
**Research date:** 2026-11-08

This role produces **files** (day lists, remaining-visit sheets copied from their tracker, referral/POC completeness packs, recert-date lists, HEP print indexes, no-show lists, wait-list packs, visit-count checks, day-close tender lists). It does **not** treat, diagnose, invent remaining visits or coverage, choose timed codes or units as care, or give Medicare billing or legal opinions.

## Industry funnel (research)

Typical US outpatient PT front-role work, from clinic SOPs and job descriptions (open → check-in → paperwork chase → close):

1. **Open / day list** — Print or export today’s schedule; keep closed blocks, lunch, and documentation rows; flag overlaps their double-book rule does not allow. Review eligibility and authorization against today’s booked visits before patients arrive.
2. **Eligibility and remaining visits** — Quote active/inactive, copay, and visit-limit sentences from a dated screenshot or tracker. Authorized, used, and remaining come only from their auth tracker and visit-count export — never invented.
3. **Check-in paperwork** — Referral and plan-of-care completeness (named pages + physician signature as their form requires). Intake/NPP presence is their folder, not a clinical note you write.
4. **Recert / POC dates** — List recert due dates and POC end dates as stored. Flag booked visits after a POC end date. They obtain signatures; you pack completeness. Do not invent a 90-day Medicare interval.
5. **HEP print index** — List which charts have a therapist-attached or named HEP PDF ready to print. Do not pick exercises as care.
6. **No-show / cancel / wait list** — List rows they already coded no-show or cancel. Keep wait-list order. Match open slots as options; they choose who is offered.
7. **Day close** — Copy tender types and amounts from their close report or drawer sheet. Do not send a deposit or store PAN.

Sources used for orientation (not this shop’s policy): Physio Therapist Scheduling daily SOP (schedule, eligibility, auth-by-count, waitlist, close); WebPT/Therabill daily eligibility and expiring-authorization guides; Healing Motion / Premier PT front-office job descriptions (verify, schedule to the plan of care, fill cancellations from wait list, collect copays, close batch); R2P clinic-coordinator daily tasks (print agenda, authorization log, ending/expired auths).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the clinic date, remaining-visits pack, referral folder, recert pull, HEP print, no-show list, wait-list pull, visit-count check, or day-close. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two clinic dates or two charts unless they named a combined pack. |
| 2. Intake source files | Drop EHR exports, auth trackers, card images, and folders they pointed to into `in/`. Read operations facts/rules. Do not invent remaining visits, fees, codes, or shop procedure. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. Stale eligibility/remaining → ask. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (day list, remaining, missing-forms, recert dates, HEP index, no-shows, wait-list, exceptions, tender) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or checklist to `out/`. Journal the artifacts. Completeness packs are not treatment, diagnosis, or a coverage promise. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase a missing referral, call a wait-list row, correct the live tracker). This expert does not treat or decide coverage. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* clinic works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Today’s book by time / therapist / type | Day List | `day-list` |
| Authorized / used / remaining from their files | Auth Remaining From File | `auth-remaining-from-file` (default) |
| Visit-count export vs auth tracker | Visit Count Export Check | `visit-count-export-check` |
| Inbound scripts and plans of care | Referral POC Completeness | `referral-poc-completeness` |
| Recert due and POC end dates as stored | Recert Dates | `recert-dates` |
| Therapist-named HEP PDFs ready to print | HEP Print Index | `hep-print-index` |
| Rows they already coded no-show / late cancel | No Show List | `no-show-list` |
| Wait-list order and cancel wait-fill options | Wait List | `wait-list` |
| End-of-day tender from their close report | Day Close | `day-close` |

Eligibility screenshots, copay posted amounts, intake/NPP presence, workers’-comp/auto completeness, and HIPAA minimum-necessary live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never treat/diagnose, never invent remaining visits) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **front-role admin** pack, not a treating therapist, coder, biller-as-care, or Medicare-counsel role.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Registry default stays `auth-remaining-from-file` (a daily auth-by-count check). Opening the clinic day typically starts with `day-list` when they ask for tomorrow’s book.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- This expert copies from files they drop. It does not log into an EHR portal, call a payer, or message patients as a product.
