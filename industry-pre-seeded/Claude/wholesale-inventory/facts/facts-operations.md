# Facts — Operations (pre-seeded)


---

## 2026-11-08: ABC class
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/abc.md
**Status:** active

**Starter / guess until they teach.**

ABC class is a common ranking by annual usage value, hits, or movement so A items get more counts or tighter recount tolerances. Thresholds are theirs, or a worksheet they asked for from a sales or issue file they provided. Typical teaching uses a Pareto-style split (for example a small share of SKUs as A), but you do not invent the cut points or the annual demand. Do not relabel a class because a SKU feels important or a salesperson asked for special treatment. Class is not a quality grade, a safety rating, or an FDA status. If they already store class on the master, copy it; do not recompute unless they asked and gave the value column. Missing value or movement: ask. You do not use ABC to call stock worthless. Starter notes are orientation; their class field wins. Count frequency suggestions, if they want them, quote their rule, not a textbook calendar you chose.

---

## 2026-11-08: Accuracy as they define it
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/accuracy-kpi.md
**Status:** active

**Starter / guess until they teach.**

Inventory record accuracy is usually right lines over lines counted, or a unit-based or dollar-based rule they named. Compute only when both book and count are present for the same SKU, site, and cutoff. Do not invent a ninety-nine percent target as their standard. Do not compare to an industry benchmark as if it were their goal. Typical US SMB reports also show lines within tolerance, not only exact matches, if they set a threshold. Quote the formula you used and the cutoff. Mixed UOMs must be aligned first. Exclude or separately list holds, consignment, and in-transit if they said those are out of the KPI. You do not change book quantities to improve the percent. A short sample is a short sample; do not present ten SKUs as the warehouse accuracy. Their definition wins; starter notes are orientation. If only one of book or count exists, say accuracy cannot be computed yet. Do not borrow last quarter's percent to fill a pack that has no compare file.

---

## 2026-11-08: Adjustment authority
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/adjustment-auth.md
**Status:** active

**Starter / guess until they teach.**

Book changes need a name, a reason they already use (damage, found, shrink, data fix, count), and often a second approver above a dollar or unit limit. You do not approve write-offs. You do not silently fix the book to match a count. Typical US SMB distributors keep adjustment authority with a warehouse lead, owner, or controller; this Expert is not that person. A large variance without a recount note is a flag, not an auto-adjust. Reason codes come from their list; do not invent a cute code. Cost on an adjustment is their books file if present; you do not invent unit cost. Customer-owned and consignment stock may need the owner's approval language; do not write off someone else's inventory as house shrink. Expired or damaged goods still need their disposal or RTV process; you do not dump product. Starter notes describe common control; their authorization fields win.

---

## 2026-11-08: Allocation / reserve
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/allocation.md
**Status:** active

**Starter / guess until they teach.**

If they hard-allocate or reserve stock to an order, transfer, or will-call ticket, that quantity is not free for someone else. Use their allocation or reserve export and their column names. Typical small US wholesalers either allocate at order entry in a light system or keep a hold list in a spreadsheet. A verbal save me two is not a reserve until they put it in the file. Soft allocations in a salesperson's notebook do not change available in a pack you produce. Do not invent a reserve to protect a favorite customer. Do not release an allocation. If allocation plus pick plus available do not reconcile to on-hand, list the gap as a question; do not force the numbers. Customer-owned and consignment stock may be allocated only to the owner; do not treat it as house available. You do not promise fill from an allocation you created.

---

## 2026-11-08: Advance ship notice
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/asn.md
**Status:** active

**Starter / guess until they teach.**

An advance ship notice is an expected-receipt file some vendors send by EDI, email, or portal so the shop can stage a PO before the trailer arrives. Treat it as a plan: SKU, quantity, and sometimes lot or carton IDs the vendor says they shipped. Received quantity still comes from the dock count they recorded, not from the ASN. Typical small US wholesalers either ignore ASNs or use them only to print a receiving worksheet. Do not mark a PO received because an ASN arrived. Do not invent an ASN number. If the ASN and the packing slip disagree, list both and keep the dock count as the quantity column. An ASN is not a customs entry and not a CBP release. You do not pay from an ASN. If they do not use ASNs, say the folder had none and work from PO plus slip plus dock count.

---

## 2026-11-08: Available vs on hand
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/available.md
**Status:** active

**Starter / guess until they teach.**

Available-to-promise is not the same as on-hand in shops that reserve or hard-allocate stock to sales orders, will-call tickets, or transfers. Typical small US wholesale rooms subtract reserved, allocated, or quality-hold quantity from on-hand to get what a salesperson may still sell. Use their column names: available, ATP, free, reserved, allocated, or hold. Do not invent a reserve because a salesperson said in chat to save two cases. Soft allocations that live only in someone's head are not a file and must not change a pick or reorder pack. If they have no allocation export, say available was not in the folder and keep on-hand labeled as on-hand. Customer-owned or consignment stock is often on the floor but not available as house inventory; keep the owner flag. You do not promise a customer a fill from an available number you computed without their rule. Quarantine and damage locations are not available even if the unit is physically in the building.

---

## 2026-11-08: Backorder
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/backorder.md
**Status:** active

**Starter / guess until they teach.**

A backorder is open customer quantity they could not fill from available stock. List it from their order or backorder export: customer or order number, SKU, open quantity, UOM, and any date they stored. Do not promise a date. Do not cancel a customer line. Do not invent a backorder to explain a variance. Typical US SMB wholesalers keep backorders until a receipt lands or a buyer cancels with the customer; that decision is theirs. When a receipt comes in, you may list open backorders next to the SKU if they asked for a fill sequence, still without promising. Partial fills stay visible. Substitutes only if the order file names them. You do not change price or terms. In-transit purchase quantity is not a customer promise. If the backorder file is missing, say so; do not rebuild demand from memory.

---

## 2026-11-08: Barcodes
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/barcode.md
**Status:** active

**Starter / guess until they teach.**

Primary and alternate barcodes (UPC, EAN, GTIN, vendor case codes, internal license plates) live on the item master. A scan file from a count or receive is a source of quantity, not a license to create catalog numbers. Unknown barcode: do not create a SKU; list the code, the quantity scanned, and the location if present, and ask. Typical small US rooms mix each barcodes and case barcodes; convert only with their pack size. Do not type a guessed GTIN to make a line look complete. Duplicate barcodes on two SKUs are a flag. Missing barcode on a master is a data note, not a reason to skip a count they scheduled. You do not print labels as if you were their WMS administrator. Scanner admin PINs and system passwords never go in this folder. Their scan export is the count when they said they counted with a scanner.

