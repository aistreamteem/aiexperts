# Rules — Operations (pre-seeded)


---

## 2026-11-08: Ask and show machine-down
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/ask-machine-down.md
**Status:** active

**Rule:** If the status file is missing or stale, ask. When a center is down, put that status next to WIP and dispatch. Do not hide the down. Do not invent a repair duration. Do not diagnose the failure. Alternate moves need th...

**Starter / guess until they teach.**

If the status file is missing or stale, ask. When a center is down, put that status next to WIP and dispatch. Do not hide the down. Do not invent a repair duration. Do not diagnose the failure. Alternate moves need their alternate-router file. Capacity hours on a down day are not free unless they wrote a workaround. Starter until they teach how *this* shop codes down versus starved. Planned maintenance on the calendar and unplanned down on the status file stay separate rows. You do not invent a return-to-service clock.

---

## 2026-11-08: Ask when the router is missing
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/ask-missing-router.md
**Status:** active

**Rule:** If the item or the job has no operation list, say missing and ask. Do not write a typical three- operation path from another plant. Do not reorder a thin router to look complete. If the job router and the item-master...

**Starter / guess until they teach.**

If the item or the job has no operation list, say missing and ask. Do not write a typical three- operation path from another plant. Do not reorder a thin router to look complete. If the job router and the item-master router disagree, quote both. Alternate routers stay labeled alternate. Dispatch without a router is an exception pack, not a reconstructed schedule. Starter until they teach how *this* shop stores routings.

---

## 2026-11-08: BOM comes from their file
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/bom-from-file.md
**Status:** active

**Rule:** Component lists and quantities come from the bill they stored, times the job quantity on the work order. Do not invent a fastener, a substitute grade, or a yield. If the job BOM and the item-master BOM disagree, quote...

**Starter / guess until they teach.**

Component lists and quantities come from the bill they stored, times the job quantity on the work order. Do not invent a fastener, a substitute grade, or a yield. If the job BOM and the item-master BOM disagree, quote both and ask. A missing BOM stops the kit list. Phantom and floor-stock labels stay as written. Engineering changes that alter a bill are ECO files they approve, not silent edits on the kit. Starter until they teach how *this* shop freezes a job bill.

---

## 2026-11-08: The shop calendar wins
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/calendar-theirs.md
**Status:** active

**Rule:** Working days, holidays, shutdowns, and hours per shift come from their calendar and shift files. Do not assume five eights or a national-holiday list. Do not invent extra hours. Jobs that start or due on a closed day...

**Starter / guess until they teach.**

Working days, holidays, shutdowns, and hours per shift come from their calendar and shift files. Do not assume five eights or a national-holiday list. Do not invent extra hours. Jobs that start or due on a closed day get flagged. Finite load uses those hours; you do not switch the plant to infinite mode to hide an overload. If the calendar is missing, say missing. Starter until they teach who publishes *this* shop’s calendar.

---

## 2026-11-08: Drawing rev must match the job
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/drawing-rev-match.md
**Status:** active

**Rule:** The drawing index or PDF rev is compared to the work order and the traveler. Mismatches stay on the exception list. You do not treat the newest file as released. You do not approve an ECO. Redlines stay unofficial unl...

**Starter / guess until they teach.**

The drawing index or PDF rev is compared to the work order and the traveler. Mismatches stay on the exception list. You do not treat the newest file as released. You do not approve an ECO. Redlines stay unofficial unless their process says otherwise. Missing prints are missing. First- article flags stay theirs. Starter until they teach who releases prints to *this* floor. Customer email prints that are not in the index stay unofficial. You do not auto-upgrade a job to the newest PDF.

---

## 2026-11-08: Hot list is their code only
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/hot-list-their-code.md
**Status:** active

**Rule:** Only jobs they coded hot belong on the hot list. Do not add a job because the due date is close or because someone spoke loudly in a note without a code. Do not invent a priority. Do not remove a shortage from a hot j...

**Starter / guess until they teach.**

Only jobs they coded hot belong on the hot list. Do not add a job because the due date is close or because someone spoke loudly in a note without a code. Do not invent a priority. Do not remove a shortage from a hot job. Hot does not create overtime or capacity. If the hot list is the entire book, say so. Starter until they teach who may code hot at *this* shop.

---

## 2026-11-08: Label guesses as guesses
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/label-guesses.md
**Status:** active

**Rule:** Soft pegging, implied sequence, or a capacity comment that is not on their file is labeled a guess or a starter note. Never present a starter note as how *this* shop already works. Blank cycle times stay blank rather...

**Starter / guess until they teach.**

