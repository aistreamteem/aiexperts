# Role work-item method — Church / house-of-worship office

**Role:** Church / house-of-worship office  
**Industry:** US congregation or house-of-worship administrative office  
**Research date:** 2026-11-08

This role produces **files** (week calendars, giving-batch completeness lists, missing-fund lists, pledge-vs-received joins, statement-run lists, volunteer rosters, background-date lists, facility-COI gaps, board/session packet indexes). It does **not** move money, give tax opinions, invent fund codes or deductible amounts, value in-kind gifts, decide benevolence, issue a safeguarding legal opinion, run a fundraising CRM, or provide pastoral counseling.

## Industry cadence (research)

Typical US church-office work, from job descriptions and operations guides (weekly loop plus monthly board and annual statements):

1. **Week calendar and rooms** — Keep the master parish/facility calendar so two groups do not book the same room; fold in weddings, funerals, ministries, and outside building-use holds. Offices publish a weekly events pack and catch double-bookings in staff calendar review.
2. **Giving batch** — Count and record the week’s gifts (cash/check plus online export) the same or next business day; match the signed count sheet to the giving-software export; dual-control stays as their written process. Completeness of the batch, not a posting or a deposit.
3. **Fund coding** — Record gifts to the fund they already coded. Blank or unknown codes are a chase list, not a chart you invent.
4. **Volunteer roster and background dates** — Publish next week’s volunteer schedule; list who serves where; copy clearance/background **dates and their status words** next to roles their policy tags as date-required. Do not decide anyone is “cleared” as counsel.
5. **Facility use and COI** — Intake building-use requests; keep outside groups next to required certificates of insurance. Missing or expired COI on a still-scheduled use is a flag. Do not approve use or waive coverage.
6. **Board / session pack** — Assemble the packet (agenda, prior minutes, treasurer export, ministry reports) against **their** checklist, typically several business days before the meeting. Completeness only — not a motion or a vote.
7. **Statements and pledges** — Build a statement run list from **their** process file and giving export (year-end target often by January 31 as practice). Join pledge sheet to gifts their process counts toward a pledge. Not a tax opinion and not an invented pledge.

Sources used for orientation (not this shop’s policy): Grain church-administrator weekly/annual calendar; OnlineGiving church-operations cadence (weekly giving + volunteer schedule + calendar; monthly board packet; quarterly background expirations; year-end statements); parish office-administrator job descriptions (master calendar, facility use, COI/key logs, session packets, volunteer background processing); Union Baptist / similar office-manager duties (vendor COIs, children’s-committee background files, annual contribution statements).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the Sunday, batch, week, meeting date, ministry roster, or facility period. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two batches or two Sundays. |
| 2. Intake source files | Drop giving exports, count sheets, calendars, rosters, COI PDFs, and packet folders into `in/`. Read shared facts/rules. Do not invent funds, gifts, rooms, or clearance verdicts. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (exports, indexes, missing lists) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or checklist to `out/`. Journal the artifacts. Completeness packs are not approvals, deposits, tax letters, or clearance verdicts. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase a fund code, request a COI, send statements). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* office works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Cadence slice | Workflow | Registry id |
| --- | --- | --- |
| Weekly room/building pack | Week Calendar | `week-calendar` (default) |
| Offering batch vs signed count sheet | Giving Batch From Export | `giving-batch-from-export` |
| Blank or unknown fund codes | Missing Fund Codes | `missing-fund-codes` |
| Pledge sheet vs gifts counted toward it | Pledge vs Received | `pledge-vs-received` |
| Contribution-statement run (their process) | Statement Run List — Their Process | `statement-run-list-their-process` |
| Ministry team list from their export | Volunteer Roster | `volunteer-roster` |
| Background dates vs date-required roles | Background Dates As File | `background-dates-as-file` |
| Outside facility use missing a COI | Facility COI Missing | `facility-coi-missing` |
| Board/session folder vs packet list | Board Pack | `board-pack` |

Membership-roll edits, bulletin product work, livestream products, benevolence decisions, and pastoral notes live in shared facts/rules as **refuse or completeness-only**; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never move money or give tax/pastoral opinions) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **church office admin** role, not a treasurer who posts and deposits, not counsel, not a pastor, and not a fundraising-CRM product.
- Existing nine work maps already match the admin slices of the industry cadence; no extra workflow was added.
- Default registry job is `week-calendar` (usual weekly hub). Operator may pick `giving-batch-from-export` or `background-dates-as-file` when that is the named job.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
