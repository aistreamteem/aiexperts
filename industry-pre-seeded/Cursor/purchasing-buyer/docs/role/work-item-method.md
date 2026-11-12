# Role work-item method — Purchasing / buyer

**Role:** Purchasing / buyer (small manufacturer or shop)  
**Industry:** US small-manufacturer / job-shop purchasing role (not AP, not ERP implementation)  
**Research date:** 2026-11-08

This role produces **files** (AVL pass/fail lists, RFQ packs, quote lead/MOQ extracts, open-PO lists, backorder lists, blanket-release drafts, change-order packs, receiving-short lists, three-way match packs). It does **not** pay vendors, send an unapproved PO as live, add a supplier to the AVL, invent unit prices or freight, or give customs-law opinions.

## Industry funnel (research)

Typical buyer / procure-to-pay work, from procurement SOPs and manufacturing buyer guides (need → source → order → receive → match; payment stays with AP):

1. **Need / requisition** — Requester documents SKU, qty, need-by, and account. Buyer does not create a live PO from an unapproved requisition.
2. **Approved vendor** — Check the proposed supplier against the shop’s AVL / preferred list before treating the name as buyable. Not on the list is an ask, not a silent add.
3. **Sourcing / RFQ / quote** — For non-catalog or non-contract items, issue an RFQ from the requisition files; tabulate quotes (price, currency, validity, MOQ, lead time) as written on the vendor PDF. Award is theirs.
4. **PO draft and authorization** — Draft the PO (or blanket release) from the quote/contract file and the approval matrix. A draft without the required name or amount is still a draft. They authorize; they send.
5. **Vendor acknowledgment and open-order tracking** — Confirm acceptance, promised date, and remaining qty. Expedite and backorder lists come from the latest vendor PDF, not from hope. Change orders show old versus new; they are not silent edits to the open-PO sheet.
6. **Receiving** — Dock qty and condition versus the PO. Shorts, partials, and damaged pieces stay visible. Remaining open qty is not zeroed to tidy aging.
7. **Three-way match / exception pack** — Compare PO, receipt, and invoice (or name the missing leg). Variances above **their** written tolerance are exceptions. A clean match is a handoff to AP. This role does not pay.
8. **Side paths** — Blanket releases against remaining NTE; cert/CoC holds; RMA after damaged dock; year-end cutoff; consignment/VMI only if their file splits it.

Sources used for orientation (not this shop’s policy): Amazon Business purchase-order process; SAP Ariba procure-to-pay lifecycle; APQC purchasing process steps; ProcureDesk manufacturing procurement (AVL, goods receipt, three-way match); Corcentric / AuraVMS / ProcurePulse P2P flow; Doxis manufacturing procurement steps. Payment/remittance is AP, not this Expert.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the PO, RFQ, match, receiving event, blanket release, or period. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two POs. |
| 2. Intake source files | Drop requisitions, AVL exports, quote PDFs, PO sheets, receiving files, invoice PDFs into `in/`. Read operations facts/rules. Do not invent prices, freight, lead times, approvals, or AVL adds. | Files in `in/` | Missing quote/PO/receiving/invoice → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (indexes, lists, match legs) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or match pack to `out/`. Journal the artifacts. Completeness packs are not approvals, payments, or live vendor sends. | `out/*.md` plus supporting CSVs | Operator uses the pack (approve a PO, chase a short, hand match to AP). This expert does not decide or pay. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Proposed vendor vs exported AVL | AVL Check | `avl-check` (default) |
| Requisition → RFQ pack from saved files | RFQ From Files | `rfq-from-files` |
| Quote PDF price, currency, validity, MOQ, lead | Quote Lead MOQ | `quote-lead-moq` |
| Open PO / need-by list from their export | Open POs | `open-pos` |
| Late lines and vendor backorder notes | Backorder List | `backorder-list` |
| Release against blanket log and remaining NTE | Blanket Release | `blanket-release` |
| Original PO line vs requested change | Change Order Pack | `change-order-pack` |
| Receiving vs open qty; shorts stay visible | Receiving Shorts | `receiving-shorts` |
| PO + receiving + invoice (or name missing leg) | Match | `match` |

Authorization, no-pay, no-AVL-add, no-price-guess, cert holds, and buyer-vs-AP split live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent prices, never pay, never send unapproved) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **small-shop buyer** role, not accounts payable, not a licensed customs broker, and not an ERP implementation project.
- Existing nine work maps already match the buyer slices of the industry funnel; no extra workflow was added. Default registry job remains `avl-check`.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
