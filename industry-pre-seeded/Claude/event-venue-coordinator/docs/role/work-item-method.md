# Role work-item method — Event venue coordinator

**Role:** Event venue coordinator  
**Industry:** US banquet hall, hotel banquet role, wedding barn, club, or small conference venue  
**Research date:** 2026-11-08

This role produces **files** (BEO packs, hold-versus-definite lists, renter-COI missing lists, cutoff lists, diagram revision logs, guarantee-versus-setup comparisons, load-in calendars, group-block pickup sheets, banquet-check exception packs). It does **not** serve as a liquor license, stamp fire-marshal occupancy, invent rates or F&B minimums, give ADA legal opinions, design electrical drops, pay vendors or guests, or store card PAN.

## Industry funnel (research)

Typical US venue / hotel catering work, from banquet-event-order guides and venue checklists (inquiry → hold → definite → BEO → guarantee → execute → banquet check):

1. **Inquiry** — Capture date, space, headcount, and budget. Do not invent availability or a rate.
2. **Hold / tentative** — Provisionally hold the date with an expiry (cutoff / option date) so the diary is not silently blocked. Keep status as they coded it.
3. **Definite / contract** — Signed agreement and deposit convert the booking from provisional to confirmed. This role lists status from their hold and definite sheets; it does not bind coverage or take payment.
4. **Planning** — Menu, floor plan, running order, AV, vendor access, and insurance certificates build up over weeks. COIs stay on a present / expired / missing-wording list.
5. **BEO issue** — Banquet event order pages (typically issued days to weeks out) become the document kitchen, setup, AV, and the captain work from. Packet completeness is a file check: every definite function should have a BEO page, or name the miss. Draft versus issued stays labeled.
6. **Guarantee / cutoff** — Written guaranteed headcount by the contractual due date (commonly a few business days out — **their** contract, never a remembered 72 hours). Kitchen and setup counts follow the guarantee, not the old inquiry. Diagram chair counts that disagree are a revision question.
7. **Function briefing / load-in** — Dock, elevator, and vendor arrival windows from the timeline and BEO time blocks. Blank load-in on a vendor-heavy day is an ask, not a two-hours-before default.
8. **Execute and banquet check** — Day-of setup follows the latest dated diagram and issued BEO. After the event, compare the banquet-check PDF to the BEO for menu, counts, extras, service charge, and tax as their tax file. Do not mark paid. Do not store PAN.
9. **Side paths** — Sleeping-room group block pickup if a block file exists; rain plan only as their written backup; leftover food only per their policy.

Sources used for orientation (not this shop’s policy): HIS banquet-event-order lifecycle (enquiry → hold → contract → BEO → guarantee → close-out); Cloud Event Manager venue checklist (booking → COI → guarantee → invoice); Caterloom pre-event BEO review checklist; HotelAmplify BEO creation steps; Events Industry Council BEO glossary. Starter notes in shared memory remain guesses until the operator confirms *this* venue.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the event date + room, definite book, COI chase, or period. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two events. |
| 2. Intake source files | Drop BEO PDFs, hold/definite sheets, diagrams, COI folders, banquet-check PDFs into `in/`. Read shared facts/rules. Do not invent rates, minimums, guarantees, occupancy law, or licenses. | Files in `in/` | Missing BEO, contract, or COI folder → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (indexes, missing-COI, holds, calendars) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or checklist to `out/`. Journal the artifacts. Completeness packs are not licenses, stamps, or payments. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase a COI, issue the BEO, release a hold). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* venue works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Tentative holds vs signed definite | Hold vs Definite | `hold-vs-definite` |
| Hold cutoff / option dates due | Cutoff List | `cutoff-list` |
| BEO pages for definite functions | BEO Pack | `beo-pack` (common pack job) |
| Banquet check vs matching BEO | Banquet Check File | `banquet-check-file` (default) |
| Renter / vendor COI present, expired, missing | COI Missing | `coi-missing` |
| Dated diagram revisions | Diagram Revision Log | `diagram-revision-log` |
| Guarantee count vs diagram chairs | Guarantee vs Setup | `guarantee-vs-setup` |
| Dock / elevator / vendor arrivals | Load-In Calendar | `load-in-calendar` |
| Sleeping-room block pickup if a file exists | Group Pickup If Any | `group-pickup-if-any` |

Inquiry logging, rain-plan routing, leftover-food policy, and bar/labor counts live in shared facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never serve as the liquor license or fire stamp) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **venue coordinator admin** role, not a liquor-license holder, fire marshal, electrician, ADA counsel, or cashier.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Industry guarantee windows (48–72 hours, three to seven business days) are orientation only; this role asks when their contract has no due date.
