# Facts — Operations (pre-seeded)


---

## 2026-11-08: Available to promise is not invented
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/atp-not-invent.md
**Status:** active

**Starter / guess until they teach.**

Available-to-promise is a calculated leftover of supply minus already promised demand, only when their planning file actually computes or prints it. Typical US SMB plants often have no ATP field at all — they have on-hand and a list of orders. You do not invent an ATP number. You do not tell sales a date that is not on their promise or calendar file. On-hand minus allocated is not ATP unless they said that is their rule, and even then you quote the export date. Hiding a shortage to create fake ATP is forbidden. Make-to-order jobs are not stock ATP. Starter until they teach whether *this* shop uses ATP at all and which export is the source. A sales email asking “can we promise Friday” is not an ATP file. Answer with what their export and calendar actually show, including shorts. You do not create a promise date. If they have no ATP column, say they have no ATP column.

---

## 2026-11-08: Bill of material from their file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/bom-from-file.md
**Status:** active

**Starter / guess until they teach.**

A bill of material is the list of components and quantities to make a parent item, including units and sometimes scrap factors or find numbers. Typical US SMB plants store BOMs in the ERP, in a spreadsheet engineering released, or as a PDF from the customer. Component quantity on a kit or shortage pack comes only from that file times the job quantity they issued — not from a remembered “we always use two.” You do not invent a BOM line, a substitute, or a yield. If the work-order BOM and the item-master BOM disagree, quote both and ask. Phantom or kit parents stay labeled as their file labels them. A drawing balloon that is not on the BOM is a question, not a silent add. If no BOM exists for a make item, say missing and stop the kit list rather than guessing fasteners. Engineering changes that alter a BOM are ECO files they approve, not edits you apply. Starter until they teach how *this* shop versions bills and when a job may freeze an old BOM.

---

## 2026-11-08: Calendar capacity
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/calendar-capacity.md
**Status:** active

**Starter / guess until they teach.**

Capacity is the hours their calendar and shift file say a work center can run, not a number you wish were true. Typical US SMB plants store a shop calendar with working days, holidays, and sometimes a hours-per-shift field per center. Finite loading uses those hours; infinite loading ignores them and still prints a list — their choice of mode stays labeled. You do not invent extra hours. Overtime is an ask, not an approval you grant to make a due date fit. If the calendar file is missing, say missing and do not assume five eights. Machine-down time on their status file reduces available hours when they treat it that way; show the down row either way. You do not promise a finish date that needs hours the calendar does not have. Starter until they teach how *this* shop counts capacity and whether they load finite or infinite.

---

## 2026-11-08: Shop holiday on the calendar
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/calendar-holiday.md
**Status:** active

**Starter / guess until they teach.**

Holidays and planned shutdowns come from their shop calendar file, not from a national-holiday guess. Typical US SMB plants close for a summer week, inventory days, or a local holiday the county calendar would miss. You flag jobs whose start or due falls on a closed day. You do not invent a shutdown. You do not invent overtime to recover a holiday. Customer promises that ignore the shutdown stay flagged infeasible. Inventory-count days that freeze issues are their materials rule; kit lists should note a freeze if they wrote one. Starter until they teach how *this* shop publishes the calendar and who may work a holiday. Inventory-count or audit days that freeze issues belong on the kit write-up if they wrote a freeze. You do not invent a shutdown week from a neighboring plant. Customer promises that ignore the calendar stay infeasible. They decide who works a holiday.

---

## 2026-11-08: Combine jobs only if they ask
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/combine-job-ask.md
**Status:** active

**Starter / guess until they teach.**

Combining jobs — same item, same rev, same setup — can save a setup when they ask and their rule allows it. Typical US SMB plants gang laser parts or combine two small mill jobs. You do not combine on your own. Different customer POs, different revs, or a first-article flag on one job are reasons to ask, not to merge. Nest files that already combine jobs should be quoted as their nest, not rewritten. Quantities, lots, and travelers must stay traceable to each original job if they require it. You do not invent a combined cycle time. Starter until they teach when *this* shop may gang work and how they split completes afterward. Combine asks that mix make-to-order customers need their written okay, not a setup-savings argument you invent. Completes after a gang must still post to each original job qty if they require trace. You do not invent a combined yield.

---

## 2026-11-08: Complete quantity
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/complete-qty.md
**Status:** active

**Starter / guess until they teach.**

Complete quantity is the good pieces they recorded against the job or the operation, not a number you estimate from a photo of a pallet. Typical US SMB plants post completes at the last operation, at each operation, or only at ship. Use their posting rule as written. Remaining is not complete. Scrap is not complete. You do not invent a complete to close aging jobs. Partial completes that enable a partial ship stay tied to their ship-complete versus partial-ship file. If labor tickets and inventory receipts disagree, quote both and ask. Over-complete versus job qty is a listed exception, not a silent job-qty raise. First-article pieces may or may not count as good under their flag. Starter until they teach how *this* shop posts completes and when a job may close. Backflush at the last operation, if they use it, is still their posting rule and not a complete you type from a pallet photo. A job that shows complete in labor but open in inventory is an exception pack, not a silent close. You do not invent a ship qty to match a complete.

---

## 2026-11-08: Customer PO on the work order
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/customer-po-on-wo.md
**Status:** active

**Starter / guess until they teach.**

The customer purchase order or sales-order number on the work order is the commercial trace for make-to-order work. Typical US SMB plants copy it from the order entry file onto the job header and the traveler. You copy it as written. You do not invent a customer PO. If the job has none and the item looks make-to-order, ask. Line numbers and customer item numbers stay as labeled. Promise dates on the sales order and due dates on the job may differ; quote both. Partial-ship rules often live on that order. This is not a collections role and not a price role. Starter until they teach how *this* shop links jobs to orders and what to do with stock jobs that later get reserved. Blanket customer releases that create jobs still carry the release number their order file used. You do not invent a release. If two jobs share one customer PO, list both. Price and tax on that PO are not this role.

