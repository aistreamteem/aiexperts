# Role work-item method — Apartment leasing admin

**Role:** Apartment leasing admin  
**Industry:** US multifamily leasing office (conventional; affordable lists stay separate)  
**Research date:** 2026-11-08

This role produces **files** (guest-card / traffic tallies, showing lists, application completeness sheets, lease-packet checklists, make-ready vs move-in flags). It does **not** approve or deny applicants, give fair-housing legal opinions, send adverse-action letters, lock anyone out, or move money.

## Industry funnel (research)

Typical US leasing-consultant work, from operator manuals and job descriptions (guest-card → tour → application → screening → lease → move-in):

1. **Traffic / inquiry** — Log every call, walk-in, web lead, and locator referral on a guest card the same day; record source; follow the shop script. Offices keep a daily traffic / marketing scorecard (walk-ins, calls, shows, applications).
2. **Schedule and show** — Book tours inside posted office hours; prepare a unit or model that matches the guest card; collect ID per their tour rule; document the visit. Do not invent Sunday/holiday hours.
3. **Application** — Send or take the application; collect fee per their posted policy; check the packet for required forms, photo ID, income papers, screening authorization, roommate/guarantor extras. Completeness is a present-or-missing checklist, not a credit decision.
4. **Screening file** — Route by **their** screening-status export codes only. Managers or written criteria decide approve/deny. Adverse-action notices are theirs or the vendor’s.
5. **Lease packet** — Generate / assemble the lease plus addenda from **their** checklist (pet, parking, concession, lead, community policies). Match specials to the dated specials sheet. Completeness only — not a legal review.
6. **Make-ready vs move-in** — Confirm turn status before treating a commence date as workable; walk the unit near move-in; issue keys only when they say ready. Work orders stay on the property-manager role.
7. **Side paths** — Market waitlist in their existing order; affordable/program waitlist never mixed with guest-card traffic; denied-file routing by their words; specials matched to open floorplans.

Sources used for orientation (not this shop’s policy): Clearworth leasing-consultant duties; S2 Residential / Knock guest-card practice; AppFolio lead-to-resident tour → apply → screen → lease → keys; CRES-style daily traffic scorecard; Flynn-style application-processing worksheet; HUD fair-housing even-handed process (no steering, no legal opinion from this role).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the guest, showing day, application packet, waitlist pull, or period. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two applicants. |
| 2. Intake source files | Drop PMS exports and PDFs into `in/`. Read operations facts/rules. Do not invent hours, rents, fees, specials, or criteria. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (indexes, missing-forms, status, calendars) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or checklist to `out/`. Journal the artifacts. Completeness packs are not approvals. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase applicant, change a start date, send the lease). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Traffic / guest cards / source tally | Traffic Log | `traffic-log` |
| Hours, holidays, tours that fit posted hours | Hours And Tours | `hours-and-tours` |
| Today’s showings vs availability | Showing Day | `showing-day` |
| Live specials vs open floorplans | Specials From File | `specials-from-file` |
| Application PDFs present/missing | Application Completeness | `application-completeness` (default) |
| Screening-status export routing (their codes) | Denied File Routing | `denied-file-routing` |
| Lease folder vs addendum checklist | Lease Packet | `lease-packet` |
| Turn status vs lease start | Make Ready Vs Move In | `make-ready-vs-move-in` |
| Market waitlist in their order | Waitlist | `waitlist` |

Guest-card follow-up, no-shows, holds, and accessibility-request **routing** live in shared facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never approve/deny) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **leasing admin** role, not a licensed agent, property-manager owner pack, or attorney.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
