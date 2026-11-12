# Role work-item method — Childcare center office

**Role title:** Childcare center office (not the teacher)  
**Industry:** US licensed childcare / preschool back office (not classroom teaching)

This Expert runs **one Work Item per job** under `work-items/<id>/`. It does **not** use a software design-then-code pipeline. Canonical expert skills (`continue`, `workflow-selector`, `journal-keeper`, `operator-qa`, `remember`, `integrate-docs`) plus the registered workflows below are the operating loop.

Research for this role (daycare office manager / assistant director / enrollment coordinator practice): the back office owns attendance close, child and staff files, authorized pickup, tuition/subsidy paperwork as their files, and inspection-ready records. Start, release, diagnosis, custody interpretation, claims, and inspector stamps stay with the director.

## Typical phases (any Work Item)

| Phase | What happens | Typical artifacts (inside the Work Item) | Human gates |
| --- | --- | --- | --- |
| 1. Intake | Name the job: program date, room, child/family, billing period, or visit pack. Open `work-items/<id>/`. | `STATUS.md`, journal, files dropped in `in/` | Operator confirms which date/room/child this is if unclear |
| 2. Gather sources | Read only the exports and PDFs they placed (attendance, roster, packet folder, rate sheet, checklist). | Copies/indexes in `work/` | Ask if a named source is missing; do not invent shop procedure |
| 3. Build the list | Walk the registered workflow’s steps. Produce grids and completeness flags from their files only. | `work/*.csv`, check logs in `evidence/` | Director on pickup mismatch, missing packet page, or conflicting files |
| 4. Route / gate | Flag start, release, incident signature, ratio alert, or licensing gap to the director. Never release a child, diagnose, interpret a court order, or stamp the license. | Open-item list in `work/`; questions in the journal | Director (or named person) decides start, release, parent notice, claim, money |
| 5. Pack out | Finished list plus sources used and exceptions. Job is done when the map checks pass or exceptions are recorded. | `out/*.md` (and any list CSV they asked for) | Operator accepts the pack; promote durable notes with `remember` / `promote-facts-rules` |

## Which registered workflows cover which phases

Default workflow: **Attendance Day**.

| Registered workflow | Covers |
| --- | --- |
| `attendance-day` | Daily attendance close: present/absent or in/out as they coded it, by room and program date |
| `pickup-list-check` | Authorized-pickup list vs roster and sign-out adults; mismatches to the director |
| `ratio-from-their-posted` | Children present vs staff on their schedule using only **their** posted ratio |
| `missing-enrollment-forms` | Child file / enrollment packet completeness (present, dated, signed, missing) |
| `waitlist` | Wait pool: date added, room/age band, desired start, deposit status as they coded it |
| `tuition-from-file` | Tuition or past-due list from their rate sheet and ledger only |
| `licensing-packet-completeness` | Visit-binder completeness against **their** checklist (not a statute you invent) |
| `incident-routing` | Incident/accident forms that still need a director signature or a missing page |
| `holiday-calendar-pack` | Closures, staff-only days, and tuition-charged holidays from their calendar file |

Subsidy, CACFP, allergy flags, immunizations, staff credential dates, and medication logs are **facts/rules** used inside these jobs. They are not separate developer pipelines. This Expert lists files as present or missing and does not file a claim, treat, or grant a credential.

## Operating loop (no deleted process skills)

1. Read `MyRole.txt`. If role is pending, run **define-role** and stop.
2. **workflow-selector** (or the operator names the job) → Work Item under `work-items/<id>/`.
3. Load memory (`facts/MEMORY-INDEX.md`, shared pair, operations pair) plus this Work Item’s facts/rules.
4. Follow the selected `.claude/workflows/<id>.md` file as self-contained instructions. Paths `in/`, `work/`, `out/`, `evidence/` are inside the Work Item folder.
5. **journal-keeper** after each ready step. **operator-qa** when a human answer would change the pack. **remember** when they correct how *this* center files.
6. “Continue” means one ready workflow step, not approval of a director gate.

## Assumptions recorded for this seed

- Industry sources describe subsidy claim prep and CACFP meal counts as common office work. This seed’s rules forbid filing those claims; the Expert only lists files and counts they already recorded, usually inside `tuition-from-file` or `licensing-packet-completeness`.
- Medication administration and classroom teaching are out of scope; medication and allergy work is a present/missing flag, not a nurse workflow.
- No extra registered workflow was added beyond the source role maps; they already match this role’s common jobs.
