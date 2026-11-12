# Role work-item method — Wholesale / inventory role

**Role:** Wholesale / inventory role  
**Industry:** Small US wholesale distributor or shop stockroom (file-based; not a WMS product)  
**Research date:** 2026-11-08

This role produces **files** (receiving-match packs, putaway lists, pick lists, count-variance CSVs, reorder lists, lot/expiry flags, dead-stock lists, RMA condition sheets, transfer lists, ABC class sheets). It does **not** post book adjustments, send money, invent on-hand quantities, SKUs, POs, or lots, mark a shipment cleared through customs, act as a customs broker, classify HTS, ship hazmat, dump expired stock, or run a warehouse-management product.

## Industry cycle (research)

Typical US wholesale / inventory-control work, from warehouse SOPs and inventory-clerk job descriptions (inbound → putaway → pick/pack → count/control → replenish → returns):

1. **Receiving match** — Compare the purchase order, packing slip (and ASN if they use one), and dock count. Flag shorts, overs, damage, extra lines, and UOM mismatches. ASN is a plan, not a receipt. BOL is freight paperwork, not a line count and not a customs clearance.
2. **Putaway** — Direct accepted goods to bins the receiver wrote or preferred locations from their map or item master. Do not invent aisle/rack/slot labels.
3. **Pick / pack** — Build a pick list from their order export and on-hand or available file. Do not invent a substitute, a promise date, or a fill.
4. **Transfers** — Site-to-site (or warehouse-to-counter) moves from their transfer file: from, to, SKU, qty, UOM. In-transit is not on-hand at either end.
5. **Cycle count and ABC** — Count a scheduled slice (often by ABC class). Blind sheets hide book qty. Variances go to review with their recount threshold — not a silent book fix. This role lists variances; it does not authorize write-offs.
6. **Lot / expiry** — Flag lots and dates from **their** file (FEFO/FIFO only if they named the rule). Do not invent lots or dates. Do not dump expired stock.
7. **Dead stock** — Slow-mover list from last-movement or last-sale dates they provided, plus quantity. Do not call stock worthless.
8. **Reorder** — SKUs at or below **their** min from **their** stock file. Buyer placement and payment stay out of this role.
9. **RMA / returns** — Condition and sellable flag from their RMA sheet. Do not credit. Do not restock as good on-hand unless their line says sellable.

Sources used for orientation (not this shop’s policy): Cleverence inventory-control SOP (receive → putaway → ABC cycle count → variance → RMA disposition); Xorosoft wholesale-distribution warehouse guide (PO receiving, exceptions, directed putaway); Glyde inventory-management SOP (ASN/BOL check, putaway, transfers, ABC counts, approved adjustments); Hyring / SpartanNash-style inventory-control clerk duties (cycle count, slot accuracy, short-dated and damage lists). This expert works **exports and PDFs**, not the WMS itself.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the receipt, count date, pick wave, transfer, RMA, or reorder pull. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two POs or two count dates unless they named a combined pack. |
| 2. Intake source files | Drop CSVs and PDFs into `in/`. Read operations facts/rules. Do not invent on-hand, SKUs, POs, lots, mins, or bins. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (PO extract, receiving lines, variance, reorder, pick, lots) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or match sheet to `out/`. Journal the artifacts. Completeness and flags are not book postings or payments. | `out/*.md` plus supporting CSVs | Operator uses the pack (recount, chase a short, place a buy, credit an RMA). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Cycle slice | Workflow | Registry id |
| --- | --- | --- |
| PO vs packing slip vs dock count | Receiving Match | `receiving-match` (default) |
| Bins after receive | Putaway List | `putaway-list` |
| Order export → pick list | Pick Pack | `pick-pack` |
| Site-to-site move | Transfer | `transfer` |
| Rolling count vs book | Cycle Count | `cycle-count` |
| Class from their rules or value column | ABC Class | `abc-class` |
| Slow movers from their dates | Dead Stock | `dead-stock` |
| Lots and expiry from their file | Lot Expiry | `lot-expiry` |
| SKUs at or below their min | Reorder | `reorder` |
| Return condition / sellable flag | RMA Returns | `rma-returns` |

Blind-count hiding, UOM checks, one-warehouse-unless-asked, consignment labeling, quarantine holds, and “do not invent qty/SKU/PO/lot” live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent on-hand, never send money, never customs) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **wholesale / inventory admin role** that works files, not a licensed customs broker, hazmat shipper, FDA legal reviewer, or WMS implementer.
- Existing ten work maps already match the admin slices of the warehouse cycle; no extra workflow was added.
- Default job is **receiving-match** (inbound start of the cycle). ABC class remains a registered analysis job.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