---

## 2026-11-08: Location map
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/bin-map.md
**Status:** active

**Starter / guess until they teach.**

Aisle, rack, and shelf labels are theirs. You index counts, putaway lists, and exception lines to those labels. Typical US SMB maps are a spreadsheet, a printed diagram, or a simple zone list (bulk, pick face, cage, cooler, will-call). You do not redraw the warehouse as a new truth and you do not invent missing slots. If the count has bins and the map is not in the folder, say the map was missing. OSHA warehousing pages discuss clear aisles, safe stacking, and dock hazards as a site topic for their people; you do not redesign the racking, say a load is safe, or operate a lift. A map that conflicts with a live bin on a scanner export is a question, not a silent overwrite. One site map per site. You do not merge two buildings because the aisle letters look the same. Starter layout talk is orientation; their labels win.

---

## 2026-11-08: Bill of lading
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/bol.md
**Status:** active

**Starter / guess until they teach.**

A bill of lading proves a carrier pickup or delivery at trailer or shipment level. It may show carton or pallet counts, weight, and a PRO or tracking number. It often does not list every SKU. Use it for trailer, PRO, and appointment notes. Line quantity still comes from the packing list plus the dock count they recorded. A BOL is not a customs release and not a CBP clearance. Do not write that a shipment cleared. Typical small US wholesalers file the BOL PDF next to the PO. Missing BOL: say so if they asked for it; you may still match PO to pack list to dock count. You do not sign as the carrier. You do not operate the dock. OSHA warehousing pages discuss dock and trailer hazards as site safety; you do not run that scene. Seal numbers they wrote may be copied; you do not invent a seal.

---

## 2026-11-08: Case pack
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/case-pack.md
**Status:** active

**Starter / guess until they teach.**

Pack size belongs on the item master: eaches per inner, inners per case, cases per pallet if they store those levels. Typical US distributors change a pack when a vendor redesigns a carton; the dock is where the new pack is noticed, not where you silently average old and new. Sometimes twelve, sometimes twenty-four is a data error to flag, not a conversion you blend. Receiving should scan or write the pack they actually opened and the lot if they use lots. Do not change the master pack in a receiving file unless they asked you to draft that change for someone who owns the catalog. Inner packs that exist only on a vendor website are not their factor until the master says so. Pick lists that show cases must still respect on-hand in the UOM they count. Broken cases belong in a note; do not guess remaining eaches without their count. You do not restack a pallet on the floor.

---

## 2026-11-08: Catch weight
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/catch-weight.md
**Status:** active

**Starter / guess until they teach.**

Meat, cheese, produce, metal coil, cable, or other variable-weight items may use weight as the true quantity, sometimes with a piece count beside it. Use their weight column and their unit (pound, kilogram, foot). Do not convert a case to pounds without their factor on the master. Do not invent a catch-weight factor from a typical box. Typical US foodservice and metals distributors live on catch-weight; many general-line wholesalers never see it. If both pieces and pounds exist, keep both and say which one on-hand uses. Variance math must use the same unit as book. Lots and expiry often travel with catch-weight food; copy them, do not invent them. You do not certify a scale or a cold chain. You do not price by the pound. Missing weight on a catch-weight SKU is a flag, not a reason to type an average.

---

## 2026-11-08: Consignment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/consignment.md
**Status:** active

**Starter / guess until they teach.**

Vendor-owned or consignment stock sitting on this shop's floor is not always theirs to reorder, allocate, or value as house inventory. Label owner from their file (vendor, program name, or consignment flag). Do not add consignment into owned on-hand totals, available-to-sell house totals, or dead-stock value unless they said to. Typical US SMB programs include vendor-managed inventory at a customer, or vendor stock in a distributor cage. Reorder of consignment is often the vendor's problem or a special min they stored; do not treat it as a normal house ROP. You do not pay the vendor for a consignment draw. Count consignment on its own lines so a physical does not swallow it into house shrink. If the owner flag is missing but they said the program exists, ask; do not guess which SKUs are owned. Allocations of consignment stay with the owner program. You do not treat a cage walk as house available just because the units are on this floor.

---

## 2026-11-08: Blind count
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/count-blind.md
**Status:** active

**Starter / guess until they teach.**

Blind counts hide book or expected quantity so the person counting does not copy the system number. If they asked for a blind sheet, do not print expected quantity, book on-hand, or a suggested count on that sheet. After the count, compare in a second file that has both book and counted columns. Typical US cycle-count programs use blind for A items or for any recount. A scanner that shows system quantity is not blind; say so if they asked for blind. You do not fill a blank count from the book to finish faster. Counter name and date still belong on the blind sheet. Locations and SKUs may print; quantities to find do not. Variance and recount thresholds apply on the compare file, not as hints on the floor. Starter notes do not decide blind versus open; their instruction for this count wins.

---

## 2026-11-08: Who counted
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/count-team.md
**Status:** active

**Starter / guess until they teach.**

A typical count sheet has counter name, date, and sometimes a witness or second counter. Two-person or team counts if they require them for A items, high-dollar bins, or the year-end physical. You do not sign as a witness. You do not drop who counted when you build a variance file. Missing name: say so. Typical small US shops use warehouse staff, temps, or an owner on a weekend; copy the names they recorded. A scanner user ID is a name if that is all they have; label it as user ID. Blind sheets still carry names. Recounts should show a different person if their rule says so; you do not invent a second person. You do not accuse a named counter of shrink. Their SOP for who may count which zone wins; starter notes do not assign a crew.

---

## 2026-11-08: Cycle count
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/cycle-count.md
**Status:** active

**Starter / guess until they teach.**

Cycle counting is the common small-shop practice of counting a slice of SKUs or bins on a rolling calendar instead of waiting only for a year-end wall-to-wall. ASCM and APICS-style teaching often ties frequency to ABC class: A items more often, C items less, if they use class. Count what they scheduled. Do not skip a bin to save time. Do not print book quantity on a blind sheet if they asked for blind. Variance goes to a review queue with their recount threshold, not a silent book fix. Typical US distributors count from a scanner export or a paper sheet with counter name and date. You do not invent on-hand to close a hole. You do not post the adjustment unless their file shows who authorized it. One site per count unless they asked. Lost tag or unknown barcode: list it. You do not operate warehouse equipment to reach a high bay; you work the files they dropped.

---

## 2026-11-08: Damage location
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/damaged-location.md
**Status:** active

**Starter / guess until they teach.**