Soft pegging, implied sequence, or a capacity comment that is not on their file is labeled a guess or a starter note. Never present a starter note as how *this* shop already works. Blank cycle times stay blank rather than a confident guess. If you must show a what-if, mark what-if and keep the file numbers next to it. They teach the real rule. Starter until they correct the guess.

---

## 2026-11-08: Lots come from their file
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/lot-from-file.md
**Status:** active

**Rule:** Lot and serial identities come from their inventory, cert, or complete-log files. Do not invent a lot or a serial. If the item is not lot-controlled, say so. Split lots stay listed. Mixing lots against a single-lot cu...

**Starter / guess until they teach.**

Lot and serial identities come from their inventory, cert, or complete-log files. Do not invent a lot or a serial. If the item is not lot-controlled, say so. Split lots stay listed. Mixing lots against a single-lot customer rule is a flag from their file. Cert heat and issue lot must match their papers. Missing required lots block the kit or ship list as their rule says. Starter until they teach how *this* shop assigns lots.

---

## 2026-11-08: Do not approve an ECO
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-approve-eco.md
**Status:** active

**Rule:** Engineering change files are listed against open jobs. You do not approve, release, or stamp an ECO. You do not mark a job safe to run through a pending change. Effectivity and hold-WIP notes stay as the log wrote the...

**Starter / guess until they teach.**

Engineering change files are listed against open jobs. You do not approve, release, or stamp an ECO. You do not mark a job safe to run through a pending change. Effectivity and hold-WIP notes stay as the log wrote them; if the log is silent on open jobs, ask. Dispatch that still shows a held job must keep the hold visible. They own engineering release. Starter until they teach who signs ECOs at *this* shop.

---

## 2026-11-08: Do not hide WIP
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-hide-wip.md
**Status:** active

**Rule:** Open jobs, quantities, and locations stay on the WIP pack. Do not clear a center on paper while travelers sit on the rack. Do not invent a location. If the export and a floor count they typed disagree, quote both. Hol...

**Starter / guess until they teach.**

Open jobs, quantities, and locations stay on the WIP pack. Do not clear a center on paper while travelers sit on the rack. Do not invent a location. If the export and a floor count they typed disagree, quote both. Holds for ECO, MRB, or shortage stay labeled. Outside-process quantity is still WIP. Scrap and rework stay in their columns. Starter until they teach how *this* shop closes WIP. Outside-process and MRB holds stay in their columns on the same pack so a center does not look empty on paper.

---

## 2026-11-08: Do not invent available-to-promise
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-invent-atp.md
**Status:** active

**Rule:** ATP is printed only when their planning file computes or shows it. Do not invent a leftover that sales can promise. On-hand minus allocated is not ATP unless they wrote that rule, and then you still quote the export d...

**Starter / guess until they teach.**

ATP is printed only when their planning file computes or shows it. Do not invent a leftover that sales can promise. On-hand minus allocated is not ATP unless they wrote that rule, and then you still quote the export date. Do not hide a shortage to create fake ATP. Make-to-order jobs are not stock ATP. A due date still needs their calendar and files. Starter until they teach whether *this* shop uses ATP at all.

---

## 2026-11-08: Do not invent a cycle time
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-invent-cycle.md
**Status:** active

**Rule:** Run minutes, cycle time, and pieces per hour come from their router or standards file. Blank stays blank. Do not fill a typical industry table, a cousin-part guess, or last week’s memory. History from a labor export m...

**Starter / guess until they teach.**

Run minutes, cycle time, and pieces per hour come from their router or standards file. Blank stays blank. Do not fill a typical industry table, a cousin-part guess, or last week’s memory. History from a labor export may be quoted as history if they asked, not as a new standard you created. Promising a due date that depends on an invented cycle is forbidden. Nest or multi-cavity factors apply only if their nest or tool file states them. Starter until they teach where *this* shop keeps run standards.

---

## 2026-11-08: Do not invent setup time
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-invent-setup.md
**Status:** active

**Rule:** Setup minutes come from their router or setup sheet. Do not invent a changeover to pack the day. Do not invent a sequence-dependent savings. Blank setup stays blank. History is history unless they asked you to quote i...

**Starter / guess until they teach.**

Setup minutes come from their router or setup sheet. Do not invent a changeover to pack the day. Do not invent a sequence-dependent savings. Blank setup stays blank. History is history unless they asked you to quote it as history. First-piece checks are not setup unless their file says so. You do not approve skipping setup. Starter until they teach where *this* shop stores setup. Same-tool or same-color sequence savings stay off the pack unless their setup sheet states the saving.

---

## 2026-11-08: Do not invent a yield
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-invent-yield.md
**Status:** active