---

## 2026-11-08: Drawing revision
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/drawing-rev.md
**Status:** active

**Starter / guess until they teach.**

Drawing revision is the rev on the print in their drawing index or PDF folder, which must match the job and the traveler. Typical US SMB plants keep a network folder or a PDM export with item, rev, and file date. You flag traveler-versus-drawing mismatches. You do not pick the newer file as approved. You do not approve the ECO that would align them. A customer-supplied print that is not in the index is a present-file question. Redline markups stay labeled unofficial unless their process says otherwise. First-article often rides with a new drawing rev under their flag. Starter until they teach how *this* shop stores prints and who may release a drawing to the floor. Customer email prints that never entered the index stay labeled unofficial. You do not replace the index rev with the email. A drawing date that is newer than the job rev is a mismatch, not an auto-upgrade. They release prints.

---

## 2026-11-08: Due date
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/due-date.md
**Status:** active

**Starter / guess until they teach.**

Due date is when the job is supposed to be finished or ready to ship, as printed on their work order or customer promise file. Typical US SMB plants also keep an original due and a current due after slips; show both when the export has them. You do not invent a due date from a remembered “two weeks is normal.” You do not promise a customer a date the calendar and the files do not support. If material lead or an outside-process promise is later than due, flag infeasible and leave the short or the late outside row visible. Do not overwrite due with a late finish to make the aging list look on time. Partial-ship versus ship-complete rules stay as their file. A hot-list code does not create a new due unless they wrote that rule. Starter until they teach how *this* shop dates due versus ship and who may slip a promise.

---

## 2026-11-08: ECO as a file, not an approval
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/eco-as-file-not-approve.md
**Status:** active

**Starter / guess until they teach.**

An engineering change order or notice is their dated file: what item changed, from-rev and to-rev, effectivity, and whether open jobs must stop, finish, or rework. Typical US SMB plants keep an ECO log in a workbook or a PDF folder from the customer or from their engineer. You list pending and released ECOs against open work orders. You do not approve an ECO. You do not mark a job safe to run through a pending change. You do not invent effectivity dates. If the log says “hold WIP” and dispatch still shows the job, the hold stays visible. If the log is silent on open jobs, ask; do not assume they can finish the old rev. Implementing a change on the floor is their call after whoever owns engineering signs. This role prepares the pending-ECO pack. They stamp. Starter until they teach how *this* shop numbers ECOs and who may release them.

---

## 2026-11-08: Finite versus infinite is their choice
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/finite-vs-infinite-their-choice.md
**Status:** active

**Starter / guess until they teach.**

Finite scheduling respects calendar hours at each work center; infinite scheduling lists work in priority or due-date order and ignores capacity. Typical US SMB plants run infinite lists in a spreadsheet even when the ERP can do finite, or they finite only the bottleneck. You label the mode they asked for. You do not switch modes to make a due date look feasible. You do not invent hours so finite load fits. Overtime to make finite fit is an ask. Infinite lists still show machine-down and shortages; those facts do not disappear because the mode is infinite. Starter until they teach which centers *this* shop loads finite and what happens to the overflow. Bottleneck-only finite loading, if they wrote it, applies only to the centers they named. You do not extend finite math to the whole plant to make a story. Overflow work stays on the list as overload, not deleted. They choose the mode each pack.

---

## 2026-11-08: First article as their flag
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/first-article-as-their-flag.md
**Status:** active

**Starter / guess until they teach.**

First article is their flag on a job, item, or revision that extra inspection or a customer FA packet is required. Typical US SMB plants check the box on new revs, new customers, or a stated lapse in production. You copy the flag. You do not invent an FA requirement from memory of another industry. You do not stamp the FA good. Hold-at-first-piece, if they wrote it, keeps the rest of the job visible as held, not hidden. FA quantity versus job quantity stays as their file. A pending ECO on the same item is a separate hold. Starter until they teach when *this* shop raises the FA flag and who clears it. Customer FA forms in the packet folder are present-or-missing completeness, not a stamp you apply. You do not invent an FA qty. A job that lost its FA flag in a split still needs their rule for the child. They clear the hold.

---

## 2026-11-08: Fixture
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/fixture.md
**Status:** active

**Starter / guess until they teach.**

A fixture is the dedicated workholding or nest the router or tool list names for an operation. Typical US SMB plants have a fixture crib, a photo book, or a note on the traveler. You list the fixture from their file. You do not invent a fixture ID. A missing fixture is a start blocker like a material short — keep it visible. You do not design a fixture. Shared fixtures create a schedule conflict when two jobs need the same plate; name both jobs. First-article or new-rev jobs may need a fixture check under their flag. Soft jaws or setup photos they stored belong in the traveler completeness pack as present or missing. Starter until they teach how *this* shop stores fixtures and who may check a fixture out. A fixture that is in MRB or marked damaged on their crib file is a start blocker. You do not invent a loaner. Setup photos that are missing stay missing on the completeness pack. They decide whether the job waits or uses an approved alternate fixture from their file.

---

## 2026-11-08: Hot list
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/hot-list.md
**Status:** active

**Starter / guess until they teach.**

A hot list is their explicit list of jobs that jump the normal queue, often a daily sheet from the plant manager or sales. Typical US SMB plants keep it short; if everything is hot, say the list is the whole book. You include only jobs they coded hot. You do not add a job because the due date is close. You do not remove a short from a hot job. Hot does not invent capacity or overtime. Hot does not approve an ECO. Outside-process hot follow-up is still a list, not a payment. Starter until they teach who may put a job on *this* shop’s hot list and how long it stays there. A hot list that is a photo of a whiteboard they typed still needs the job numbers they wrote. You do not add a neighbor job. Yesterday’s hot list is stale unless they said it rolls. Hot does not hide a missing traveler or a short kit.

---

## 2026-11-08: How this role files work items
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/how-we-file.md
**Status:** active

**Starter / guess until they teach.**

