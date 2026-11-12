# Role work-item method — Pest control office

**Role:** Pest control office  
**Industry:** US structural pest-control office (routes, tickets, chemical logs as files — not an applicator license, not landscaping or lawn care)  
**Research date:** 2026-11-08

This role produces **files** (route-day lists, skip lists, callback lists, chemical-log completeness packs, inventory-vs-log sheets, bait-map indexes, device counts, estimates from their price file, WDO/termite form completeness packs). It does **not** apply or recommend a pesticide, invent a mix or EPA number, diagnose a structure, give wildlife legal advice, pay techs or vendors, or store gate codes.

## Industry funnel (research)

Typical US pest-control office work, from dispatcher/office SOPs and pest-software job flows (orientation only — not how *this* shop already works):

1. **Open / reconcile** — Match yesterday’s unclosed stops to today’s board. Confirm appointments. Apply cancellations and holds.
2. **Skip / hold list** — Wind, no-access, customer hold, and “do not service” rows win the day. Do not invent a skip to hide a miss.
3. **Route day / dispatch** — Build the tech’s ordered stop list from the route CSV and matching tickets: account, service, window, pet/child/dog flags, access as an ask (never a code). They dispatch. You write the list.
4. **Callbacks** — Open callbacks stay visible (original ticket, complaint words they recorded, warranty vs courtesy as their file). A callback is not finished when the pest is gone; it is finished when the office has the reason and the next action.
5. **Application records** — Completeness of chemical logs: date, account, product, EPA-from-file, rate-as-logged, tech name, interior vs exterior. Blanks stay blanks. Tickets that say treated with no log row stay holes.
6. **Inventory vs usage** — Compare on-hand chemical inventory to product names already on the log. Do not invent a quantity, mix, or EPA number. They buy. You do not pay the vendor.
7. **Devices / bait maps** — Index bait-station maps to account and ticket; count devices as written. Do not invent a station.
8. **WDO / termite pack** — Their WDO or termite form, graph present, photos named if they require them. Completeness only — not an inspector stamp.
9. **Estimate from price file** — Draft lines from **their** price file and the lead or ticket they stored. Do not invent a rate.
10. **Close exceptions** — Unclosed stops, missing tickets, missing log fields, and unlabeled targets stay questions. They schedule returns and they talk to the customer.

Sources used for orientation (not this shop’s policy): pest-control SOP open-to-close checklists (reconcile unclosed stops → route sheet → exceptions at close); PestBossPro / OpsVara / WebWork dispatch-board to ticket to EPA chemical record; commercial logbook and WDO/termite compliance packs; office-manager duties for callbacks, reinspections, and WDO scheduling.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the route day, ticket, callback board, log pack, map set, WDO folder, or estimate. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two route days or two tickets. |
| 2. Intake source files | Drop route CSV, tickets, logs, maps, price file, WDO PDFs into `in/`. Read operations facts/rules. Do not invent mix, EPA, rate, ticket, or target pest. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (route, tickets, skips, logs, indexes) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or completeness pack to `out/`. Journal the artifacts. Completeness packs are not licenses, diagnoses, or payments. | `out/*.md` plus supporting CSVs | Operator uses the pack (dispatch, chase a missing log, schedule a callback). This expert does not treat, stamp, or pay. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Daily board / dispatch | Route Day | `route-day` |
| Holds and do-not-service | Skip List | `skip-list` |
| Open callbacks | Callback List | `callback-list` |
| Application-record completeness | Chemical Log Completeness | `chemical-log-completeness` |
| On-hand vs logged products | Inventory Chem Vs Log | `inventory-chem-vs-log` |
| Bait-station maps | Bait Map Index | `bait-map-index` (registry default until they pick) |
| Station / trap counts | Device Count | `device-count` |
| Price-file estimates | Estimate From Price | `estimate-from-price` |
| WDO / termite form pack | Wdo Form Completeness | `wdo-form-completeness` |

Typical daily start in the industry is **route-day** (after applying **skip-list**). The registry default remains `bait-map-index` until the operator chooses. Missing-ticket, missing-target-label, pet/child/food/school flags, wind holds, and “never invent mix/EPA” live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent mix/EPA, never diagnose, never store gate codes) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **pest-control office** role, not a licensed applicator, wildlife attorney, or landscaping/lawn-care role.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Starter notes in operations memory are typical US practice, not how *this* shop already works, until they say so.
