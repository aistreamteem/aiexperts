# Role work-item method — Wholesale / inventory role

**Role:** Wholesale / inventory role  
**Industry:** US small-to-midsize wholesale distribution and shop stockroom operations  
**Research date:** 2026-11-08

This role produces **files** (receiving PO-to-slip-to-dock match sheets, putaway bin lists, order pick/short lists, site transfer sheets, cycle-count variance packs, ABC classification worksheets, lot/expiry watchlists, slow-mover reports, reorder trigger lists, and RMA condition/sellable sheets). It does **not** administer a live WMS product, invent on-hand quantities/SKUs/POs/lots/bins, silently adjust book quantities, act as a customs broker or importer of record, mark shipments cleared through customs, certify hazmat or FDA/FSMA legal status, dispose of stock, issue customer credits, or move money.

## Industry stockroom & inventory-control cycle (research)

Typical US wholesale distribution and stockroom control workflows, synthesized from warehouse SOPs, ASCM/APICS inventory practice, and distributor receiving/counting manuals:

1. **Inbound receiving verification** — Match open purchase orders (and ASN/BOL when present) against the vendor packing slip and the physical dock count before goods touch a shelf. Record SKU, UOM, ordered quantity, received quantity, shorts, overages, damage, and required lot/serial numbers at the dock. Never treat an ASN or BOL as a line-level dock count or a customs clearance.
2. **Putaway and location assignment** — Route received goods from the dock to named bins, slots, bulk zones, coolers, or quarantine cages using the receiver's recorded bin or the shop's bin map / item-master preferred location. Keep lot/serial and site separation intact.
3. **Order fulfillment (pick / pack) & site transfers** — Build pick lists from open sales orders or transfer orders against confirmed on-hand or available-to-promise exports. Honor hard allocations, quarantine/damage holds, and consignment owner flags; record short picks explicitly without silent SKU or lot substitution; track inter-site transfers with transfer numbers and from/to sites.
4. **Cycle counting & physical inventory reconciliation** — Count scheduled slices of bins or SKUs on a rolling calendar (often stratified by ABC velocity/value class) with transaction freeze/cutoff windows and blind count sheets when requested. Compare counted quantity to book quantity in aligned UOMs, flag lines exceeding the shop's recount threshold, preserve counter names and dates, and route variances for authorized adjustment with reason codes rather than silently fixing book numbers.
5. **Stock health, lot/expiry & ABC review** — Maintain ABC class rankings from stored rules or provided usage/value columns; monitor lot-controlled and dated inventory (FEFO/FIFO per shop rule) to flag blanks, mixed lots, and near/past expiry; review slow-moving or dead stock from last-movement dates while keeping consignment and kit components distinct.
6. **Replenishment (reorder) & returns (RMA)** — Flag SKUs at or below the shop's min / reorder point using on-hand and on-order columns, converting Buy vs Sell UOMs only via item-master pack factors and noting vendor MOQs/price breaks for the buyer without placing POs. Log customer returns against RMA numbers with condition (`good`, `damaged`, `unknown`) and explicit sellable status before any unit returns to good stock.