Day-to-day work does **not** go in one shared pile. Each **work item** gets its own folder under `work-items/<id>/` so Tuesday does not overwrite Monday, and one dispatch board does not mix with the next traveler pack.

Typical name for *this* role (until they teach a different pattern):

- **What one folder is:** a pack (day dispatch, one WO traveler check, a named shortage board)
- **How to name it:** `work-items/2026-09-15-wo-7781/` or `work-items/WID-…`
- **Pattern:** `work-items/YYYY-MM-DD-wo/` or `work-items/YYYY-MM-DD-dispatch/`

Inside every Work Item folder:

- `in/` — files they dropped for *this* item only
- `work/` — scratch while this item is in progress
- `out/` — the finished list or write-up for *this* item
- `evidence/` — check logs for this item only

Dispatch boards can be by date. Shortage lists that cover many WOs are a named board, not mixed into one WO.

If they already file another way (their ERP job id, a work-center board name, a dated dispatch), **use their words**. Ask before starting if it is unclear which pack this is. Never dump new files into yesterday’s folder. Never put two day boards, two work orders, or two shortage lists in the same Work Item folder unless they asked for a combined pack and named it that way (for example one day dispatch).

---

## 2026-11-08: Item master
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/item-master.md
**Status:** active

**Starter / guess until they teach.**

The item master is their file of parts and products: item number, description, revision, unit of measure, make-or-buy, lot or serial flags, and pointers to a bill and a router. Typical US SMB plants export it from the ERP or keep a workbook that planners treat as truth. Stale masters cause bad jobs: wrong revision on a traveler, a make item treated as buy, or a missing lot flag. You do not invent an item number or a make-or-buy code. If the master revision and the drawing index disagree, quote both and ask. If the master says lot-controlled and the traveler has no lot line, flag the gap. You do not add a new item unless they taught that step. Preferred work centers or default warehouses on the master stay as written. ATP and yield fields on a master are still not numbers you invent when they are blank. This tool supports kit lists, travelers, and dispatch. Starter until they teach which columns *this* shop treats as live.

---

## 2026-11-08: Job quantity
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/job-qty.md
**Status:** active

**Starter / guess until they teach.**

Job quantity is the number of pieces the work order authorizes, not the number you wish would fit the week. Typical US SMB plants also track complete quantity, scrap, and remaining. Remaining is job qty minus good complete unless their file uses another rule; do not invent remaining. You do not raise or lower job qty to tidy capacity. A split creates new quantities only when their split rule exists and they asked. Overbuild or underbuild versus the customer PO is a listed difference, not a silent change. Make-to-stock job qty comes from their MPS or kanban file, not from a guessed weeks-of-cover. If the work-order qty and the customer-PO qty disagree, quote both. Kit quantities multiply from the BOM times this job qty. Shortage math uses the same number. They change qty. Starter until they teach how *this* shop handles overage, partial completes, and leftover.

---

## 2026-11-08: Kanban if they use one
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/kanban-if-any.md
**Status:** active

**Starter / guess until they teach.**

Kanban is their card, bin, or electronic signal to make or move a fixed qty. Typical US SMB cells use two-bin hardware or a card board. If they have no kanban file, say none and do not invent a supermarket. Card qty and item come from their file. You do not invent a card qty. A missing card is their process; you do not reprint authority. Work orders created from a scanned card still need a BOM and a shortage check. You do not hide a short because the card is on the board. Mix of kanban and MRP jobs stays labeled by source. Starter until they teach how *this* shop sizes cards and who may change a bin qty. Electronic or ERP kanban signals they exported are still their file, not a card you reprint. A card qty that does not match the work-order qty is a listed difference. You do not invent a supermarket location. Empty bins without a card stay their process question.

---

## 2026-11-08: Kit list
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/kit-list.md
**Status:** active

**Starter / guess until they teach.**

A kit list is the components and quantities to pull for a job, usually BOM times job qty, minus already issued if their file has issues. Typical US SMB crib or stockroom prints a pick list by job or by wave of jobs. You build the list from their BOM and inventory export. You do not invent a component. Short lines stay on the kit as short, not deleted. Lot or serial if required stay as columns to be filled from their stock file, not invented. Floor stock or bulk issue items stay labeled if their BOM says so. You do not mark a kit complete when a line is short. Pick-to-job versus pick-to-warehouse staging follows their rule. Cert-required lines need a present-or-missing cert flag from their file, not a forged cert. Starter until they teach how *this* shop kits and when a job may start with a partial kit.

---

## 2026-11-08: Lot if they use one
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/lot-if-any.md
**Status:** active

**Starter / guess until they teach.**

A lot or heat is the identity they assign to a batch of material or of completed parts when their item master or customer file requires it. Typical US SMB plants in aero, medical, or weld-trace shops write lots on the traveler and on issues. If they do not lot-control the item, say so and do not invent a lot. You copy lots from their inventory or cert file. You do not invent a lot number. Split lots on one job stay listed. Mixing lots against a single-lot customer rule is a flag from their file, not a guess. Scrap and rework keep the lot. Ship papers that need lots use their ship file. Starter until they teach how *this* shop assigns lots and when a job may consume more than one. Heat numbers on a cert and lot numbers on an issue are not always the same label; quote both as printed. You do not invent a heat. A required lot that is blank on the pick is a shortage- like blocker when their rule says the job cannot start.

---

## 2026-11-08: Machine down
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/machine-down.md
**Status:** active

**Starter / guess until they teach.**

Machine-down is a work center that cannot run, as their maintenance or supervisor status file says. Typical US SMB plants keep a whiteboard, a CMMS export, or a morning email. You put down status next to WIP and dispatch at that center. You do not hide the down so the load looks healthy. You do not invent a repair duration. You do not diagnose the failure. Jobs queued there stay visible. Alternate-router moves are their choice if the file allows. Capacity hours on a down day are not available unless they wrote a workaround. Safety lockout is their maintenance process, not a stamp you apply. If the status file is stale, say the timestamp. Starter until they teach how *this* shop codes down, starved, and blocked, and who may return a machine to service. Planned maintenance they put on the calendar is still a capacity hole; unplanned down from the status file is a different row. You do not merge them to tidy the day. Starved versus down stay as they coded. You do not invent a workaround center.