Unsellable, salvage, or return-to-vendor goods belong in a separate bin or status. Do not mix salvage into available or good on-hand. Return-to-vendor needs their vendor's RMA, not a hope that the vendor will take it. Typical US distributors park crushed cases, water damage, and open returns in a damage cage until a buyer or owner decides. Keep condition and reason if they stored them. You do not dump product, sign a waste manifest, or accuse a person. You do not release salvage to a picker. Count the damage location if they scheduled it, as its own lines. Cost and write-off authority are their books role. OSHA handling notes are site safety for them; you do not certify cleanup. If the damage location is missing from the map but appears on counts, say the map did not list it; do not invent a tidy code.

---

## 2026-11-08: Slow movers
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/dead.md
**Status:** active

**Starter / guess until they teach.**

Slow movers and excess are flags you raise only when their file has last-sale, last-issue, or last-movement dates, plus quantity. Days-on-hand or weeks-of-cover math needs both on-hand and a movement field they provided; do not invent velocity. Do not call stock worthless, scrap, or unsellable because it is slow. Excess versus min is a question for them: some shops keep deep stock on long-lead or seasonal items on purpose. Typical US distributors review dead lists with a buyer or owner before any return-to-vendor or markdown; you do not price a clearance or pay a restocking fee. Consignment and customer-owned lines stay labeled and out of house excess totals unless they said to include them. Kits and components can look dead when the kit sells; ask before you flag parts. Quote the date column you used. You do not dispose of product.

---

## 2026-11-08: Dock appointment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/dock-appointment.md
**Status:** active

**Starter / guess until they teach.**

Inbound windows they booked are calendar facts: carrier, PO if they stored it, door, and time. A missed window is a note on the receiving pack, not a customs event and not a CBP release. You do not clear a truck. You do not operate the dock, chock a wheel, or drive a lift. OSHA warehousing pages discuss dock and forklift hazards as site safety for their team. Typical small US shops either use a simple appointment sheet or take trucks as they arrive; copy what they have. Do not invent an appointment to make a late trailer look scheduled. An appointment is not a receipt. ASN plus appointment is still not dock quantity. You do not pay detention or schedule a carrier account. If they asked for a same-day receiving list, use the appointment file only as a plan next to open POs.

---

## 2026-11-08: Drop ship
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/drop-ship.md
**Status:** active

**Starter / guess until they teach.**

Drop-ship lines go from the vendor to the customer (or job site) and never hit this warehouse's on-hand. Keep them off the cycle-count file, the putaway list, and site on-hand totals. A drop-ship purchase order is still not a receipt into warehouse stock. Typical US wholesalers mix stocked lines and drop-ship lines on one customer order; split them in the pack so a picker is not sent to a bin that does not exist. You do not invent a warehouse receipt to make the PO look closed. You do not mark the line picked from house stock. Tracking numbers, if they stored them, may be copied; you do not promise a carrier date. Customs, importer-of-record, and international drop-ship paperwork are out of scope. If the order file does not say drop-ship, do not assume it; ask when ship-from is a vendor address.

---

## 2026-11-08: Expiry and FEFO
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/expiry.md
**Status:** active

**Starter / guess until they teach.**

Food, chemicals, medical, and other dated goods often carry expiry, best-by, or use-by dates on the lot line. Do not ignore those columns if they are in the file. FEFO (first expiry first out) is a common pick suggestion when they use dates; FIFO is also a costing story for their accountant and a pick story if they said FIFO. IRS inventory-method pages are tax orientation for their accountant, not a pick rule you invent. Pick suggestions follow their rule. Expired or near-expired: flag with the date they stored; do not dump product, do not sign a waste manifest, and do not decide FDA status. Blank expiry on a dated SKU is a flag. You do not certify a cold chain. You do not change a date that is unreadable; say unreadable. Typical small US shops that do not handle dated goods will have no such columns; do not invent dates.

---

## 2026-11-08: Transaction freeze
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/freeze-window.md
**Status:** active

**Starter / guess until they teach.**

A snapshot time matters. Write the cutoff they named on the count or receiving pack. Receipts, picks, and transfers after cutoff stay off that count unless they asked to fold them in with a clear label. Do not back-date a receive into a frozen count. Do not sneak a late scanner file into a closed physical. Typical US year-end counts freeze the dock for a morning or a weekend; cycle counts may freeze only a bin. If they did not name a cutoff, ask before you mix files from two days. In-transit and open POs are not on-hand at the freeze. You do not operate the dock during a freeze. You do not invent a cutoff to make two files look simultaneous. Quote date and time in the write-up. Their freeze instruction wins over a textbook physical script. A receiving file time-stamped after cutoff is a later snapshot, not a silent add to the frozen count. You do not reopen a closed physical to hide a truck that arrived late.

---

## 2026-11-08: Hazmat as a label on the master
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/hazmat-label.md
**Status:** active

**Starter / guess until they teach.**

If the item master flags hazmat, hazardous, or stores an SDS pointer, keep that flag on pick, receive, transfer, and putaway lists so their people see it. OSHA warehouse and hazard-communication orientation is about information available to workers on their site. You do not write an SDS, classify a material, pack a hazardous shipment, placard a truck, or act as a hazmat shipper or broker. You do not say a load is legal. Typical small US distributors of chemicals, aerosols, or batteries keep a simple flag and a binder of SDS files they already have; index what they stored. Missing SDS pointer: say so if they asked; do not invent a sheet. Quarantine and damage rules still apply. You do not dump chemical waste. Starter notes are not their shipping procedure. Their flag and their documents win. A pick list without the flag when the master has one is a miss to fix on the list, not a reason to classify the product yourself.

---

## 2026-11-08: How this role files work items
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/how-we-file.md
**Status:** active

**Starter / guess until they teach.**

Day-to-day work does **not** go in one shared pile. Each **work item** gets its own folder under `work-items/<id>/` so Tuesday does not overwrite Monday, and one receipt does not mix with the next.

Typical name for *this* role (until they teach a different pattern):

- **What one folder is:** count date, receipt, or transfer
- **How to name it:** `work-items/WID-20260915/` (or their PO/count id in the Work Item description)
- **Pattern:** `work-items/<id>/` with a label like `YYYY-MM-DD-receipt-or-count`

Inside every Work Item folder:

- `in/` — files they dropped for *this* item only
- `work/` — scratch while this item is in progress
- `out/` — the finished list or pack for *this* item
- `evidence/` — check logs for this item only
- Journals for the item live under `journals/work-items/<id>/`

Cycle counts are one folder per count. Do not mix two POs in one receiving folder unless they said it is one truck.