Sources used for orientation (not this shop's policy): ASCM/APICS inventory control & cycle-counting practice; Zenventory / Glyde / Obol / Cleverence distributor receiving, putaway, blind cycle-count, and RMA SOP patterns; SBA / IRS Pub 538 / OSHA warehousing / FDA FSMA public orientation pages cited in `facts/facts-operations.md`.

## This expert's phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the receipt/PO, count date, pick batch, transfer, RMA sheet, or reorder pull. Create or switch Work Item (`WID-XXXXXXXX`). Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; keep one warehouse/site and one receipt or count per Work Item unless asked for a combined pack. |
| 2. Intake source files | Drop stock CSVs, scanner exports, count sheets, PO PDFs, packing slips, or RMA forms into `in/`. Load `facts/MEMORY-INDEX.md` and operations facts/rules. Do not invent SKUs, POs, lots, bins, UOM conversions, or on-hand quantities. | Files in `in/` | Missing export/PDF, unclear UOM/pack factor, missing cutoff time, or conflicting item-master files → ask (`operator-qa` or chat). |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step per `continue` unless the operator asked for the whole named job. Read the named `docs/tools/` doc. Write the step's `produces` file under this Work Item. | `work/*.csv` (`open-po.csv`, `receiving.csv`, `putaway.csv`, `picks.csv`, `count-raw.csv`, `count-variance.csv`, `stock.csv`, `lots.csv`, `movement.csv`, `rmas.csv`, `transfers.csv`, `abc-input.csv`) | Do not start a step whose `needs` file is missing. Do not pass a chat summary in place of a file. |
| 4. Check the step | Run the map's `check` command against this Work Item's paths (`file-exists.py`, `csv-has-columns.py`). Retry at most 3 times on failure, then ask. Save check output under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check failure is never a silent pass. Operator approves any new check command before use. |
| 5. Pack | Write the finished match sheet, variance report, pick list, or worksheet to `out/*.md` quoting filenames, cutoff times, UOMs, and exception flags. Update the journal via `journal-keeper`. | `out/*.md` plus supporting `work/*.csv` | Operator reviews and acts on the pack (investigates shorts, orders recounts, approves book adjustments, places POs, or processes RMAs). This expert never posts adjustments or sends orders/funds. |
| 6. Close | Mark the Work Item `done` when every map step has passed its check (or has a documented exception). Optionally capture or promote durable shop learnings. | Journal completion, `STATUS.md`, optional `remember` / `promote-facts-rules` | Shop-wide rules or facts are persisted only after operator confirmation. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer to an open question and not approval of a human gate.

## Which registered workflows cover which phases

| Stockroom cycle slice | Workflow | Registry id |
| --- | --- | --- |
| Match PO vs packing slip vs dock count; flag shorts/overs/damage | Receiving Match | `receiving-match` (default) |
| Assign received lines to bins from receiver notes, bin map, or master | Putaway List | `putaway-list` |
| Build pick list from order export and on-hand/available; flag shorts | Pick Pack | `pick-pack` |
| List inter-site moves with from/to site, SKU, qty, UOM, transfer number | Transfer | `transfer` |
| Compare count CSV to book on-hand; list variances and recount flags | Cycle Count | `cycle-count` |
| Rank SKUs into ABC classes from stored rules or value/movement column | ABC Class | `abc-class` |
| Track lot/batch IDs and expiry dates; flag blanks and near/past expiry | Lot Expiry | `lot-expiry` |
| Flag slow-moving stock from last-movement/sale dates and quantity | Dead Stock | `dead-stock` |
| List SKUs at or below min/ROP from stock export with UOM/pack notes | Reorder | `reorder` |
| Log customer returns by RMA, condition, and explicit sellable status | RMA Returns | `rma-returns` |

Cross-cutting constraints (consignment/owner codes, quarantine holds, blind count sheets, transaction freeze cutoffs, catch-weight, hazmat flags, cold-chain locations, kit/BOM handling, and vendor SKU cross-references) live in the shared pair (`facts/facts-shared.md`, `facts/rules-shared.md`) and the operations pair (`facts/facts-operations.md`, `facts/rules-operations.md`) and apply across all registered workflows. If the operator names a new recurring stockroom job, add a workflow file and registry entry via `define-role` or `promote-facts-rules`.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, must-never list, ask when shop procedure is missing, label starter guesses, resolve conflicting notes) live in `MyRole.txt`, `.cursor/rules/expert.mdc`, and `facts/rules-operations.md`—not in separate process-glue skills.

## Assumptions

- This seed is a **wholesale / inventory role** working from CSV exports, spreadsheets, scanner files, and PDFs—not a live WMS, customs broker, hazmat shipper, or accounting/AP role.
- The ten registered workflows in `.cursor/workflows/workflow-registry.json` cover the full recurring wholesale stockroom cycle; `receiving-match` is the default workflow.
- Step checks remain lightweight Python CSV/file checks (`docs/tools/checks/`) that the operator can refine as they teach this shop's exact export column names.
