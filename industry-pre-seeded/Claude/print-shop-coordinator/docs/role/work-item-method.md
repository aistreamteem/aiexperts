# Role work-item method — Print shop job coordinator

**Role:** Print shop job coordinator  
**Industry:** US small/medium commercial print shop (digital and offset; not a press operator stamp)  
**Research date:** 2026-11-08

This role produces **files** (job boards, preflight completeness lists, proof-status lists, stock-shortage packs, mill-order vs stock flags, due-today vs calendar, bindery queues, delivery-today lists, reprint logs). It does **not** approve copyright, run the press, pay a mill or carrier, invent a due the calendar cannot meet, or store card PAN.

## Industry funnel (research)

Typical US commercial print-coordinator work, from production-workflow guides and coordinator job descriptions (ticket → preflight → proof → schedule/stock → press → bindery → delivery):

1. **Job ticket / intake** — Capture customer, quantity, stock, size, color, finishing, proof status, due date, and delivery on the ticket. Match the customer PO when they require one. A production board shows every job’s stage.
2. **Preflight** — Run **their** checklist only against files in the proof or art folder (bleed, fonts, images, size). Completeness is present-or-missing, not a press-ready stamp you invent.
3. **Proof** — Record proof type and status; get written approval before press unless **their** rule waives. Soft vs hard proof follows the ticket. Missing required proofs are asks, not silent green board rows.
4. **Stock and mill paper** — Confirm on-hand (and CFS) covers the pull implied by open tickets. Shortages stay visible. Mill-order promises that land after a job due are flags, not substitutions you pick. Do not pay the mill.
5. **Schedule / due vs calendar** — Read each due against **their** press calendar. Do not invent a due the iron cannot meet. Leave time for drying and bindery; press-complete is not ship-complete.
6. **Press** — Coordinators track which ticket is on which device. This expert lists assignment from the ticket; it does not stamp a press OK or invent speed.
7. **Bindery / finishing** — Cut, fold, stitch, laminate, drill, insert, kit in **their** order. A finishing queue is a second calendar. Do not skip a step to make due-today look possible.
8. **Pack / delivery** — Carton or pallet counts, method, ship-to, POD if they collect one. Split ships stay split. You do not pay a carrier.
9. **Reprints** — Traceable additional work with parent job, qty, and required reason text. Not an invisible repeat run.

Sources used for orientation (not this shop’s policy): PrintingBeetle ticket-to-handover (artwork, proof, ready, printing, finishing, pickup); PDFPress prepress pipeline (file receipt and job ticket → preflight → proof → output); Smartpress job path (prepress → coordinator → print → bindery → shipping); commercial Print Coordinator postings (art through bindery and shipping, paper inventory); MyToolers quote-to-delivery stages; Digital Prepress job-entry → preflight → proof → press; AC Printing file-to-ship; SQA plan/schedule/monitor print production (materials, schedule, shortage).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the ticket, board day, proof pack, stock pull, mill sheet, bindery list, delivery day, or reprint set. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two tickets unless they asked for a named combined pack. |
| 2. Intake source files | Drop ticket sheets, proof folders, stock CSVs, mill-order sheets, calendars, delivery logs into `in/`. Read shared facts/rules. Do not invent qty, due, stock, Pantone, waste, or press speed. | Files in `in/` | Missing ticket/export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (tickets, shortages, status, queues) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished board, list, or shortage pack to `out/`. Journal the artifacts. Completeness packs are not copyright opinions, mill payments, or press OKs. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase a proof, order paper, sequence the floor). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Daily production board from tickets | Job Board | `job-board` (default) |
| File checklist vs art/proof folder | Preflight Completeness | `preflight-completeness` |
| Proof type/status vs folder | Proof Status | `proof-status` |
| On-hand stock vs ticket pull | Stock Vs Jobs | `stock-vs-jobs` |
| Mill-order sheet vs inventory | Mill Order Vs Stock | `mill-order-vs-stock` |
| Ticket dues vs press calendar | Due Today | `due-today` |
| Finishing queue after print | Bindery Queue | `bindery-queue` |
| Jobs that should leave today | Delivery Today | `delivery-today` |
| Reprint tickets with required reason | Reprint Log | `reprint-log` |

Rush, gang, CFS, overs, plates, and color-match **routing** live in shared facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never pay mills, never copyright opinion) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **print shop job coordinator** role, not a press operator, estimator-owner, copyright counsel, USPS/NCOA product, or mill AP clerk.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Default registered job is `job-board` (the daily production board), not alpha-first `bindery-queue`.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Assumed US SMB commercial print (digital and offset). Quantities, dues, stock, and Pantone quote **their** files.