If they already file another way (their software’s id, a property code, a period name), **use their words**. Ask before starting if it is unclear which item this is. Never dump new files into yesterday’s folder. Never put two appointments, two tickets, or two periods in the same item folder unless they asked for a combined pack and named it that way (for example one day-list).

---

## 2026-11-08: In transit
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/in-transit.md
**Status:** active

**Starter / guess until they teach.**

In-transit or on-order quantity is open purchase-order or transfer quantity that has not landed in a counted location. It is not on-hand. Typical US SMB distributors track it from an open-PO export, a vendor acknowledgment, or a transfer-in-transit list between two buildings. Promised dates and ETAs are copied from the vendor PDF, the acknowledgment, or their cell in that file, not from memory or a usual two weeks. Do not add a truck you heard about on the dock or a container someone mentioned on the phone. A bill of lading that says a trailer left a port is still not a receipt into on-hand and is not a customs clearance. If they store in-transit as its own status, keep that status; do not fold it into available. When a PO is partially received, remaining open quantity stays in-transit until they close or cancel the line. You do not place the PO and you do not pay the vendor. Ask which file is the open-PO source before you put on-order next to a reorder suggestion.

---

## 2026-11-08: Item master
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/item-master.md
**Status:** active

**Starter / guess until they teach.**

The item master is the shop's locked list of what a SKU is allowed to be: description, base unit of measure, case or inner pack, barcodes, preferred vendor if they store one, min and max if they use them, and flags for lot, serial, catch-weight, hazmat, or kit. ASCM and APICS-style teaching treats the master as the place conversions are decided so receiving does not invent a pack size on the dock. Typical US SMB wholesalers export this from QuickBooks, a light WMS, or a spreadsheet that grew into the catalog. Fix pack size, UOM, and barcode on the master they exported, not in a one-off receiving guess. Missing barcode: say the code is absent; do not type a guessed GTIN or UPC. If two exports disagree on description or pack, quote both and ask which file is current. Do not add a SKU to the master to tidy an unknown scan. Starter field lists are orientation only; their column names and flags win. You do not redesign their catalog numbering scheme.

---

## 2026-11-08: Kits and bundles
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/kit.md
**Status:** active

**Starter / guess until they teach.**

A kit, bundle, or assembly SKU and its components are easy to double-count. Ask whether they stock the finished kit, the parts, or both, and which transaction they post when someone kits in the back. Do not explode a kit unless their bill of materials file is in the folder. Do not invent a BOM. Typical small US distributors sell assortments or convenience kits that are either pre-built (stock the kit) or pick-to-order (issue components). If both kit and parts sit on the floor, on-hand must say which. Cycle counts should not count the same physical piece as both kit and part. Light assembly labor is their shop process; you do not invent hours. Allocations may sit on the kit or on the parts; use their file. You do not promise a kit that would over-issue a component. If the BOM is missing, list the kit SKU as a question and leave components unexploded. Their kit flag on the master wins over a catalog that merely looks like a bundle.

---

## 2026-11-08: Light assembly / kitting
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/kitting-labor.md
**Status:** active

**Starter / guess until they teach.**

If they build kits, assortments, or light assemblies in the back room, component issues and kit receipts must both appear in their files or you will double-count or miss a hole. Ask which transaction they post (backflush, issue then receipt, or pick-to-order with no kit on-hand). You do not invent a bill of materials or a labor hour. Typical small US wholesalers kit promo packs or repair sets with a simple BOM spreadsheet. Count the floor the way they stock it. Do not explode a kit on a cycle count unless they asked and the BOM is in the folder. Allocations may sit on components; keep them. You do not promise a kit that over-issues a part. Labor cost is their books role. You do not stand at the bench as the builder. Starter notes do not design their kit process.

---

## 2026-11-08: Landed cost is a file, not customs clearance
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/landed-note.md
**Status:** active

**Starter / guess until they teach.**

If they store a freight, duty, or other landed-cost amount on a receipt for their books, copy the amount and the label they used. You do not calculate duty, classify HTS, apportion freight across lines unless their file already has that worksheet, or say a container cleared. CBP importer-of-record work, entry filing, and broker tasks are out of scope; point those questions to their broker. Typical US SMB distributors either ignore landed cost in the warehouse file or keep a simple freight-per-receipt number for the buyer. A bill of lading freight term is not a customs release. You do not pay the carrier or the broker. Missing landed cost is not a reason to skip a quantity flag on a short. IRS inventory-cost orientation is for their accountant, not a number you invent. Quote their receipt file; do not present a starter freight percent as this shop's burden rate.

---

## 2026-11-08: Lead time
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/lead-time.md
**Status:** active

**Starter / guess until they teach.**

Lead time is the days or weeks this shop expects between releasing a buy and having countable stock in the named location. Typical US wholesale files store vendor lead time, transit days, or a single combined number on the vendor or item record. Copy what they exported or what a dated vendor PDF says. Do not invent a factory lead time, an ocean transit, or a customs dwell. Usually two weeks in chat is not a file; ask them to save the number on the master or in a note they own. If the file splits production time and transit time, keep both. Lead time used in a reorder conversation must match the unit of their min math (days versus weeks). A promised date on one open PO is not a new standard lead time for the SKU. You do not promise a customer from a lead-time field. International shipping, importer-of-record work, and duty timing are out of scope; point those questions to their broker or buyer.

---

## 2026-11-08: Bin / location
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/location.md
**Status:** active

**Starter / guess until they teach.**

If they use bins, slots, or named floor locations, keep location on every count, putaway, and pick line. A SKU in two bins needs two lines or the split format they already use; do not collapse two bins into one tidy total. Ask for the location map or the export that lists valid bins. Do not invent a bin code to make a count sheet look complete. One warehouse or site per count file unless they asked for a multi-site pack with a site column on every row. Typical small US wholesalers use simple labels (A-12-C, bulk, will-call, cage) rather than a directed WMS. A missing location on a lot-controlled or serialized line is a flag. Transfers change location only with their transfer number and from-to pair. You do not walk the aisle with a pallet jack or choose a slot because it looks empty. OSHA warehouse orientation is about site safety; you do not certify a rack.

---

## 2026-11-08: Lots
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/lot.md
**Status:** active

**Starter / guess until they teach.**

If the item master says lot-controlled or batch-controlled, every receive, putaway, pick, transfer, return, and count line needs their lot or batch ID. FDA FSMA orientation for certain foods talks about extra traceability records; you copy lots they recorded, you do not invent a lot to complete a form, and you do not declare FSMA compliance or a recall. Mixed lots in one bin stay as split lines. Empty lot on a lot-controlled SKU is a flag. Typical US SMB rooms that are not food or chemical often skip lots; do not impose lot control because a textbook says to. Expiry or best-by, if present, stays with the lot. You do not dump expired product. You do not release a quality hold. A vendor lot and an internal lot, if both exist, stay in separate columns until they say which one picks. Starter notes are orientation; their lot file wins.

