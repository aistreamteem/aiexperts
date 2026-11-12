# Role work-item method — Staffing agency office admin

**Role:** Staffing agency office admin  
**Industry:** Small US staffing office that places temps at client sites  
**Research date:** 2026-11-08

This role produces **files** (assignment boards, open-order lists, missing-credential-date lists, timesheet-completeness packs, DNS/DNR lists, orientation-missing lists, holiday-shift lists, incident-routing packs). It does **not** give employment-law or immigration advice, decide firing or discipline, send money, or build a recruiting CRM product.

## Industry funnel (research)

Typical US staffing-branch admin / coordinator work, from branch job descriptions and staffing-ops guides (job order → assignment → credential/onboard completeness → time capture → closeout):

1. **Job order intake** — Capture the client request as they coded it (client, site, shift, headcount, start window, class/rate pointers). List orders still open or partial-fill. Do not invent or close orders. Do not run a CRM pipeline.
2. **Assignment / dispatch board** — Who is on which client, shift, start, and expected end, with DNS/unavailable filters they already coded. They dispatch. This role lists holes. Do not invent a placement.
3. **Credential and screening dates** — License/cert expiration or issued dates, background and drug-screen **dates** as their log (not a verdict or result copy), I-9 index as present/missing dates (not counsel). Flag blanks they track. They decide who may still be sent.
4. **Orientation / first-day packet** — Sign-ins, safety-video acks, handbook/drug-policy acks against people who should have a packet. Completeness only. They collect missing acks.
5. **Do-not-send / do-not-return** — Print people flagged DNS or DNR with the scope they coded. They own the flags. This role does not invent a flag or fire anyone.
6. **Timesheet completeness** — Missing timesheet files, punches, blank totals, missing client-sign or approval ticks for the named period. Do not invent hours or decide overtime as law. They chase the site.
7. **Fill versus open** — Join orders to assignments using **their** status words and fill-rate formula. Operations math, not a marketing dashboard.
8. **Holiday / shutdown shifts** — Who is scheduled on a holiday **they wrote**, with premiums only from the rate file. Do not invent a federal-holiday list.
9. **Incident routing** — Form-present, date, site, named receiver. They investigate. This role flags missing forms and does not give a workers'-comp opinion.
10. **Side paths** — End-of-assignment, replacement, conversion-fee quote, certified-payroll file present, attendance codes: live in shared facts/rules on the board or timesheet pack. Not separate process skills.

Sources used for orientation (not this shop’s policy): TalentZok / Clark Atlanta branch-admin weekly rhythm (temp board, background/drug-screen tracking, Monday missing-timecard chase); Workhint staffing workflow (request → assignment → onboard → time → closeout); ATZ CRM job-order health as operations listing not product build; Baybloom staffing ops (credentials, timesheet exceptions); MAU Branch Coordinator and Bonney / Arizona Labor Force staffing-coordinator duties (onboarding completeness, orientations, timecards, credential audit). OSHA temporary-worker pages and DOL WH-347 are orientation only.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the assignment week, credential pack date, timesheet period, open-order pull, or incident batch. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two weeks or two people. Use their worker number, not SSN. |
| 2. Intake source files | Drop assignment sheets, rate files, timesheet CSVs, credential logs, PDFs into `in/`. Read shared facts/rules. Do not invent rates, holidays, markups, OT, or required certs. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (boards, missing dates, open orders, completeness) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or checklist to `out/`. Journal the artifacts. Completeness packs are not legal opinions, payroll approvals, or dispatch decisions. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase timesheets, collect a card, dispatch, investigate). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Who is placed where (default) | Assignment Board | `assignment-board` |
| Open / partial-fill orders | Open Job Orders | `open-job-orders` |
| Filled versus open math | Fill Vs Open | `fill-vs-open` |
| License / credential dates | Credential Expirations | `credential-expirations` |
| First-day acks | Orientation Missing | `orientation-missing` |
| DNS / DNR flags they coded | Do Not Send List | `do-not-send-list` |
| Hours files for a named period | Timesheet Completeness | `timesheet-completeness` |
| Holiday or shutdown schedule | Holiday Shift List | `holiday-shift-list` |
| Incident form routing | Incident Routing | `incident-routing` |

End-of-assignment, replacement, conversion-fee quotes, certified-payroll file present, I-9/W-4/direct-deposit **present** flags, and attendance codes live in shared facts/rules on the relevant pack; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never fire, never employment-law) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **staffing office admin** role, not a recruiter CRM product, employment lawyer, immigration counsel, or payroll-tax advisor.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added (certified payroll and conversion fees stay file-completeness facts).
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