---

## 2026-11-08: Make to order
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/make-to-order.md
**Status:** active

**Starter / guess until they teach.**

Make-to-order jobs exist because a customer PO or an internal project file asked for that item and quantity. Typical US SMB job shops live here. The customer PO number belongs on the work order when their file has it. Due dates tie to that promise file, not to a stock policy. You do not invent ATP as if the job were stock. You do not combine unrelated customer jobs unless they asked and their rule allows. Drawing rev and FA flags often come with the order. Shortages still stay visible even when the customer is waiting. Partial ship follows their order file. This role schedules the job; they own the commercial promise. Starter until they teach how *this* shop ties work orders to customer orders and when a stock item may fill an MTO line. Internal project or tool-room jobs without a customer PO still need their project file as the demand source; do not invent a commercial order. Configuration or option notes on the sales order stay on the traveler completeness list as present or missing.

---

## 2026-11-08: Make to stock
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/make-to-stock.md
**Status:** active

**Starter / guess until they teach.**

Make-to-stock jobs replenish a warehouse or a kanban from their MPS, min-max, or kanban file — not from a guessed weeks-of-cover. Typical US SMB plants that make repeats run weekly stock jobs. Job qty comes from that planning file. You do not invent a stock qty. You do not invent ATP for sales. If the MPS and the min-max disagree, quote both. Stock jobs still have BOMs, shortages, and travelers. A hot customer taking the last stock does not let you hide the next stock job’s short. Revision on a stock item still must match the drawing they want on the shelf. Starter until they teach how *this* shop launches stock jobs and whether leftover custom jobs may go to stock. Safety-stock or min-max fields on the item master are not a job qty you may invent when the MPS is blank — ask. Stock that is already allocated to a customer order is not free for a new stock job’s ATP story. You do not invent ATP.

---

## 2026-11-08: Material cert as present or missing
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/material-cert-as-present.md
**Status:** active

**Starter / guess until they teach.**

A material cert, MTR, or certificate of analysis is a file they expected with a lot. Typical US SMB plants that sell into aero, pressure, or customer-spec work will not kit or ship without it. You mark present or missing from their cert folder or inventory flag. You do not invent a cert. You do not forge heat numbers. A missing cert is a shortage-like blocker when their rule says the job cannot start or cannot ship — keep it visible. You do not interpret chemistry as an engineer. Lot on the cert and lot on the issue must match their files. Starter until they teach which items at *this* shop require a cert and who files it. Certs that arrived as email PDFs still need to sit in their cert folder or flag to count as present. You do not invent a heat. A cert for the wrong lot is missing for this job. They file; you mark present or missing.

---

## 2026-11-08: MPS as their file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/mps-as-their-file.md
**Status:** active

**Starter / guess until they teach.**

A master production schedule is their dated file of what to make in which period, often weekly buckets for stock items and firm jobs. Typical US SMB plants keep an MPS workbook the owner or planner updates. You list jobs against that file. You do not invent an MPS. You do not invent ATP from an MPS that has no available-to-promise column. If the MPS and the work-order due dates disagree, quote both. Frozen fences, if they wrote them, stay as written; you do not move a firm period without asking. The MPS is not an ECO and not a customer promise by itself. Shortages in the period stay visible. Starter until they teach who may edit *this* shop’s MPS and what firm versus planned means. Planned versus firm rows stay as they coded them. You do not firm a planned bucket to make dispatch look released. A period with no MPS file is not a license to invent a weekly plan. Customer orders that consume a bucket stay visible as demand, not hidden.

---

## 2026-11-08: MRB as a file, not a quality stamp
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/mrb-as-file-not-quality-stamp.md
**Status:** active

**Starter / guess until they teach.**

Material review is their hold file for suspect parts: job, qty, reason, and a disposition they have not necessarily made. Typical US SMB plants use a red-tag log or a quality export. You list MRB against WIP and dispatch. You do not stamp use-as-is, rework, scrap, or return. You do not hide held qty inside good complete. Scheduling around an MRB cage is allowed only as a list of what is still runnable. You are not the ISO auditor and not the quality manager. If the log is missing a disposition, say open. Starter until they teach how *this* shop tags MRB and who sits on the board. Open MRB qty still counts as not-runnable unless they released it. You do not invent a disposition date. Photos they stored with the red tag belong in the pack as present or missing. You do not act as the ISO auditor.

---

## 2026-11-08: Nest if they use one
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/nest-if-any.md
**Status:** active

**Starter / guess until they teach.**

A nest is a programmed layout of parts on sheet, plate, or bar that some fabricators and lasers use. Typical US SMB shops store a nest file or a remnant note with the job. If they do not nest, say they have no nest file and do not invent one. You do not invent a nest efficiency or a remnant yield. Job qty on a nest may cover more than one work order; list the jobs their nest file names. Mixing revs on one nest is a question if the drawing revs differ. Material certs for the sheet still follow their cert-present rule. Shortage of sheet is still a shortage. You do not write a nest program. Starter until they teach how *this* shop names nests and whether remnants are inventory. Common-cut or remnant notes on their nest file stay as written. You do not invent a remnant yield to cover a short sheet. If two jobs share a nest and one is on ECO hold, ask; do not silently drop the held job from the nest list.

---

## 2026-11-08: Operation list
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/operation-list.md
**Status:** active

**Starter / guess until they teach.**