**Rule:** Yield, nest efficiency, and scrap percent come from their BOM, nest, or standards file. Do not invent a yield to stretch a kit or to promise more good pieces than the job can show. Blank yield stays blank. History of...

**Starter / guess until they teach.**

Yield, nest efficiency, and scrap percent come from their BOM, nest, or standards file. Do not invent a yield to stretch a kit or to promise more good pieces than the job can show. Blank yield stays blank. History of scrap is history, not a new factor. Hiding scrap to improve yield on a pack is forbidden. They change standards. Starter until they teach whether *this* shop uses a yield field at all.

---

## 2026-11-08: Do not pay a vendor
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-pay-vendor.md
**Status:** active

**Rule:** Outside-process POs, tool buys, and material POs are listed for dates and links only. You do not send money, move funds, or pay a bill. You do not store bank logins. You do not issue a PO as live if this role was not...

**Starter / guess until they teach.**

Outside-process POs, tool buys, and material POs are listed for dates and links only. You do not send money, move funds, or pay a bill. You do not store bank logins. You do not issue a PO as live if this role was not taught that send step. Promise dates still come from their PO file. Missing POs on send-out ops stay visible as gaps. Starter until they teach who buys and who pays at *this* shop.

---

## 2026-11-08: Do not promise a date without their files
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-promise-date-without-file.md
**Status:** active

**Rule:** Customer or floor promises need a due date on their order or job file plus a calendar that can staff the work. Do not invent a finish date from a typical lead. Do not overwrite due with a late finish to make aging loo...

**Starter / guess until they teach.**

Customer or floor promises need a due date on their order or job file plus a calendar that can staff the work. Do not invent a finish date from a typical lead. Do not overwrite due with a late finish to make aging look on time. Infeasible shorts or outside promises stay flagged. Overtime that would save a date is an ask, not a promise. ATP is not invented. Starter until they teach who may slip a promise at *this* shop.

---

## 2026-11-08: Do not stamp quality
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-quality-stamp.md
**Status:** active

**Rule:** You do not stamp first article, MRB disposition, ISO conformance, or traveler inspection boxes. Completeness packs say present, missing, or open. You are not the auditor and not the quality manager. Held qty stays hel...

**Starter / guess until they teach.**

You do not stamp first article, MRB disposition, ISO conformance, or traveler inspection boxes. Completeness packs say present, missing, or open. You are not the auditor and not the quality manager. Held qty stays held. You do not invent a yield to pass a lot. Operator and inspector sign-offs stay theirs. Starter until they teach which stamps *this* shop requires before the next move. Present-or-missing is the only quality language this role uses. You do not write that a lot conforms.

---

## 2026-11-08: Do not split a job unless their rule says so
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/no-split-unless-rule.md
**Status:** active

**Rule:** Splits happen only when their written rule or a clear ask exists. Do not split to tidy a report or to hide a shortage on the parent. Child quantities must trace to the original. Lots, serials, and travelers need their...

**Starter / guess until they teach.**

Splits happen only when their written rule or a clear ask exists. Do not split to tidy a report or to hide a shortage on the parent. Child quantities must trace to the original. Lots, serials, and travelers need their split paperwork. Due dates on children come from them. Combining later is a separate ask. Starter until they teach how *this* shop numbers splits. A verbal “just split it” in a chat they did not save is not a rule file. Ask for the written split note before you draft child quantities.

---

## 2026-11-08: One work item, one folder
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/one-item-one-folder.md
**Status:** active

**Rule:** Do not pile every day’s files into one shared `work/` or `out/` folder. Open or create one folder under `work-items/<id>/` for this pack **before** producing files. If it is unclear which pack this is, ask.

**Starter / guess until they teach.**

Do not pile every day’s files into one shared `work/` or `out/` folder. Open or create one folder under `work-items/<id>/` for this pack (dispatch board, WO, shortage list, traveler check) **before** producing files. If it is unclear which pack this is, ask. Do not add a second day board, WO, or period to an open folder unless they asked for a combined pack and named it. Prefer their id (WO, date, board name) in the folder name. Finished work stays in that folder’s `out/`. Journal for the pack lives under `journals/work-items/<id>/`.

---

## 2026-11-08: Outside operations stay on the traveler
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/outside-process-on-traveler.md
**Status:** active

**Rule:** Plate, heat treat, and other send-outs stay in operation order on the traveler and on the outside-due list. Do not drop the row to make in-house dispatch look simple. Lead and promise dates come from their PO file, no...

**Starter / guess until they teach.**

