# Role work-item method — Moving company office

**Role:** Moving company office  
**Industry:** US household-goods / local moving office (estimator, dispatcher, and claims-file clerk slices)  
**Research date:** 2026-11-08

This role produces **files** (estimate drafts from their rate file, inventory completeness packs, crew-day lists, truck calendars, materials pulls, delivery-window lists, weigh-ticket indexes, high-value present/missing checks, claims-routing packs). It does **not** invent weight or cube, give tariff or DOT legal opinions, certify a truck or driver, pay crews, settle claims, or store card PAN.

## Industry funnel (research)

Typical US moving-office work, from owner workflow guides, dispatch/claims field practice, and FMCSA-oriented estimate/inventory/BOL paperwork:

1. **Intake / inquiry** — Capture origin, dest, requested load day, and access questions. Operator names the move (estimate number, origin date, or their job id) and drops the live rate file, inventory, calendar, tickets, or claim papers.
2. **Survey / inventory** — Room-by-room sheet is the master record later documents view. PBO vs CP, photos, high-value list if their form requires it. Cube/weight stay blank unless their sheet or scale ticket already has a number.
3. **Estimate** — Draft from their rate file + stored inventory. Binding / non-binding / not-to-exceed copied from their form. Accessorials only when the survey already names them. Operator sends the estimate.
4. **Dispatch prep** — Crew size vs job, truck vs cube, materials/carton pull, dest delivery windows, building/elevator/COI notes from their files. Do not invent a person, a free truck day, a box count, or a clock hour.
5. **Load-day papers** — Weigh-ticket index (tare/gross/net as written). High-value list check if not already done. BOL completeness is listed from their form; they issue and sign.
6. **Claims routing** — Assemble claim row, named photos, inventory lines, BOL number. Quote deadline words from their form only. This Expert does not settle.

Sources used for orientation (not this shop’s policy): mover-owner eight-handoff workflow (inquiry → survey → estimate → dispatch → crew → close); MoveWise-style intake/survey/estimate then book/dispatch then pack/load then delivery/claims; Supermove office checklist (lead → quote → book → assign crew/truck → invoice); interstate survey → estimate → BOL/inventory → claims-on-evidence practice. Payment, deposits, crew pay, tariff/DOT legal opinions, and inventing weight or cube are **out of scope** (see `MyRole.txt`).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the move (estimate number, origin date, or their job id). Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two moves. |
| 2. Intake source files | Drop the live rate file, inventory, calendar, tickets, or claim papers into `in/`. Read operations facts/rules. Do not invent weight, cube, rates, crew names, or delivery hours. | Files in `in/` | Missing file → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (indexes, lists, missing-item flags) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or draft to `out/`. Journal the artifacts. Completeness packs are not legal stamps, settlements, or sent estimates. | `out/*.md` plus supporting CSVs | Operator uses the pack (sends the estimate, dispatches, sends the truck back to the scale, routes the claim). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Estimate from their rate file + stored inventory | Estimate From Rate File | `estimate-from-rate-file` (default) |
| Survey sheet vs rooms, PBO/CP, high-value if required | Inventory Completeness | `inventory-completeness` |
| High-value form present/missing | High Value List Check | `high-value-list-check` |
| Carton/crate pull from their materials sheet | Materials List | `materials-list` |
| Day list from roster + booked calendar | Crew Day | `crew-day` |
| Truck unit/date collisions | Truck Calendar | `truck-calendar` |
| Dest windows and spreads | Delivery Window List | `delivery-window-list` |
| Scale slips: tare, gross, net as written | Weigh Ticket Pack | `weigh-ticket-pack` |
| Claim row, photos, BOL number to named owner | Claims Routing | `claims-routing` |

Default new-job workflow: **estimate-from-rate-file** (typical office start is survey → written estimate). Pick another registered job when the operator already has a booked move, a scale slip, or a claim file.

Guest-card-style extras (elevator/COI, parking permit, SIT, valuation as their form) live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent weight/cube, never pay, never tariff/DOT legal) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **moving-company office** role, not a tariff lawyer, scale, van-line claims adjuster, or payroll clerk.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Weight and cube stay blank unless their scale ticket or sheet already has them.