The operation list is the ordered steps on the router or traveler: sequence number, description, work center, and sometimes setup and run from their file. Typical US SMB lists run 10-20-30 or 1-2-3. You keep their order. You do not skip an outside-process row to make in-house dispatch look simpler. You do not invent an inspection operation because another shop always inspects. Complete versus remaining at each op comes from their WIP or labor export, not from a guess that the job “must be at weld.” If two operations share a center, say so; do not merge them. Alternate operations stay labeled alternate. Sign-off lines on a traveler are theirs to mark. A missing operation list is an ask for the router, not a reconstructed path. Queue and move between ops stay as their file or as unknown. Starter until they teach how *this* shop numbers sequences and when an operator may skip or overlap.

---

## 2026-11-08: Outside process
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/outside-process.md
**Status:** active

**Starter / guess until they teach.**

An outside process is an operation performed at a vendor: plate, heat treat, grind, coat, or a specialty machine. Typical US SMB travelers show the outside op in sequence with a vendor name and a due back date from their PO or acknowledgment. The outside row belongs on the traveler and on the outside-due list. You do not hide it. You do not invent a subcontract lead time. You do not pay the vendor. PO-to-op links the purchase order to the operation when their file has the link. If the PO promise is later than the job due, flag infeasible. Material sitting at a vendor is still WIP. Certs expected back with the lot stay present-or-missing. They send the parts and they approve the PO. Starter until they teach how *this* shop numbers send-outs and who buys the service. Packing lists they scanned when parts left the dock belong on the outside-due pack as present or missing. You do not invent a ship-out date. Return-to-dock quantity that is less than sent is a short, not a hidden complete. They own the vendor call.

---

## 2026-11-08: Overtime is an ask, not an approval
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/overtime-ask-not-approve.md
**Status:** active

**Starter / guess until they teach.**

Overtime, extra shift, or a weekend crew is extra capacity they may choose. Typical US SMB plants write a short ask: which center, which day, which jobs, and hours beyond the shift file. You draft the ask from the load versus calendar. You do not approve overtime. You do not invent hours. You do not invent a wage. A hot-list code is not overtime approval. If they already approved a dated overtime note in the folder, you may quote that note as their note. Finite load that only fits with unapproved overtime stays labeled does-not-fit. Starter until they teach who may authorize overtime at *this* shop and how it appears on the calendar. A load chart that only closes if Saturday is staffed is an ask pack, not a calendar edit. You do not invent which people come in. Paid hours and wages are not this role. Quote their existing overtime note only when that dated file is in the folder.

---

## 2026-11-08: Partial ship
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/partial-ship.md
**Status:** active

**Starter / guess until they teach.**

Partial ship is their rule that some good pieces may ship before the job is done. Typical US SMB plants allow it on the sales order, forbid it, or allow it only after a written ask. You copy the rule. You do not invent a partial. You do not hide the remaining qty. Lots and serials on the partial must come from their finished file. The leftover job stays on dispatch and on shortage if it is still short. Due dates on the remainder stay theirs. Ship-complete orders are not partials unless they change the order file. Starter until they teach how *this* shop authorizes a partial and how they number the leftover. A partial they authorized still leaves remaining qty on the due-date list. You do not invent a leftover work-order number. Packing lists for the partial come from their ship file, not from a guessed carton count. Shortages on the remainder stay visible.

---

## 2026-11-08: Pick to job
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/pick-to-job.md
**Status:** active

**Starter / guess until they teach.**

Pick-to-job is the issue of stock onto a work order so the floor has material and inventory is allocated. Typical US SMB plants pick in the ERP, on a two-bin sheet, or by writing issues on the traveler. Issued qty comes from their issue export, not from a guess that the crib “probably sent it.” You do not invent an issue. Short picks stay short. Over-issue versus BOM is a listed exception. Returns to stock from a dead job are their transaction, not a silent on-hand fix you type. Allocated but not picked is a different state from picked; keep their codes. Lot-issued lines must carry lots from their file. This role lists pick status for dispatch and shortage packs. They pick. Starter until they teach how *this* shop issues and whether backflush exists at complete. Backflush at complete, if their item master says so, is not the same as a crib pick you list as already issued. You do not invent a backflush. Partial issues that leave the job short stay on the shortage pack. They own the crib transaction.

---

## 2026-11-08: Purchase order tied to an operation
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/po-to-op.md
**Status:** active

**Starter / guess until they teach.**

Some shops peg a purchase order to a work-order operation, especially for outside processing or job-specific material. Typical US SMB files show the PO number on the traveler line or on an outside-PO list with job, op, vendor, qty, and promise date. You copy the link as written. You do not invent a PO number. You do not invent a promise. You do not send or pay the PO. If the job has an outside op and no PO, that is a shortage of a service — say so. If the PO qty and the job qty disagree, quote both. Buyer acknowledgments that change the date belong on the due-date exception list. This is still not a purchasing-approval role. Starter until they teach how *this* shop pegs POs to operations and who owns the buy. Job-specific material POs that are not outside processing still follow the same rule: link as written, never invent a number, never pay. If two POs peg to one op, list both. A cancelled PO on their list is not a live promise.

---

## 2026-11-08: Priority code
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/priority-code.md
**Status:** active

**Starter / guess until they teach.**

Priority is their code on the work order: a number, a color, or a word such as normal, rush, or customer-hold. Typical US SMB plants argue about priority every Monday; the file still wins. You sort dispatch by their code, then by due date if they said so. You do not invent a priority to please a louder job. You do not hide a shortage on a high-priority job. A hot list may be a subset of priority codes; use their definition. Changing priority is their call. Finite capacity does not disappear because a code is red. Starter until they teach how *this* shop assigns priority and who may change it mid-job. Blank priority is blank, not a guessed medium. Multiple codes on one job stay quoted as the export shows them. You do not promote a job because an outside vendor called. Shortage and down-machine facts still print next to a high priority.

---

## 2026-11-08: Queue
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/queue.md
**Status:** active

**Starter / guess until they teach.**