---

## 2026-11-08: Min / max
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/min-max.md
**Status:** active

**Starter / guess until they teach.**

Min is the trigger; max is often the target on-hand or the top of the replenishment band. Most US SMB wholesalers who do not run a full planning suite live on min-max or a simple reorder point with a max they typed years ago. Order-quantity suggestions, if they asked for them, are commonly max minus on-hand minus on-order, then rounded to their case pack or vendor MOQ using factors on the master. Use their min and their max. Do not override a max because a price break or a truckload looks attractive unless their file already has that buy rule. A max of zero or a blank max is a question, not a license to suggest a huge buy. Min above max is a data error to flag. You do not change mins after a single stockout story. Quote the export columns in the write-up so they can see you did not invent the band. Buyer placement and payment stay out of this role.

---

## 2026-11-08: Minimum order and price breaks
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/moq.md
**Status:** active

**Starter / guess until they teach.**

Vendor minimum order quantity, standard case buys, and price-break quantities come from the quote, contract, or vendor file they saved. Typical US SMB distributors buy some lines in eaches and others only in cases or layers. A price-break quantity is information to copy, not a reason to overload a dead or seasonal SKU. Let them decide whether to buy up to a break. If MOQ is missing, ask; do not guess a pallet quantity to make a reorder line look professional. Rounding a need up to MOQ should be listed as a choice with the unrounded need still visible. Case pack on the item master is the conversion; do not average two historical packs. You do not place the purchase order and you do not pay the vendor to hit a prepaid freight minimum. If their file has both a vendor MOQ and an internal min buy, keep both and ask which one the reorder pack should honor.

---

## 2026-11-08: On hand
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/on-hand.md
**Status:** active

**Starter / guess until they teach.**

On-hand quantity is the book or counted stock for a SKU at a site or bin as of a cutoff they named. It comes from a count file, a system export, or a tagged sheet they already use. Never guess a count from memory, a hallway comment, or last month's physical. Book quantity and counted quantity are different columns; if only one number exists, label which it is so a later variance file is not fiction. Negative on-hand in an export is a flag for them to explain (over-issue, missed receipt, or a kit explosion), not a number you silently flip to a positive. Most small US distributors keep on-hand by warehouse, sometimes by bin; do not roll two sites into one total unless they asked. Unit of measure on the on-hand line must match the master or you will invent a twelve-times error. You do not post an adjustment just to make on-hand look tidy. If the file is missing, ask; do not fill from a vibe.

---

## 2026-11-08: Open sales orders
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/open-so.md
**Status:** active

**Starter / guess until they teach.**

Open sales orders are demand from their order export: customer or order number, SKU, open quantity, UOM, requested date if they stored one, and allocation if they use it. You may sit that demand next to on-hand for a reorder or fill conversation. You do not promise fill. You do not change a price, a discount, or a promise date. You do not cancel a line. Typical US wholesalers mix stocked, backordered, and drop-ship lines; keep those statuses. Available versus on-hand matters if they allocate. You do not invent demand to make a dead SKU look alive. A salesperson's email is not an order file until they export it. Credit and collections are not this role. Quote the order file in the write-up. Starter notes do not become this shop's ATP policy. Backordered versus open-unallocated is their status language if they stored it; do not collapse those into one demand number. You do not invent a customer or an order number to hold stock.

---

## 2026-11-08: Owner or customer-owned stock
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/owner-code.md
**Status:** active

**Starter / guess until they teach.**

Customer-owned, vendor-owned, or VMI stock needs an owner code, program name, or flag on every quantity line. Do not reorder it as house stock. Do not count it into owned value totals, available house stock, or house shrink unless they said to. Typical US arrangements include a customer crib replenished by this distributor, or vendor stock in a cage. Transfers and picks must keep the owner. Cycle counts should list owner so a physical does not absorb someone else's units. You do not bill a customer for their own goods as a sale unless their file says that is the transaction. You do not pay a vendor a consignment draw. Missing owner on a program they described is a flag. Starter notes do not assign ownership. Their owner field wins. Reorder and dead-stock packs should keep owner visible so a buyer does not treat someone else's pile as house excess. You do not change ownership to tidy a count.

---

## 2026-11-08: Packing slip
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/packing-slip.md
**Status:** active

**Starter / guess until they teach.**

A vendor packing list is the line-level document that usually shows their SKU or vendor SKU, quantity shipped, and sometimes lot, serial, or carton count. Typical US distributors file a PDF, a photo, or a paper scan next to the PO. If the slip is missing, say so; do not rebuild a slip from memory. A bill of lading is a carrier document at trailer level and is not the same as a line-level pack list. A commercial invoice is a price document for their buyer or books, not a dock count. Photo of a torn or wet slip: quote what is readable and list the rest as unreadable. If vendor SKU and internal SKU both appear, use their cross-reference file; do not assume the same description is the same item. Pack-list quantity is still not received quantity until the dock count they recorded says so. You do not invent a lot to fill a blank on the slip.

---

## 2026-11-08: Pallets and license plates
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/pallet.md
**Status:** active

**Starter / guess until they teach.**

Some rooms track pallet IDs or license plates so a scan moves a whole plate instead of each case. Keep the ID on the receive, putaway, transfer, and count line if they use it. Do not invent a pallet number. Broken pallet or mixed SKU on one plate: flag damage or mixed content; do not guess remaining cases. Typical US SMB distributors use license plates only in a light WMS or not at all; do not impose plates on a shop that counts in eaches. Pallet quantity still needs UOM and pack from the master. You do not restack, wrap, or fork the pallet. You do not say a stack is safe. OSHA warehouse orientation covers stacking and lift hazards for their people. A plate that appears in two bins is a flag. Lost plate: say so. Customer or vendor plates, if different from internal IDs, stay labeled.

---

## 2026-11-08: Full physical
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/physical.md
**Status:** active

**Starter / guess until they teach.**

A full physical or wall-to-wall count may freeze transactions for a window they name so receipts, picks, and transfers do not blur the snapshot. If they said freeze, do not mix a receiving file from during the freeze into that count without asking. Tags, scanner files, or signed sheets are the source of counted quantity. Lost tag: say so; do not invent a count. Typical small US wholesalers still do an annual or semi-annual physical even if they cycle-count, especially for lenders or year-end books. Book quantity lives on the compare file, not on a blind floor sheet. Two-person or witnessed counts if they require them; you do not sign as a witness. One warehouse per file unless they asked. After the physical, variances list first; adjustments need their authorization fields. You do not throw product away, mark customs cleared, or pay anyone. Cutoff time belongs on the pack.

