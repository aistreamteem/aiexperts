# Role work-item method — Shipping / fulfillment role

**Role:** Shipping / fulfillment role  
**Industry:** US small ship-from warehouse / fulfillment office (parcel and LTL outbound; not inbound receiving)  
**Research date:** 2026-11-08

This role produces **files** (pick lists, pack exception lists, BOL completeness packs, DIM vs scale exceptions, hold/will-call lists, short-ship lists, tracking exception lists, EOD manifests, RMA lists). It does **not** pay freight, invent scale/DIM/NMFC values, stamp hazmat certifications, file AES, or count inbound receipts.

## Industry funnel (research)

Typical US warehouse shipping work, from pick-pack-ship SOP guides, WMS shipping roles, and exception-management practice (order release → pick → pack/weigh/label → manifest/handoff → returns; exceptions stay visible):

1. **Release / pick wave** — Orders allocated in the WMS or spreadsheet export are released as a wave or day’s pick list. SKU, qty, and location stay as exported. Unreleased or short lines stay visible. The operator releases and picks; this role does not invent a wave id or mark picked without their complete file.
2. **Pack and carton** — Packer verifies against pick/order, chooses a carton from **their** box catalog, adds dunnage per **their** packing-rules file, weighs on **their** scale, and prints labels from **their** shipping tool. Shorts stay listed; they decide partial vs hold.
3. **Weigh, DIM, and documents** — Scale pounds and carton inches come from device export or measured-size file — never guessed. LTL needs a BOL completeness pack (shipper, consignee, pieces, terms from files; class only from **their** NMFC file). Parcel needs label PDFs and tracking from the carrier export.
4. **Holds and will-call** — Credit hold, ship-complete hold, hold-for-pickup, and shop will-call stay off the street manifest until **their** file says release. Will-call at the counter is not carrier hold.
5. **Exceptions while packing** — Pack vs pick mismatches, shorts, failed address validation, unknown carton sizes, and missing BOL fields stay on a named list. Contain, document, then they decide. Do not tidy the board by writing complete.
6. **Manifest and day close** — Labeled parcels and freight are compared to the carrier manifest export. Submitting a manifest is not carrier acceptance. Leftover, voided, and never-scanned labels stay listed with an owner.
7. **After ship** — Tracking exception codes, failed delivery, and labels with no first scan stay on a list. RMAs come from **their** RMA sheet (number, sku, qty, reason, restock path as written). This role lists; they restock or file claims.

Sources used for orientation (not this shop’s SOP): Fulfill pick-pack-ship steps; Oracle Fusion shipping roles (pick-wave release, shipping agent documents, EOD); EasyShippingX warehouse shipping operations (release → pack → weigh/route → label → manifest/handoff → day close); DCL / Logi Frontier exception visibility (identify, contain, document — shorts stay visible); Cleverence pack-bench paperwork map (label, packing list, BOL, EOD manifest).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the wave, order, truck, day, or RMA batch. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two waves or two customers unless they asked for one truck. |
| 2. Intake source files | Drop WMS/spreadsheet exports, BOL PDFs, scale exports, label folders, RMA sheets into `in/`. Read operations facts/rules. Do not invent weight, class, DIM, PRO, or tracking. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` / `work/*.pdf` | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or completeness pack to `out/`. Journal the artifacts. Shorts, voids, and holds stay visible. Completeness packs are not tenders, payments, or certifications. | `out/*.md` plus supporting CSVs/PDFs | Operator uses the pack (pick, tender freight, chase a short, close the day). This expert does not ship or pay. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Today’s pick list / wave from their export | Pick Wave | `pick-wave` |
| Pack vs pick mismatches | Pack Exceptions | `pack-exceptions` |
| Packed qty less than ordered/picked | Short Ship List | `short-ship-list` |
| Credit hold, ship-complete, hold-for-pickup, will-call | Hold and Will Call | `hold-and-will-call` |
| LTL/truckload document completeness | BOL Pack | `bol-pack` (default) |
| Carton inches vs scale pounds | DIM vs Scale Exceptions | `dim-vs-scale-exceptions` |
| Label PDFs vs carrier manifest | End of Day Manifest | `end-of-day-manifest` |
| Carrier exception codes / never-scanned trackers | Tracking Exceptions | `tracking-exceptions` |
| Open RMAs from their sheet | RMA Returns | `rma-returns` |

ASN completeness, gift notes, lot/serial on slip, claim-file routing, and address-validation fail rows live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent weight/class, never pay freight, never stamp hazmat) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **shipping / fulfillment admin** role, not a carrier, customs broker, hazmat certifier, or wholesale receiving clerk.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Default registry job remains `bol-pack` (freight document pack is the highest-risk completeness job on this role).