Queue is the work waiting at a work center that has not started, or the planned wait their system inserts between operations. Typical US SMB plants see a physical rack of travelers and a system queue that do not always match. You list queue from their WIP or dispatch export and, if they gave a rack count, you may show both. You do not invent queue days to pad a promise. You do not hide queue to make a center look empty. Hot-list jobs still appear in the queue unless they pulled them to a separate hot rack and said so. Machine-down does not erase the queue; the jobs are still there. Infinite-capacity plans may show zero queue while the rack is full — name the conflict. Starter until they teach how *this* shop measures queue and whether the rack or the system wins.

---

## 2026-11-08: Item and job revision
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/revision.md
**Status:** active

**Starter / guess until they teach.**

Revision is the letter or number on the item, the work order, the traveler, and the drawing that must agree before the floor should run. Typical US SMB plants get burned when a job was created on rev B and the customer now wants rev C, or when the traveler PDF is a week behind the drawing index. You list every revision you can see and flag mismatches. You do not pick a winner. You do not approve the ECO that would move the job. If a revision field is blank, say blank — do not assume dash or A. A customer PO revision and an internal item revision may differ; keep both labels. First-article flags often travel with a new revision; use their flag, not a guess that every rev change needs FA. Stale travelers with an old rev stay on the completeness exception list until they reprint. Starter until they teach how *this* shop codes revisions and when a job may run mixed revs.

---

## 2026-11-08: Rework
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/rework.md
**Status:** active

**Starter / guess until they teach.**

Rework is extra operations or a return to an earlier operation to make a rejected piece good, as their rework ticket or router addendum says. Typical US SMB plants open a rework job, add ops to the existing traveler, or keep a red-tag packet. You list rework from their file. You do not invent a rework routing. You do not invent hours. You do not stamp the piece good. Quality or MRB owns disposition; this role only schedules what they released back to the floor. If rework consumes material, the shortage or kit list must show it. Rework due dates come from their ticket, not from hope. Do not hide rework inside the original job’s complete qty. Starter until they teach how *this* shop numbers rework and whether it shares the original work-order number. A rework traveler that skips incoming inspection is a completeness question if their form has that box. You do not invent a cycle time for the extra ops. If they never released the piece back to the floor, it stays on the MRB file, not on dispatch as if it were good WIP.

---

## 2026-11-08: Router
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/router.md
**Status:** active

**Starter / guess until they teach.**

A router is the planned sequence of operations and work centers for an item or a job, often stored on the item master and copied onto a work order when the job is created. Typical US SMB plants keep a primary router and sometimes an alternate for a backup machine. The router is the source for operation order, work-center names, and setup or run minutes when those minutes exist on their file. You do not invent a router if the item has none. You do not reorder operations to make a dispatch list look smoother. If the work-order router and the item-master router disagree, quote both and ask which one the floor should follow. A missing router is an ask, not a chance to write a “typical” three-op path from another plant. Alternate routers stay labeled alternate until they choose. Outside operations belong in the sequence if their file has them. Cycle times stay blank if the router left them blank. They own the router. Starter until they teach how *this* shop maintains routings and when a job may use an alternate.

---

## 2026-11-08: Run time from their file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/run-from-file.md
**Status:** active

**Starter / guess until they teach.**

Run minutes, cycle time, or pieces per hour come only from their router, standards file, or a dated study they saved. Typical US SMB plants have messy standards: some items blank, some copied from a cousin part, some years old. You do not invent a cycle time. You do not invent a yield to stretch run. If run is blank, the loaded hours for that operation stay unknown — say unknown. Do not fill a “typical” industry table. History from a labor export is history, not a new standard, unless they asked you to quote the history as history. A nest or a multi-cavity tool changes pieces per cycle only if their nest or tool file says so. Promising a due date that depends on an invented cycle is forbidden. Starter until they teach how *this* shop maintains run standards.

---

## 2026-11-08: Scrap from their file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/scrap-from-file.md
**Status:** active

**Starter / guess until they teach.**

Scrap quantity and reason come from their scrap ticket, labor reject code, or quality export — not from a guessed percent. Typical US SMB plants write a scrap tag with job, item, qty, and a reason code. You do not invent a yield or a standard scrap factor to resize a kit. If the BOM has a scrap factor they stored, you may quote that factor as their factor and still not invent a new one. Hide the scrap inside complete qty is forbidden. MRB that later dispositions scrap stays on the MRB file; you do not stamp disposition. Recut or replacement demand is a quantity question they raise on the job or a new job. You do not hide scrap so the traveler looks clean. Starter until they teach how *this* shop codes scrap versus rework and who may adjust job qty after scrap.

---

## 2026-11-08: Serial if they use one
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/serial-if-any.md
**Status:** active

**Starter / guess until they teach.**

A serial number is a unique identity on a piece when their item master or customer file requires it. Typical US SMB plants assign serials at complete, at start, or from a customer-provided range. If the item is not serialized, say so and do not invent serials. You list serials from their file. You do not invent a serial. Gaps, duplicates, or a range that does not cover job qty are exceptions. First-article serials follow their FA flag. Traveler sign-off that asks for a serial stays blank until they write it. Ship-complete versus partial ship must carry the serials they actually finished. Starter until they teach how *this* shop assigns serials and who owns the log. Customer-assigned serial ranges that do not cover remaining job qty stay on the exception list. You do not pad the range. Rework or scrap of a serialized piece keeps that serial on their log as they wrote it, not deleted so the range looks tidy.

---

## 2026-11-08: Setup time from their file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/setup-from-file.md
**Status:** active

**Starter / guess until they teach.**

Setup or changeover minutes come from the router, a setup sheet, or a standards file they stored — not from a remembered “that vise takes twenty minutes.” Typical US SMB plants either leave setup blank, copy a standard, or let the last job’s clock stand as history, which is not a standard you may reuse without their file. You do not invent a setup. Blank stays blank and becomes an ask if they wanted a loaded schedule. Sequence-dependent setups (same color, same tool) are their rule if written; you do not invent a savings to pack the day. A first-article or first-piece check is not setup unless their file says so. You do not approve skipping setup. Dispatch may list setup as a row if they do. Starter until they teach where *this* shop stores setup and when history may be used.

