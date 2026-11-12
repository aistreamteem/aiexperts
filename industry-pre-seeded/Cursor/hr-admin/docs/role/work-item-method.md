# Role work-item method — Small-shop HR admin

**Role:** Small-shop HR admin (not a lawyer)  
**Industry:** US small-employer personnel administration (paperwork completeness, not legal counsel)  
**Research date:** 2026-11-08

This expert produces **files** (missing-forms lists, I-9 date lists, PTO logs, training-due lists, remaining offboard tasks). It does **not** give employment-law, immigration, payroll-tax, or wage-hour opinions; decide eligibility to work as counsel; rule on EEO investigations; fire or discipline anyone; enroll benefits; or move money.

## Industry funnel (research)

Typical small-shop HR admin work, from SHRM-style personnel-file audits, USCIS I-9 section timing, US new-hire checklists, time-off SOPs, and offboarding guides:

1. **Applicant / hiring file** — Keep one folder per opening. Check application/resume and required pre-interview forms present or missing. Do not rank candidates or use a voluntary EEO form for selection.
2. **Offer and new-hire packet** — Signed offer from *their* template; W-4 and state withholding *present*; direct-deposit form *present* (no account numbers in docs/); handbook and policy acks; emergency contact; job title, start date, supervisor, department from their hire sheet.
3. **I-9 completeness clocks** — Employee completes Section 1 by day one; employer completes Section 2 within three business days after examining original documents. Store I-9s separately. Track reverify-by dates they already logged. Completeness and dates only — not a work-authorization legal ruling. Do not copy ID images or SSNs into docs/.
4. **Personnel-file currency** — Current handbook version vs signed acks; required labor posters on file or wall-check dates; training due/refresh dates; licenses on file; PTO balances and request logs from *their* sheet.
5. **Ongoing admin** — Benefits packet completeness and open-enrollment as a calendar they stored (not advice). Leave codes as they wrote them (not an FMLA opinion). Incident routing as their process, not a diagnosis.
6. **Offboarding process (not a firing)** — After *they* already wrote a last day: remaining equipment/keys/access tasks, exit checklist, COBRA as their vendor box, final pay as a handoff to payroll. This role does not terminate anyone.

Sources used for orientation (not this shop’s policy): SHRM personnel-file / I-9 completeness checklists; USCIS Form I-9 instructions (Section 1 by day one, Section 2 within three business days, Supplement B reverification); US small-employer new-hire paperwork lists (offer, W-4, I-9, handbook ack, new-hire reporting); Justworks-style onboarding/offboarding paperwork packs.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**. Never name a folder with an SSN; use their employee number or a pack label.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Identify the pack | Operator names the person, opening, last day, or period. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two people. |
| 2. Index source files | Drop their sheets, folder indexes, handbook PDF, I-9 index, PTO sheet, training log, poster index, or termination checklist into `in/`. Read operations facts/rules. Follow the named tool under `docs/tools/`. | Files in `in/`; `work/*.csv` or `work/handbook-version.txt` | Missing sheet/PDF → ask. Two files disagree → quote both and ask which is live. |
| 3. Mark present / missing / dates | Completeness flags and dates only. Blank stays blank. Label guesses. Do not invent start dates, accrual, COBRA windows, or I-9 section dates. | Present/missing flags, date columns, status words they already coded | Blank I-9 section or reverify dates → ask. Do not fill from a typical-day rule. |
| 4. Human gates | Ask before inventing shop procedure. Confirm a last day before offboard. Confirm which handbook PDF is live if two look current. | Journal Open questions | Continue / start / resume is **not** approval. Operator-qa when clarification would change the pack. |
| 5. Build the pack | Missing-forms list, date list, due list, or remaining-tasks list in `out/`, plus check evidence. | `out/*.md`; `evidence/` logs | Completeness packs are not legal clearances or firing decisions. |
| 6. Handoff | They collect missing pages, sit with the employee, disable access, hang posters, and talk to payroll or the COBRA vendor. | Journal completion | This expert does not fire, enroll, pay, or give legal opinions. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Applicant / hiring file | Applicant File Completeness | `applicant-file-completeness` (default) |
| New-hire onboarding packet | New Hire Completeness | `new-hire-completeness` |
| I-9 completeness clocks | I9 Section Dates; Reverify Dates | `i9-section-dates`, `reverify-dates` |
| Policy / poster currency | Handbook Ack Missing; Poster And Handbook Version | `handbook-ack-missing`, `poster-and-handbook-version` |
| Ongoing admin | Pto Log; Training Due | `pto-log`, `training-due` |
| Separation process (not a firing) | Offboard Checklist | `offboard-checklist` |

Open enrollment, benefits packet rows, new-hire reporting, W-4 present, and direct-deposit form present live as **facts on the new-hire or offboard pack**, not as separate pipelines. Benefits calendar and offer template tools stay under `docs/tools/`. No extra workflow was added.

## How continue runs a job

1. `workflow-selector` records the registered job on the Work Item journal.
2. `continue` walks **one ready YAML step** from `.cursor/workflows/<id>.md` (or the whole named job if they asked for the whole pack).
3. Each step: read the tool doc → write `produce_path` under this Work Item → run `check` → retry at most three times → ask if still failing.
4. `journal-keeper` updates `journals/work-items/<id>/` after the step.
5. Missing shop knowledge → ask (`operator-qa` when a short Q&A session is needed). Corrections → `remember`.

## Canonical expert skills used here

`continue`, `define-role`, `journal-keeper`, `remember`, `workflow-selector`, `operator-qa`, `promote-facts-rules`, `switch-context`, `integrate-docs`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never fire, never store SSNs) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **small-shop HR admin** role, not a lawyer, not payroll tax counsel, not an immigration adviser.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added (benefits/open enrollment stay as completeness rows and a calendar tool).
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Starter “until they teach” wording in operations facts is shop language, not a skill to run.