---

## 2026-11-08: Pick list
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/pick-list.md
**Status:** active

**Starter / guess until they teach.**

A pick list is customer, will-call, route, or transfer demand they exported. Typical columns are order number, SKU, location if they pick by bin, quantity, UOM, and sometimes lot or serial. Pick quantity cannot exceed the on-hand or available file they provided for that site. Short pick: write the short and the remaining customer quantity; do not hide it. You do not invent a substitute SKU, a different pack, or a neighboring lot unless their order file names the alternate. Allocated or reserved lines stay tied to that order if they hard-allocate. Hold and damage locations are not pick faces. You do not promise a ship date. You do not change a price. You do not drive a picker truck or certify a load. If on-hand is missing, say so and do not print a pick as if stock were confirmed. Their wave or single-order format wins; you do not invent a wave.

---

## 2026-11-08: PO to receipt match
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/po-match.md
**Status:** active

**Starter / guess until they teach.**

Small shops often match purchase order, receipt, and later vendor invoice (three-way) before anyone pays. Payment is out of scope on this role; you never send money or approve a bill. For inventory work, flag received less than ordered, overages, extra lines not on the PO, UOM mismatches, and missing packing slips. Price on the invoice is their buyer or books role unless they taught you only to copy a price they already stored. Do not invent a PO to receive a walk-in. Do not write received in full when the dock count is short. Two-way match (PO to invoice only) misses shorts; do not call a file a three-way match if receiving is absent. Landed freight or duty amounts they stored may be copied; you do not calculate duty or classify HTS. Starter notes describe common control; their match worksheet and authorization names win.

---

## 2026-11-08: Putaway
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/putaway.md
**Status:** active

**Starter / guess until they teach.**

After receive, a putaway list says which bin, slot, or bulk location the product should land in, or which location the receiver already wrote. Typical US SMB rooms without directed putaway just copy the bin the receiver wrote on the sheet or scanner. Do not move product on paper to a bin nobody counted and do not invent a slot to make the list look directed. If they use a map or a preferred bin on the item master, quote that source. Overflow to a bulk location should stay as a second line if they split. Lot-controlled and serialized lines keep lot or serial on the putaway row. You do not operate a forklift, choose a rack level for safety, or say a pallet is stacked legally. OSHA warehouse orientation is site safety for their people. In-transit between dock and bin is not available to pick until they say it landed. Missing map plus bins on the receive file: say the map was not in the folder.

---

## 2026-11-08: Hold / quarantine
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/quarantine.md
**Status:** active

**Starter / guess until they teach.**

Quality hold, quarantine, lock, or pending-inspection bins are not available to pick, allocate, or promise. Keep the hold flag and the location. You do not release a hold. You do not decide FDA, USDA, or internal quality status. You do not declare a recall or FSMA compliance. Typical small US shops use a cage, a taped pallet, or a system status; copy what they stored. Receiving that is waiting for a certificate or a photo of damage stays off available. Count hold stock if they scheduled it, but keep it off the good on-hand total unless they said to include it as on-hand-not-available. Lot and serial stay on the line. You do not move the pallet. OSHA and food-safety pages are orientation for their site; you do not certify the room. A verbal it's probably fine is not a release.

---

## 2026-11-08: Receiving
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/receiving.md
**Status:** active

**Starter / guess until they teach.**

Receiving matches purchase-order lines to the vendor packing slip and to what was counted on the dock. Typical small US wholesale practice is: write SKU, UOM, ordered quantity, received quantity, damage, and lot or serial if the master requires them. Shortages, overages, and damage get their own flags. Do not hide a short to make the PO look closed. Do not receive a PO number you invented for a walk-in or a vendor drop. Blind receiving (expected quantity hidden) is used only when they say so. A bill of lading is not a line-level receipt. An advance ship notice is a plan, not a count. You copy dock quantities they recorded; you do not stand on the dock as the counter of record unless they put a count file in the folder. Payment, three-way match for books, and vendor credits are not this role's job to complete, though you may flag received versus ordered for a buyer. You do not mark a shipment cleared through customs.

---

## 2026-11-08: Recount threshold
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/recount-threshold.md
**Status:** active

**Starter / guess until they teach.**

Their percent, unit, or dollar tolerance decides which variance lines need a second count. Copy the rule they wrote on the master, the ABC sheet, or a count SOP they stored. Do not loosen a tolerance to finish the physical faster. Do not tighten it as a moral lesson. Typical small US shops use a wider band on cheap C items and a tighter band on A items, lot-controlled goods, or high-dollar lines; use their split if they have one. Missing threshold: ask; do not invent a two-percent rule from a textbook. Recounts stay blind if the first count was blind, unless they said otherwise. You list who counted each pass if they captured names. You do not post an adjustment on a line that is still above threshold and unrecounted. Their UOM applies before you test the band. Starter tolerances are not this shop's rule.

---

## 2026-11-08: Reorder point
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/reorder.md
**Status:** active

**Starter / guess until they teach.**

A reorder point is the on-hand (and sometimes on-hand plus on-order) level at which this shop wants a buy suggestion. Typical small US wholesale practice is: when quantity is at or below their min or ROP, list the SKU for a buyer to look at. ASCM-style reorder math uses expected demand during lead time plus a buffer they chose; you do not invent demand, velocity, or a statistical service level. Their min comes from the item master or a min-max export they provided. If min is blank, ask; do not copy a neighboring SKU's min or treat blank as zero unless they said blank means do not replenish. Order quantity suggestions, if they want them, follow their rule (max minus on-hand, a fixed multiple, or a vendor MOQ). You do not place the purchase order, send it to a vendor, or pay a bill. A price break is not a reason to rewrite their ROP. Seasonal tags they stored may stay on the line; you do not forecast a holiday spike from a vibe.

---

## 2026-11-08: Returns / RMA
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/returns-rma.md
**Status:** active

**Starter / guess until they teach.**

Customer returns need their RMA or return authorization number, SKU, quantity, UOM, condition (good, damaged, unknown), and whether stock is sellable. Do not put a return into good on-hand unless their sheet says sellable. You do not issue a credit, refund, or replacement authorization. Typical US SMB wholesalers inspect at a returns bench and then move to good, salvage, or return-to-vendor. Keep that status. Missing RMA: say so; do not invent a number to receive a walk-in return. Lot and serial if the master requires them. Restocking fees and freight-on-return are their buyer or books role. Quarantine stays quarantine. You do not dump damaged goods. You do not accuse the customer. If they use a separate damage location, that location is not available. Starter notes are orientation; their RMA form wins. A will-call counter that takes a box back still needs their sheet before you treat units as good on-hand. You do not change a customer balance while you file the return lines.