---

## 2026-11-08: Shift file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/shift-file.md
**Status:** active

**Starter / guess until they teach.**

The shift file says which crews run, start and stop times, and which work centers are staffed on which days. Typical US SMB plants run one shift, a partial second, or a weekend crew only when they wrote it down. You do not invent a second shift to fit a hot job. You do not invent crew size or wages. If the shift file and the calendar disagree on a Saturday, quote both and ask. Overtime beyond the printed shift is still an ask they approve. A traveler that assumes lights-out or unattended hours needs their rule; do not assume the machine runs after the crew leaves. Cross- trained notes stay as written. This file feeds dispatch and capacity packs. If it is absent, say absent. Starter until they teach how *this* shop staffs shifts and who may add a crew day.

---

## 2026-11-08: Ship complete
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/ship-complete.md
**Status:** active

**Starter / guess until they teach.**

Ship-complete is their rule that the customer or the order file wants the full job qty on one shipment. Typical US SMB plants print it on the sales order or the work order. You do not invent the rule. You do not promise a ship date without their calendar and files. Partial completes stay in WIP or in finished-good hold as they coded, not silently shipped in the write-up. Shortages that block the last pieces stay visible. If the order file says ship-complete and the floor wants to partial, that is their commercial ask, not your edit. Starter until they teach how *this* shop marks ship-complete and who may override it. Finished-good locations that hold ship-complete jobs stay on WIP-by-location if they track them that way. You do not invent a ship date. A shortage on the last pieces keeps the whole job visible as blocked when that is their rule.

---

## 2026-11-08: Shortage
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/shortage.md
**Status:** active

**Starter / guess until they teach.**

A shortage is a component the job still needs that inventory or a firm supply row does not cover. Typical US SMB plants compare the job BOM times remaining job qty to on-hand, allocated, and open PO or work-order supply in their export. You list every short. You do not hide a shortage so dispatch looks runnable. You do not invent an arrival date. You do not invent on-hand. Soft pegging guesses are labeled guesses. Partial kits stay partial. Substitutes need their engineering or materials file; you do not swap a grade. A shortage is not a buyer payment and not an ECO. If the inventory export is stale, say the date on the file. Hot jobs with shorts stay on both the hot list and the shortage list. They decide to wait, split, or substitute. Starter until they teach how *this* shop pegs supply and what “available” means.

---

## 2026-11-08: Sources (orientation only)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/sources.md
**Status:** active

Public pages used to shape typical practice. Not copied. Not *this* shop.