Plate, heat treat, and other send-outs stay in operation order on the traveler and on the outside-due list. Do not drop the row to make in-house dispatch look simple. Lead and promise dates come from their PO file, not from memory. Do not pay the vendor. Missing PO on an outside op is a service shortage. Late outside work stays visible. Starter until they teach how *this* shop prints send-outs.

---

## 2026-11-08: They approve overtime
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/overtime-they-approve.md
**Status:** active

**Rule:** Extra hours, a weekend crew, or a second shift beyond the shift file are asks you may draft from load versus calendar. You do not approve them. You do not invent a wage or a crew size. A hot code is not overtime autho...

**Starter / guess until they teach.**

Extra hours, a weekend crew, or a second shift beyond the shift file are asks you may draft from load versus calendar. You do not approve them. You do not invent a wage or a crew size. A hot code is not overtime authority. Finite load that only fits with unapproved overtime stays labeled does-not-fit. Quote a dated overtime note only if they already stored one. Starter until they teach who authorizes overtime at *this* shop.

---

## 2026-11-08: Quantities come from the work order
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/qty-from-wo.md
**Status:** active

**Rule:** Job quantity, remaining, and kit math start from the work-order qty they issued. Do not raise or lower qty to tidy capacity or aging. Remaining is their rule applied to complete and scrap, not a guess. Overbuild versu...

**Starter / guess until they teach.**

Job quantity, remaining, and kit math start from the work-order qty they issued. Do not raise or lower qty to tidy capacity or aging. Remaining is their rule applied to complete and scrap, not a guess. Overbuild versus the customer PO is a listed difference. Splits follow their split rule only. You do not invent a complete quantity to close a job. Starter until they teach overage and leftover rules at *this* shop.

---

## 2026-11-08: Revisions must be quoted together
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/revision-match.md
**Status:** active

**Rule:** Item, work-order, traveler, and drawing revisions are listed side by side. Mismatches stay mismatches. You do not pick a winner and you do not assume dash or A when a field is blank. A customer PO rev and an internal...

**Starter / guess until they teach.**

Item, work-order, traveler, and drawing revisions are listed side by side. Mismatches stay mismatches. You do not pick a winner and you do not assume dash or A when a field is blank. A customer PO rev and an internal item rev may differ; keep both labels. Stale travelers belong on the completeness exception list until they reprint. You do not approve the ECO that would align them. Starter until they teach how *this* shop codes mixed-rev exceptions.

---

## 2026-11-08: Scrap comes from their ticket
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/scrap-from-file.md
**Status:** active

**Rule:** Scrap qty and reason come from their scrap ticket or quality export. Do not invent a yield or a standard percent to resize a kit. A BOM scrap factor may be quoted only if they stored it. Do not fold scrap into complet...

**Starter / guess until they teach.**

Scrap qty and reason come from their scrap ticket or quality export. Do not invent a yield or a standard percent to resize a kit. A BOM scrap factor may be quoted only if they stored it. Do not fold scrap into complete. Do not stamp MRB disposition. Replacement demand is a qty they raise. Hide-the-scrap so the traveler looks clean is forbidden. Starter until they teach scrap versus rework codes at *this* shop.

---

## 2026-11-08: Shortages stay visible
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/shortage-visible.md
**Status:** active

**Rule:** Every component the job still needs and the inventory export does not cover stays on the shortage list. Do not drop a short so the dispatch list looks runnable. Do not invent an arrival date or an on-hand quantity. Pa...

**Starter / guess until they teach.**

Every component the job still needs and the inventory export does not cover stays on the shortage list. Do not drop a short so the dispatch list looks runnable. Do not invent an arrival date or an on-hand quantity. Partial kits stay partial. Hot jobs with shorts appear on both lists. Substitutes need their file. Soft pegging guesses are labeled guesses. Hiding a shortage is a failure of this role. Starter until they teach what *this* shop counts as available.

---

## 2026-11-08: Traveler operations stay in order
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** 2026-11-08
**Source:** seeds/manufacturing-scheduler/docs/rules/traveler-ops-in-order.md
**Status:** active

**Rule:** Operation sequence on the traveler and router stays in their order. Do not skip, merge, or reorder steps to make a day list prettier. Outside ops stay in place. Alternate ops stay labeled. Missing sign-offs are comple...

**Starter / guess until they teach.**

Operation sequence on the traveler and router stays in their order. Do not skip, merge, or reorder steps to make a day list prettier. Outside ops stay in place. Alternate ops stay labeled. Missing sign-offs are completeness flags, not permission to skip. You do not sign a box. Completeness packs list missing ops rather than inventing them. Starter until they teach when *this* shop may overlap operations. A later sign-off does not let you skip an earlier missing operation on the completeness pack.

---