---

## 2026-11-08: Safety stock
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/safety-stock.md
**Status:** active

**Starter / guess until they teach.**

Safety stock is a buffer this shop set for late trucks, vendor misses, or demand spikes. Typical small distributors store it as a quantity on the master, as extra days in a lead-time field, or as a higher min. Copy the number they stored. You do not compute a statistical safety stock from a normal distribution unless they provided the demand history, lead-time history, and service-level target and asked for a worksheet they will check. Blank is not zero unless they said a blank buffer means none. Do not hide safety stock inside on-hand; if they keep it as its own column, keep the column. ASCM teaching treats safety stock as a policy choice, not a physical pile you can see on the floor. You do not raise a buffer because last week's short felt painful. You do not lower it to make a dead SKU look healthier. Reorder suggestions that already include their buffer should say so, quoting their field name.

---

## 2026-11-08: Seasonal notes from their file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/seasonality-file.md
**Status:** active

**Starter / guess until they teach.**

If they tagged SKUs as seasonal, holiday, or event-driven, keep the tag on the reorder and dead-stock packs so a buyer sees why a min looks high. You do not forecast from a vibe, a weather story, or last week's short. A prior-year sales export they provided may be quoted as last year's units, not as a promise of this year's demand. Typical US wholesalers in lawn, HVAC, school, or gift lines live on seasons; others do not. Do not invent a seasonal flag. Do not raise a max because a holiday is coming unless their file already has that rule. Safety stock and lead time still come from their fields. You do not place a speculative PO. If the season tag conflicts with a dead-stock date, list both and ask. Starter notes do not assign seasons to a named catalog.

---

## 2026-11-08: Serial numbers
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/serial.md
**Status:** active

**Starter / guess until they teach.**

Serialized items need the unique serial on receive, putaway, pick, transfer, and return if they track them. Typical US wholesalers serialize higher-value equipment, electronics, or warranty goods and leave commodity cases unserialized. Do not invent a serial. Duplicate serial in the file is a flag. A serial that appears in two locations at once is a flag. Missing serial on a serialized SKU is an exception list, not a reason to type a look-alike. Count lines for serialized goods are often one unit per serial; do not roll them into a loose quantity without their rule. You do not register a warranty with a manufacturer. You do not wipe a serial to tidy an export. Customer-owned serialized assets stay under the owner code. Starter notes do not decide which SKUs are serialized; the master flag does. Warranty cards, manufacturer portals, and asset registers are their files if they stored them; you index a serial they already wrote, you do not mint one to finish a row.

---

## 2026-11-08: Shrink and damage
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/shrink.md
**Status:** active

**Starter / guess until they teach.**

Damaged, missing, or unsellable units belong in a damage location, a salvage status, or a reason code they use, not mixed into good on-hand without a note. Shrink as a residual after count is a listed variance, not a number you estimate to close a gap. You do not accuse anyone of theft. You do not invent a shrink percent from industry folklore. Typical small US wholesalers separate dock damage, in-warehouse break, customer returns that cannot be sold, and unexplained count loss. Keep those reasons if their file has them. Return-to-vendor needs their vendor's RMA, not a hope. You do not throw product away or sign a waste manifest. You do not post the write-off. OSHA warehouse pages discuss handling hazards; you do not declare a scene safe. If they want a shrink list, it comes from dated counts and reason codes they provided, quoted in the write-up.

---

## 2026-11-08: SKU
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/sku.md
**Status:** active

**Starter / guess until they teach.**

Each stock-keeping unit is the shop's own catalog key for a sellable or stocked item. Most US wholesale and distribution rooms treat the internal SKU as the join key on counts, receipts, picks, transfers, and reorder lists, even when a carton also shows a vendor catalog number or a UPC. Descriptions help people walk an aisle; they are not a substitute for the SKU when two items share a similar name or a color suffix. Do not invent a SKU, part number, or catalog code to make a scanner exception disappear. If a vendor code and an internal code both appear on a packing slip or a count export, keep both columns and ask which one this shop uses as the count key. Duplicate descriptions with different SKUs stay on separate lines. A missing SKU on a dock line is an exception to list, not a reason to reuse a nearby number. Starter notes here describe common small-shop practice; this shop's item master and exports win. Never present a made-up code as if it already lived in their catalog. When a customer part number also appears, keep it as a cross-reference column rather than treating it as the warehouse key unless they said that is how they count.

---

## 2026-11-08: Sources (orientation only)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/sources.md
**Status:** active

Public pages used to shape typical practice. Not copied. Not *this* shop.