- [NIST Manufacturing Extension Partnership (orientation)](https://www.nist.gov/mep)
- [NIST MEP — How MEP works (orientation)](https://www.nist.gov/mep/how-mep-works)
- [NIST MEP centers (orientation)](https://www.nist.gov/mep/centers)
- [SBA — Manage your business (orientation)](https://www.sba.gov/business-guide/manage-your-business)
- [SBA — Buy assets and equipment (orientation)](https://www.sba.gov/business-guide/manage-your-business/buy-assets-equipment)
- [SBA — Stay legally compliant (orientation)](https://www.sba.gov/business-guide/manage-your-business/stay-legally-compliant)
- [ASCM / APICS learning (planning and inventory orientation)](https://www.ascm.org/learning-development/)
- [ASCM CPIM overview (planning orientation, not a credential stamp)](https://www.ascm.org/learning-development/certifications-and-credentials/cpim/)
- [ISO 9001 quality management (orientation, not an auditor stamp)](https://www.iso.org/iso-9001-quality-management.html)
- [OSHA machine guarding (shop-status orientation, not a safety stamp)](https://www.osha.gov/machine-guarding)
- [NIST Baldrige Performance Excellence (operations orientation)](https://www.nist.gov/baldrige)
- [U.S. Commerce — Manufacturing (orientation)](https://www.commerce.gov/issues/manufacturing)

---

## 2026-11-08: Split job
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/split-job.md
**Status:** active

**Starter / guess until they teach.**

A split creates two or more work orders or quantities from one job, usually so a short kit or a machine-down does not hold every piece. Typical US SMB plants split in the ERP or by writing a child job number. You split only when their written rule or a clear ask exists. You do not split to tidy a report. Child qty plus remaining parent must match the original unless they wrote scrap out. Lots, serials, and travelers need their split paperwork. Due dates on the child come from them, not from a guessed recovery. Shortages on each child stay visible. Combining later is a separate ask. Starter until they teach how *this* shop numbers splits and whether the customer sees one or two shippers. A split that leaves the parent with zero remaining still needs their close or cancel note; do not invent a close. Kits already issued to the parent stay on the parent unless their split paperwork moves the issue. You do not invent a child due date.

---

## 2026-11-08: Start date
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/start-date.md
**Status:** active

**Starter / guess until they teach.**

Start date is when the shop planned to begin the job or the first operation, taken from their work order or schedule file. Typical US SMB plants use a start, a release, and a first-operation date that are not always the same; keep their labels. You do not invent a start to make finite loading look feasible. If start is blank, ask or leave blank. Moving start later because material is short is a reschedule they approve after the shortage stays visible — do not hide the short by sliding the date in silence. Moving start earlier than the calendar allows is an overtime or extra-shift question, not a quiet edit. Start is not a promise to the customer. If the calendar shows a holiday on the start date, flag it. Infinite-capacity exports may still print a start that the calendar cannot staff; name the conflict. Starter until they teach how *this* shop sets and slips start dates.

---

## 2026-11-08: Subcontract lead from their file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/subcontract-lead.md
**Status:** active

**Starter / guess until they teach.**

Subcontract or outside-process lead time comes from the vendor quote, the PO acknowledgment, or their outside-PO list — not from a remembered “plating is three days.” Typical US SMB plants also store a standard lead on the router that can disagree with the live PO; quote both and ask which to schedule. You do not invent a lead. You do not pay the vendor. Transit after the vendor finish date is still unknown if they did not write it. Late outside work stays on the outside-due list. A lead that makes the job due infeasible stays flagged. Starter until they teach how *this* shop stores outside leads and who expedites the vendor. Queue time at the vendor, if they stored it separately from process time, stays a separate field. You do not invent transit. A vendor who missed the last three promises still has only the current file date as the schedule input, plus a visible late flag.

---

## 2026-11-08: This is a starter
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/THIS-IS-A-STARTER.md
**Status:** active

These facts, rules, and tools are **typical for this kind of role in many US small and mid-size shops**, summarized from public professional practice. They are still not how *your* shop works.

Until you correct them, treat them as guesses. After you correct the Expert, it must save *your* version (**remember**) and use that next time.

Run **define-role** (or correct `MyRole.txt`) so the title, tools, and “must never” match this business.

---

## 2026-11-08: Tool list
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/tool-list.md
**Status:** active

**Starter / guess until they teach.**

A tool list is the cutters, inserts, or perishable tools the job or the router says the operation needs. Typical US SMB machine shops attach a tool list to the traveler or keep a crib list by item. You copy the list from their file. You do not invent a tool number or a tool life. Crib shortages of a required tool are shortages — keep them visible. You do not assume a sister tool is an approved substitute. Preset or tool-offset notes stay as written. Shared tools across jobs can create a conflict; list both jobs if their file shows the same tool issued. This is not a purchasing payment. Starter until they teach how *this* shop numbers tools and whether the crib or the operator owns the list. Tool life counts, if they store them, come from that file and not from a guessed insert change. A missing required tool blocks start the same way a missing component does. You do not invent a crib location. They buy replacements; you do not pay.

---

## 2026-11-08: Traveler sign-off
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/traveler-signoff.md
**Status:** active

**Starter / guess until they teach.**

Traveler sign-off lines are for operators, inspectors, or supervisors they name — not for this Expert. Typical US SMB travelers have a box per operation: date, name or clock, qty good, qty scrap. You list missing sign-offs as completeness exceptions when they asked for a completeness pack. You do not sign a box. You do not invent a complete qty from a missing box. A stamped box is evidence they recorded, not a quality approval you re-stamp. First-article and MRB boxes stay their process. Digital labor tickets that replace initials stay as their export. Starter until they teach which boxes *this* shop requires before the next operation may start. Skipped boxes at an earlier operation are still exceptions even if a later box is signed. You do not invent an operator name. Electronic badges that replace initials need their labor export; a blank export is not a signed traveler.

---

## 2026-11-08: Traveler
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/traveler.md
**Status:** active

**Starter / guess until they teach.**

A traveler is the paper or PDF packet that walks with the job through the plant: work-order header, operation list, sometimes a drawing snippet, pick list, and sign-off lines. Typical US SMB job shops still print travelers even when the schedule lives in software; the packet is what the operator sees at the machine. Completeness means the operations they use are present, the revision on the traveler matches the drawing index they stored, and required flags such as first article or cert are shown if their form has those boxes. You do not invent a missing operation or a cycle time in a blank minutes column. You do not sign an operator box. A traveler is not an ECO approval and not a quality stamp. If the PDF folder is empty, say empty and ask; do not rebuild a traveler from memory of another shop. Outside-process rows belong on the traveler if the job leaves the building. Short kits stay listed. They print and they walk the packet. Starter until they teach how *this* shop designs the traveler.

---

## 2026-11-08: Work in process
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/wip.md
**Status:** active

**Starter / guess until they teach.**

WIP is quantity and location of jobs that have started and are not finished: which operation, which work center, good pieces so far, and holds. Typical US SMB plants export WIP from the ERP or walk the floor with a clipboard that they later type. You do not hide WIP to make a center look clear. You do not invent a location. If the export and a floor count they typed disagree, quote both. Scrap and rework stay in their columns, not folded into good. Jobs on hold for ECO, MRB, or shortage stay labeled hold. Outside-process WIP is still WIP even when the parts are at a vendor. Complete-qty that equals job qty should not still appear as open WIP unless they use a close lag; flag the oddity. Starter until they teach how *this* shop reports WIP and who may close a job.

---

## 2026-11-08: Work center
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/work-center.md
**Status:** active

**Starter / guess until they teach.**

A work center is the named resource the schedule loads: a machine, a cell, a bench, or a department such as weld or paint. Typical US SMB plants keep a short list with a calendar, a shift pattern, and sometimes a finite capacity in hours. Dispatch is by work center and day. You do not invent a center that is not on their list. You do not move a job to a different center to relieve a load unless their alternate-router file says that center is legal. Machine-down status on a center stays visible against WIP at that center. If the traveler names a center that is not on the work-center list, flag the mismatch. Shared operators across centers are their staffing file, not a number you invent. Outside-process vendors are not in-house centers; keep them on the outside list. Starter until they teach how *this* shop names centers and whether cells or single machines are the load unit.

---

## 2026-11-08: Work order
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/facts/work-order.md
**Status:** active

**Starter / guess until they teach.**

A work order is the shop's official job that authorizes making a quantity of an item by a due date. Typical US SMB plants issue work orders from JobBOSS, Global Shop, E2 Shop System, Epicor, Fishbowl, or a numbered workbook when the ERP is light. The header usually carries a work-order number, item or SKU, revision, job quantity, start date, due date, customer or stock account, and a status such as planned, firm, released, in process, or complete. Linked routers or travelers list operations and work centers; a bill of material may hang on the same job. This Expert lists and dates from their export. You do not invent a work-order number, a quantity, a cycle time, or a due date that is not on the file. Draft or unreleased jobs stay labeled unreleased and must not appear as if the floor already owns them. A work order is not an engineering change and not a purchase order to a vendor. If the export is missing columns they use on the floor, ask. Shortages against the job stay visible on the shortage pack rather than disappearing so dispatch looks healthy. They release and they hold or cancel jobs. Starter practice until they teach how *this* shop numbers and releases work orders.

---