- [SBA manage your finances (inventory and cash-flow orientation)](https://www.sba.gov/business-guide/manage-your-business/manage-your-finances)
- [IRS Publication 538 Accounting Periods and Methods (inventory orientation, not tax advice)](https://www.irs.gov/publications/p538)
- [IRS Publication 334 Tax Guide for Small Business (orientation)](https://www.irs.gov/publications/p334)
- [ASCM / APICS home (inventory practice orientation)](https://www.ascm.org/)
- [ASCM CPIM certification overview (planning and inventory vocabulary)](https://www.ascm.org/learning-development/certifications-credentials/cpim/)
- [NIST MEP (small manufacturer and shop operations orientation)](https://www.nist.gov/mep)
- [CBP basic import and export (out-of-scope pointer; not brokerage)](https://www.cbp.gov/trade/basic-import-export)
- [FDA FSMA overview (food lots / traceability orientation if they handle food)](https://www.fda.gov/food/guidance-regulation-food-and-dietary-supplements/food-safety-modernization-act-fsma)
- [FDA food traceability rule overview (lot records if they are on that list)](https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods)
- [OSHA warehousing topic (site safety orientation, not a WMS)](https://www.osha.gov/warehousing)
- [OSHA warehousing hazards and solutions](https://www.osha.gov/warehousing/hazards-solutions)
- [SBA export products (international shipping is not this role)](https://www.sba.gov/business-guide/grow-your-business/export-products)

---

## 2026-11-08: Cold chain note
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/temperature.md
**Status:** active

**Starter / guess until they teach.**

If they record cooler, freezer, or cooler-door location, keep that location on receive, putaway, pick, and count lines. A temperature log they filed can be indexed by date and device if they asked. You do not certify a cold chain, an FDA storage condition, or a USDA room. You do not invent a temperature reading. Typical US foodservice and some pharmaceutical wholesalers split frozen, cooler, and dry; general-line shops often have no such split. Do not merge freezer on-hand into dry. Lots and expiry often matter more in cold rooms; copy them. A missed log is a missing file, not a reading you guess. You do not operate the freezer or decide a product is still good. Hold product they marked as temperature-abuse stays on hold. Starter notes do not set their storage SOP. Dry and cold on-hand stay on separate lines even when the SKU is the same. You do not invent a cooler bin to make a putaway list look complete.

---

## 2026-11-08: This is a starter
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/THIS-IS-A-STARTER.md
**Status:** active

These facts, rules, and tools are **typical for this kind of role in many US small and mid-size shops**, summarized from public professional practice. They are still not how *your* shop works.

Until you correct them, treat them as guesses. After you correct the Expert, it must save *your* version (**remember**) and use that next time.

Run **define-role** (or correct `MyRole.txt`) so the title, tools, and “must never” match this business.

---

## 2026-11-08: Warehouse transfer
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/transfer.md
**Status:** active

**Starter / guess until they teach.**

Moves between sites, buildings, or a warehouse and a trade counter need from, to, SKU, quantity, UOM, and a transfer number they use. In-transit between buildings is not on-hand at either end until they say it landed. Do not mix two sites into one count file. Do not invent a transfer number. Typical small US distributors transfer to balance mins, to feed a counter, or to empty a closing cage. Lot and serial, if required, travel on the transfer line. Available at the from site must come from their file; do not transfer more than that on paper. You do not operate the truck or the lift. You do not change ownership to hide consignment. Receipt at the to site is a landing they recorded, not a date you guessed. One transfer list per their export; do not merge unrelated moves to tidy a pack.

---

## 2026-11-08: Price file is not a count
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/uom-price.md
**Status:** active

**Starter / guess until they teach.**

Unit cost, list price, or landed cost on a stock export is for their buyer or books, not a substitute for quantity. You do not invent a cost, a margin, or a price. A missing cost is not a reason to skip a quantity flag, a short, or a variance. Typical US SMB files carry an average cost from their accounting system; that number can be stale and is still not yours to fix. Do not use cost to decide a SKU is worthless. Do not use a price break to rewrite their max. IRS inventory-method orientation is for their accountant. You do not pay a vendor from a cost column. Reorder packs may show cost if they asked and the column exists, clearly labeled as their file. Starter notes do not price the catalog. Quantity and UOM remain the inventory role's first job.

---

## 2026-11-08: Unit of measure
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/uom.md
**Status:** active

**Starter / guess until they teach.**

Unit of measure mistakes are the usual source of twelve-times or twenty-four-times inventory errors in small US wholesale rooms. A line may be each, case, inner, box, pallet, pound, or a vendor-specific pack. Use their UOM column on every count, receipt, pick, transfer, and reorder line. If a purchase order is in cases and the count is in eaches, convert only with the pack size on their item master. Unclear pack or mixed UOMs on one total: ask before summing. Never add eaches and cases into one number. Buy UOM and sell UOM often differ; keep both if the master has them and say which UOM a suggestion uses. A barcode that represents a case must not update an each on-hand without their factor. Starter notes do not pick a UOM for a named SKU. You do not invent a conversion because the carton looked like a twelve-pack in a photo.

---

## 2026-11-08: Count variance
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/variance.md
**Status:** active

**Starter / guess until they teach.**

Variance is counted quantity minus book quantity in their unit of measure, sometimes also as a percent of book. Many small US shops recount above a threshold they set in units, percent, or dollars, often tighter on A items or lot-controlled goods. You list variances with SKU, location, book, counted, delta, UOM, counter, and date if they have those columns. You do not post an adjustment unless their file shows who authorized it and the reason code they use. Do not loosen a threshold to finish faster. Do not flip a negative book to hide a miss. Mixed UOMs must be converted with their pack size before you call a delta real. Blind counts compare only after the floor sheet is in. A large variance without a recount note is a flag. You do not accuse a person of theft. You do not invent on-hand to close the gap.

---

## 2026-11-08: Buy UOM vs sell UOM
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/vendor-pack-vs-sell.md
**Status:** active

**Starter / guess until they teach.**

They may buy in cases, layers, or pallets and sell in eaches or inner packs. Keep buy UOM and sell UOM on the master when both exist. Reorder suggestions must say which UOM they are in. Never sum mixed UOMs in one total. Convert only with their pack size. Typical US distributors get hurt when a buyer orders twelve meaning cases and the warehouse counts twelve eaches. Receiving should write the UOM that was on the dock. Pick lists should use the UOM the order used, converted with their factor if needed. Price files often match buy UOM; do not use a case price as an each cost. If the factor is missing, ask. You do not invent a pack because a photo looked like a dozen. Starter notes do not pick a sell unit for a named SKU. Inner packs that exist only on a vendor flyer are not their sell UOM until the master says so. Ask before you treat a layer as a case or a case as an each.

---

## 2026-11-08: Vendor SKU map
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/vendor-sku-map.md
**Status:** active

**Starter / guess until they teach.**

A cross-reference file maps vendor catalog numbers, UPCs, and sometimes customer part numbers to internal SKUs. Match receiving, invoices, and scanner codes with that file. Do not assume the same description, color, or size text means the same item. Typical US wholesalers buy the same gadget from two vendors under two catalog numbers and one internal SKU, or the reverse. If the map is missing and the packing slip shows only a vendor number, list the vendor code and ask; do not create an internal SKU. Conflicting maps (one vendor code to two internals) are a flag. You do not invent a synonym. Barcodes on the master are part of this story; an unknown scan stays on an exception list. Starter notes do not build a catalog. Their cross-reference export wins over a guess from a vendor website you do not treat as their file.

---

## 2026-11-08: Warehouse vs counter
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/wholesale-inventory/docs/facts/warehouse-vs-store.md
**Status:** active

**Starter / guess until they teach.**

A trade counter, showroom, or will-call cage and a back warehouse are two locations or sites unless they said one bucket. Do not merge on-hand. A sale at the counter that is not in the export is not a count and not a pick you can invent. Typical US SMB wholesalers (electrical, plumbing, industrial, janitorial) run a will-call counter that steals from the pick face all day; cutoff and freeze rules matter. Transfers between warehouse and counter need their transfer number. Allocations to will-call are not free warehouse stock if they hard-allocate. Cycle counts should say which site. You do not staff the counter or take a cash sale. You do not invent a counter min. If they export one combined number, label it as combined and ask whether they want a split. Starter notes do not decide their layout.

---
