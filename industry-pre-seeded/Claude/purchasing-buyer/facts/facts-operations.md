# Facts — Operations (pre-seeded)


---

### 2026-11-08: Acknowledgment vs invoice
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/acknowledgement-vs-invoice.md
**Status:** active

**Starter / guess until they teach.**

A proforma, quotation, or order acknowledgment is not an invoice for three-way match. Use the document type in the filename or header they stored. Typical US SMB folders mix OA, proforma, commercial invoice, and packing slip. Paying from a proforma is AP’s problem; you still name the document you have and you do not mark match complete on a non-invoice. A commercial invoice for match should show amounts, SKU or description, and usually the PO number. You do not relabel an OA as an invoice to finish the pack. You do not pay and you do not schedule payment from a proforma. If they only dropped a proforma, say the invoice leg is missing. Filename “invoice” does not override a proforma header. A packing slip is also not an invoice. Starter until they teach how *this* shop names vendor document types.

---

### 2026-11-08: Approval / authorization
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/approval-matrix.md
**Status:** active

**Starter / guess until they teach.**

Who may approve a purchase order typically depends on dollar amount, account, commodity, or whether the vendor is on the AVL. Typical US SMB shops write a one-page matrix: buyer to X dollars, plant manager to Y, owner above that; some use email approval saved as a PDF. Their matrix or signature file is the source. A buyer-built draft without the required name or amount approval is still a draft. You do not send it to the vendor as live and you do not label it issued. If the folder has no matrix, say so and ask — do not assume the buyer can issue any amount. Splitting one need across two POs to stay under a threshold is a question for them, not a trick you apply. Blanket releases often follow the same matrix or a simpler release rule they wrote. This Expert flags missing authorization. They sign or click approve. Starter until they teach *this* shop’s thresholds.

---

### 2026-11-08: Approved vendor list (AVL)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/approved-vendor.md
**Status:** active

**Starter / guess until they teach.**

An approved vendor list is the shop’s file of suppliers they will buy from for named commodities or all production buys. Typical US SMB manufacturers keep an AVL for ISO, customer, or quality reasons; job shops and offices may keep a shorter preferred-vendor list or none at all. A pack may treat a supplier as approved only when that exact name (or their stated alias) appears on the list they exported. Do not add a vendor in the write-up, do not mark a new name approved, and do not treat a one-time buy or a sole-source email as a back-door AVL add. A one-time or emergency buy is a question for whoever owns the AVL. If they have no AVL, say so and do not invent one. Inactive, expired, or “conditional” statuses on their sheet stay as written. Dual-source notes on the AVL are theirs; you do not declare the market has only one vendor. This Expert checks names against the file. They add or remove rows. Starter until they teach how *this* shop maintains the list.

---

### 2026-11-08: Backorder / late list
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/backorder-list.md
**Status:** active

**Starter / guess until they teach.**

Open lines past need-by, or lines with a vendor backorder note, belong on a follow-up list. Typical US SMB buyers run this weekly from the open-PO export plus the latest acknowledgment or vendor email PDF. Promise dates come from that latest vendor file, not from hope and not from last month’s quote. They contact the vendor unless they asked you only to list. Do not overwrite need-by with the late promise. Do not drop a line because it is embarrassing. If the vendor PDF is silent, the promise cell stays blank and becomes an ask. Infeasible original need-by (shorter than quoted lead time) should already have been flagged; still list the line if it is open and late versus the need they kept. Cancel or close-short is their decision. This Expert builds the list. They expedite. Starter until they teach *this* shop’s late-line cadence.

---

### 2026-11-08: Blanket PO and releases
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/blanket.md
**Status:** active

**Starter / guess until they teach.**

A blanket or master purchase order holds a period, a not-to-exceed dollar amount, a price, or a quantity envelope; releases or call-offs pull quantity against that number without rewriting the commercial terms each time. Typical US SMB roles use blankets for fasteners, packaging, gases, MRO, and repeating production parts. Keep the blanket number on every release line. Remaining NTE or remaining quantity, if they track it, comes from their blanket log after prior releases — do not invent remaining value. Release prices come from the blanket price file, not from a new one-off quote that contradicts the blanket unless they asked you to show a change. Do not issue a standalone PO price that fights the blanket file without asking. A release is still a draft until they approve and send. Closing a blanket or raising NTE is their decision. You draft the release pack. They authorize. Starter until they teach how *this* shop numbers blankets and releases.

---

### 2026-11-08: Buyer role vs AP
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/buyer-vs-ap.md
**Status:** active

**Starter / guess until they teach.**

The buyer role owns the PO, AVL questions, price file, lead time, and receiving-match exceptions. Accounts payable owns payment, discounts taken, and the remittance. Typical US SMB shops split these roles even when one person wears both hats on different days. A clean match file is a handoff, not a “paid” stamp. You do not send money. You do not schedule a payment run or take an early-pay discount. If they use a Bookkeeping Expert or a bookkeeper, that is where bills and coding go after match. Invoice price variance may be discussed by both; you still do not overwrite prices on either document. Non-PO invoices follow their AP rule. A green match is still not cash out the door. Terms recorded on the PO are not a remittance you send. Starter until they teach how *this* shop splits buyer and payables.

---

### 2026-11-08: Cancel or close short
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/cancel-po.md
**Status:** active

**Starter / guess until they teach.**

Closing a PO short — remaining quantity will not ship — or canceling a line is their decision, not a tidy-up you apply to the aging report. Typical US SMB roles cancel for a dead job, a substitute, a vendor who cannot ship, or a duplicate order. You list remaining open quantity and the last vendor note from the file. Do not zero an open line to clean aging. Do not write “closed” unless their export or a signed close-short note says so. A cancel may still leave a restocking charge or a vendor claim; those dollars come from a vendor file, not a guess, and payment of any charge is AP. Receiving that arrives after they closed short is a new question (keep, return, or new PO). You do not invent a cancel reason. You do not email the vendor a cancel as this product unless they taught that send step and the line is approved to cancel. Starter until they teach how *this* shop closes shorts.

---

### 2026-11-08: Missing cert = hold
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/certificate-hold.md
**Status:** active

**Starter / guess until they teach.**

If the PO required a certificate and the folder has none, the line is incomplete even if pieces are on the dock. Say that. Do not mark match complete. Typical US SMB quality holds apply until the CoC or mill cert lands. A cert for the wrong lot, wrong rev, or wrong spec is still a miss. You do not invent a cert number or accept a verbal “it’s coming” as the file. Receiving qty can be on hold; it is not good available stock and it is not a clean three-way good receive. This is the same family as inspection hold, keyed to the document requirement. They chase the vendor or waive in writing. You flag. A cert promised “to follow” is still missing until the PDF is in the folder. Starter until they teach which *this* shop’s POs require certs.

---

### 2026-11-08: Change order
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/change-order.md
**Status:** active

**Starter / guess until they teach.**

Quantity, date, price, revision, or ship-to changes after a PO is issued need their change-order process and a new line or header revision if they use one. Typical US SMB shops write a short CO: original value, new value, reason, and who approved. Do not quietly edit the original PO CSV to match a vendor email so the open-order list “looks right.” Show old versus new with the vendor PDF or buyer note that triggered the change. An acknowledgment that changes terms is a CO question, not a confirmation. Need-by changes from the floor are also changes. Closing a line short is a different decision and still needs their word. You do not send the change to the vendor as live. They approve and they communicate. Blanket releases that exceed remaining NTE are a blanket change, not a quiet extra release. Starter until they teach *this* shop’s revision numbering.

---

### 2026-11-08: Certificates and CoC
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/coc.md
**Status:** active

**Starter / guess until they teach.**

A certificate of conformance, material cert, or test report is a file they required on the PO or item master. Typical US SMB manufacturers ask for CoC on production parts and mill certs on metal; job shops ask when the customer did. List present or missing against the PO requirement. You do not approve a cert as an engineer, metallurgist, or quality manager unless they taught that exact step to this role — usually you flag missing, wrong revision, or a lot that does not match receiving. A cert that names a different revision or spec than the PO is a hold question. Do not mark three-way receive complete if the PO required a cert and the folder has none. You do not forge a cert number. Photos of a cert they scanned are fine as the file. This is not a regulatory stamp. Starter until they teach how *this* shop files and reviews certs.

---

### 2026-11-08: Consignment or vendor-managed if they use it
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/consignment.md
**Status:** active

**Starter / guess until they teach.**

Consignment or vendor-managed inventory they do not own yet should not hit the regular buy-to-own PO the same way if their file splits it. Typical US SMB shops use consignment for fasteners, gases, or high-value spare parts; VMI may replenish a crib without a classic PO each time. Ask how *this* shop books a consume or a replenishment. Do not receive consignment as purchased inventory unless their sheet says that is how they book it. Do not invent a transfer price or a consume quantity. A consumption report they exported is the usual qty source; you do not guess crib usage. Three-way match may be consume-plus-invoice rather than dock-plus-PO — only if they taught that. Ownership, lien, and tax questions are theirs and AP’s, not a legal opinion from this role. Starter until they teach *this* shop’s consignment or VMI rule.

---

### 2026-11-08: Country of origin if on file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/coo-if-file.md
**Status:** active

**Starter / guess until they teach.**

Country of origin comes from the vendor certificate, invoice, or packing documents they saved — copied as written. Typical US SMB shops collect COO when a customer or a program asked. You do not give a customs classification, duty, drawback, or preference-program legal opinion. HS or HTS codes only if their file already has them — and still not as entry advice. You do not mark a shipment “cleared customs” and you do not act as broker of record. You do not invent a country to complete a customer form. If documents disagree (packing slip versus cert), quote both and ask. “Made in” marketing language on a catalog is not a cert unless they said to treat it as the file. Blank COO stays blank. This is buyer-file completeness, not brokerage. Starter until they teach when *this* shop collects COO.

---

### 2026-11-08: Currency and units on the quote
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/currency.md
**Status:** active

**Starter / guess until they teach.**

If the PDF is not USD, keep the currency label on every price you copy. Typical US SMB shops buy some tooling or components in EUR, CAD, or CNY. Do not convert with a guessed rate, a remembered rate, or a website you did not save into their folder at their request. Minimum-charge and lot-charge lines on a quote are real lines if they will appear on the invoice; do not hide them inside piece price. Mixed currency on one PO is a question; do not blend totals. Open commitment in a foreign currency stays in that currency unless they gave a dated rate file they want used — and even then you label it converted. You do not hedge or give an FX opinion. A USD total you typed from a foreign PDF is a guessed conversion unless they filed the rate. Starter until they teach how *this* shop prints currency on POs.

---

### 2026-11-08: Damaged or wrong on the dock
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/damaged-dock.md
**Status:** active

**Starter / guess until they teach.**

Receiving should note damage, shortage versus packing slip, wet cartons, or wrong SKU before the line is put away as good. Typical US SMB docks write a discrepancy on the receiving sheet, take a phone photo, and hold the pallet. Photos they took can sit in the folder. Do not book damaged goods as received-good quantity. Do not “receive in full” and mention damage later in a comment that AP will miss. Wrong SKU is not a substitute accept unless their engineering or buyer note says so. Hidden damage found after put-away is still a discrepancy; date it from their note, not from when you typed the pack. RMA or vendor claim is a later step with their RMA number. You do not certify freight claims as counsel or tell them who legally owns the risk; quote the freight term on the file if they ask in operational language. Held damaged qty is not available inventory and is not a clean three-way receive. Starter until they teach *this* shop’s dock discrepancy form.

---

### 2026-11-08: Drop-ship
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/drop-ship.md
**Status:** active

**Starter / guess until they teach.**

Drop-ship lines need the customer or job ship-to from the requisition or sales order they stored, not a remembered site. Typical US SMB shops drop-ship when they never want the part on their dock. Receiving may be a customer packing slip they forwarded, a signed delivery photo, or a carrier POD they saved — not a plant dock count. Three-way still needs *some* receipt evidence they accept; ask what *this* shop uses. Do not invent a ship-to or a job number. Do not mark received in full from an ASN alone. Shorts the customer reports are still shorts. Invoice match uses that evidence plus the PO. You do not pay the vendor. Wrong ship-to on a drop-ship is a serious miss; quote the requisition address next to the PO address if they differ. Starter until they teach *this* shop’s drop-ship evidence rule.

---

### 2026-11-08: Non-inventory / dummy SKUs
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/dummy-sku.md
**Status:** active

**Starter / guess until they teach.**

Expense, tooling, NRE, and one-time buys may use a dummy or non-inventory SKU. Typical US SMB QuickBooks shops use a generic “materials” or “tooling” item. They still need a clear description, quantity, unit, and a price from a quote. Do not reuse last year’s dummy price. Do not hide a production part on a dummy SKU to skip AVL or rev control if their rule would have required those. Receiving a dummy line may be a packing slip plus a photo; ask what they accept. Three-way still needs some evidence if they asked for it. You do not invent the dummy item number or a leftover price from a different job. Account coding for expense versus inventory is books if they split; you can copy the account they put on the requisition. Starter until they teach *this* shop’s non-inventory item list.

---

### 2026-11-08: Freight amount
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/freight-amount.md
**Status:** active

**Starter / guess until they teach.**

Freight dollars come from the quote, the invoice, a prepaid-freight policy file, or a carrier invoice they stored — not from a guessed shipping calculator. Typical US SMB POs either include freight in the piece price, show a separate freight line, or say “prepay and add” with the amount unknown until the invoice. Do not guess a shipping charge to complete three-way math. If freight appears on the invoice and not on the PO, name it as an unmatched invoice line or an exception; their written tolerance may or may not cover small freight differences. Prepaid versus collect is a term on their form, not a payment you make. Fuel surcharges and residential delivery fees are real if they are on the invoice file. You do not invent a freight dollar, a discount, or a “usual percent of goods.” Ask if the file is silent. This is still not a payment role. Starter until they teach *this* shop’s freight policy.

---

### 2026-11-08: Hazardous / SDS on the PO
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/hazmat-sds.md
**Status:** active

**Starter / guess until they teach.**

If they require a safety data sheet with the shipment or on file before stock, list whether the SDS arrived and the date on the file. Typical US SMB shops that buy chemicals, aerosols, or welding consumables keep SDS PDFs in a folder or binder. You do not certify OSHA compliance, do not give disposal or shipping legal advice, and do not classify hazardous materials for transport. Missing SDS when the PO or their chemical rule required it is a hold or incompleteness note, not a quiet receive. You do not invent an SDS date or a product identifier. If the SDS name does not match the received SKU, flag it. An outdated SDS they already filed is a question for whoever owns the chemical binder, not a new sheet you write. This role does not train the floor on PPE. Orientation only. Starter until they teach how *this* shop files SDS versus receiving.

---

### 2026-11-08: How this role files work items
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/how-we-file.md
**Status:** active

**Starter / guess until they teach.**

Day-to-day work does **not** go in one shared pile. Each **work item** gets its own folder under `work-items/<id>/` so Tuesday does not overwrite Monday, and one PO does not mix with the next.

Typical name for *this* role (until they teach a different pattern):

- **What one folder is:** purchase order, RFQ pack, match pack, or receiving event
- **How to name it:** `work-items/WID-20260915/` (operator may also use a PO number in the description)
- **Pattern:** `work-items/<id>/`

Inside every Work Item folder:

- `in/` — files they dropped for *this* item only
- `work/` — scratch while this item is in progress
- `out/` — the finished list or pack for *this* item
- `evidence/` — check logs for this item only

Three-way match stays in that PO’s Work Item. A blanket release is named with the blanket number plus release.

If they already file another way (their software’s id, a PO number, a period name), **use their words**. Ask before starting if it is unclear which item this is. Never dump new files into yesterday’s folder. Never put two POs, two RFQs, or two receiving events in the same Work Item unless they asked for a combined pack and named it that way.

---

### 2026-11-08: Freight terms / Incoterms if on file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/incoterm-if-file.md
**Status:** active

**Starter / guess until they teach.**

FOB, EXW, FCA, DAP, DDP, and similar words on a quote or PO change who is responsible for freight cost and, in commercial practice, when risk moves. Typical US SMB domestic buys print “FOB origin” or “FOB destination” or “freight prepaid and add.” International quotes may show Incoterms 2020 labels. Quote the term exactly as it appears on their quote or PO form. You do not give a customs, insurance, or title legal opinion, and you do not explain who “should” insure the load as counsel. If the term is blank, say blank — do not assume FOB origin or destination. A freight-amount line is a dollar question from the quote or invoice, not a substitute for the term. ICC Incoterms pages are orientation only. If they asked what a printed term usually means in buyer language, keep it operational and labeled not legal advice. Starter until they teach how *this* shop prints freight terms.

---

### 2026-11-08: Inspection hold
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/inspection-hold.md
**Status:** active

**Starter / guess until they teach.**

Some parts go to incoming inspection, quality hold, or material review (MRB) before they are available. Typical US SMB manufacturers hold first-article, customer-critical, or damaged-looking receipts. Held quantity is not available inventory and is not a clean three-way receive into good stock. Keep the hold flag from their receiving or QA sheet. Do not move held qty onto the good-received column to finish a match. Do not invent an inspect result. If the sheet says “to inspection” with no accept or reject yet, the line is open from a quality standpoint even if pieces are on site. Rejected qty is not a good receipt; it may become an RMA. You do not close MRB. They (quality or the buyer they named) disposition. Match exceptions should still name the PO, receipt, and invoice legs. Starter until they teach *this* shop’s incoming-inspect routing.

---

### 2026-11-08: Invoice is not a PO
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/invoice-not-po.md
**Status:** active

**Starter / guess until they teach.**

A vendor invoice without a PO is a non-PO buy if they allow those, or an error. Their rule file says which. Typical US SMB shops allow small-dollar non-PO invoices and require a PO above a threshold. You do not create a backdated PO to make three-way look clean unless they asked for a documented after-the-fact PO process. Do not invent a PO number or a fake issue date. Do not pretend a quote or an acknowledgment is a PO. Match language on a non-PO invoice is two-way at most (invoice plus their approval), and payment is still AP. Recurring subscriptions they never PO’d stay a policy question. This Expert names the document you have. They decide after-the-fact or return-to-vendor. A packing slip without a PO is not an invoice and not a PO. Starter until they teach *this* shop’s non-PO rule.

---

### 2026-11-08: Invoice price variance
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/ipv.md
**Status:** active

**Starter / guess until they teach.**

Invoice unit price not equal to PO unit price is an invoice price variance. Quote both numbers from the files, with UOM, and the quote or contract the PO used. Typical US SMB causes: expired quote reused, vendor increase without a change order, UOM confusion, or a price-break qty the PO did not hit. They (buyer or AP) decide who is right and whether to change the PO, dispute the invoice, or accept a variance. You do not overwrite the PO price to match the invoice so the match “clears.” You do not overwrite the invoice PDF. Freight or tax lines are not IPV unless they coded them as unit price. If the price file is missing, ask — do not pick the invoice as truth. Show the quote valid-until date when it explains the fight. Starter until they teach who at *this* shop owns price disputes.

---

### 2026-11-08: Item master export
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/item-master.md
**Status:** active

**Starter / guess until they teach.**

Preferred vendor, UOM, revision, buyer code, and min/max come from their item-master export if they have one. Typical US SMB manufacturers live and die by that file; stale masters cause bad POs. If master and quote disagree on UOM, price, vendor, or rev, quote both and ask. Do not invent a SKU or a UOM factor. Do not silently prefer the quote over the master or the reverse. Dummy SKUs still appear on some masters. Lot-controlled and cert-required flags on the master drive receiving holds. You do not redesign the master as an ERP project. A missing master row for a new part is an ask, not a new item you create unless they taught that step and their process allows it. Preferred vendor on the master still needs an AVL check when they keep an AVL. Starter until they teach which fields on *this* shop’s master win.

---

### 2026-11-08: Kanban / bin refill
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/kanban-bin.md
**Status:** active

**Starter / guess until they teach.**

Bin cards, two-bin, and kanban quantities come from their card, label, or kanban sheet. Typical US SMB shops use two-bin on fasteners and consumables. A refill PO still needs SKU, approved vendor, and a price file. Do not guess the bin size or the card qty from a photo you do not have. Do not treat an empty bin as proof of a number that is not on the card. If the card and the item-master min disagree, quote both and ask. Scan or photo of the card they stored is the qty source. Releases against a blanket are common for kanban; keep the blanket number. You do not redesign their pull system or invent a new card qty to “right-size” the crib. A refill is still a draft PO until they approve. Starter until they teach how *this* shop sizes bins and who may refill.

---

### 2026-11-08: Lead time from vendor PDF
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/lead-time.md
**Status:** active

**Starter / guess until they teach.**

Quoted lead time and promised ship or dock dates come from the vendor email, quote PDF, or order acknowledgment they saved — not from a remembered “they usually take two weeks.” Typical US SMB roles see production lead time, transit time, and a promised date as separate fields when the vendor file splits them; keep them separate if the PDF does. A need-by date from the floor is not a promise. If need-by is sooner than the quoted lead time, flag the line as infeasible and let them choose expedite, substitute, or a later need-by. Do not overwrite need-by with a late promise to make the open-PO list look on time. Acknowledgments often change the date; show old versus new and treat a worse date as a change they must accept. If the folder has no lead-time or promise document, ask. Do not fill ETA from hope, from another customer’s rumor, or from a generic industry table. Transit after FOB origin is still not a customs or insurance opinion. Starter until they teach how *this* shop records lead time and promise dates.

---

### 2026-11-08: Lot and serial if they track them
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/lot-serial.md
**Status:** active

**Starter / guess until they teach.**

If the item master, customer spec, or the PO requires lot, heat, serial, or cote, the receiving file should have it. Typical US SMB shops track lots on metals, chemicals, food-contact, aerospace, and anything they must recall. Missing lot on a controlled part is a hold, not a quiet receive into good stock. You do not invent a lot number, heat number, or serial to complete a column. If the packing slip has a lot and the dock sheet is blank, quote the slip and ask them to confirm the count against that lot. Multiple lots on one PO line stay as separate receiving rows if their sheet splits them. Certificates that name a lot should match the received lot. You do not waive a lot requirement because the parts “look the same.” If they do not track lots on that SKU, do not add lot theater. Starter until they teach which *this* shop’s SKUs are controlled.

---

### 2026-11-08: Match tolerance
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/match-tolerance.md
**Status:** active

**Starter / guess until they teach.**

Penny rounding, small tax differences, and small freight differences may pass if they wrote a tolerance in dollars or percent. The number is theirs. Typical US SMB AP policies use a few cents, a dollar band, or a small percent of the line. Do not apply a “usual two percent” from another company or from a textbook. Over tolerance: exception list, not auto-OK. Quantity tolerance is a different rule from price tolerance; do not blend them. UOM mismatches are not rounding. Invoice price variance is not freight. If they have no written tolerance, treat any difference as an exception and ask. You do not invent a band so the pack looks clean. You do not mark paid when an exception is still open. Hand the exception list to the buyer or AP as they split roles. Starter until they teach *this* shop’s written match bands.

---

### 2026-11-08: MOQ, spool, and pack
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/min-buy.md
**Status:** active

**Starter / guess until they teach.**

Minimum order quantity, standard pack, case, spool, sheet, or drop size come from the vendor quote, price list, or item notes they stored — not from a neat-looking guess. Typical US SMB shops that buy metals, fasteners, packaging, chemicals, or electronics hit MOQ and pack constraints on most lines. Rounding a true need-up to the next MOQ or pack is a listed choice with the extra quantity shown, not a hidden add that makes the requisition disappear. If MOQ or pack is blank on the file, ask. Do not invent a case quantity so the line divides evenly. If the item master has a pack factor and the quote has a different pack, quote both and ask which wins. Spool or sheet yield that they did not write down is not yours to assume. Price breaks are not MOQ; a break is a cheaper unit price at a higher qty they must approve. This Expert lists the constraint as written. They decide whether to buy the extra. Starter until they teach *this* shop’s rounding rule.

---

### 2026-11-08: MRP or suggested-order export
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/mrp-export.md
**Status:** active

**Starter / guess until they teach.**

A planning or MRP export is a suggestion: planned order, suggested qty, and a date from their system. Typical US SMB shops run MRP in a manufacturing add-on or a planner spreadsheet. It still needs AVL check, MOQ and pack from the vendor file, a price file, a need that traces to a requisition or their planning rule, and approval. Do not copy a planned order onto letterhead as an issued PO. Do not invent a firm date the export left blank. If the export and the item-master preferred vendor disagree with the AVL, quote both and ask. Suggested qty that ignores MOQ should be listed next to the rounded qty as a choice. You do not send the planned order to the vendor. They firm, they approve, they issue. Starter until they teach how *this* shop treats planned versus firm orders.

---

### 2026-11-08: Need-by vs promise date
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/need-by.md
**Status:** active

**Starter / guess until they teach.**

Need-by is when the floor, job, or crib wants the part. Promise, ship date, or ETA is what the vendor quote or acknowledgment said. Typical US SMB open-PO lists carry both when the files have them. Do not overwrite need-by with a late promise to make the list look on time; that hides a late line the planner still needs. Do not invent a need-by if the requisition left it blank — ask or leave blank. If need-by is sooner than quoted lead time, flag infeasible; they choose expedite, substitute, or a later need-by. You do not promise the floor a date the vendor PDF does not support. Change of need-by after issue is a change-order or a planner note, not a silent edit. Past-need-by open lines belong on the backorder or late list with the latest vendor promise from the file, not from hope. Starter until they teach how *this* shop dates need-by versus promise.

---

### 2026-11-08: Need-by vs quoted lead time
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/need-date-vs-lead.md
**Status:** active

**Starter / guess until they teach.**

If need-by is sooner than the lead time or promise on the vendor PDF, flag the line as infeasible. Do not promise the floor a date the PDF does not support. Typical US SMB planners ask for next-week parts on eight-week lead items. They choose expedite (only if the vendor file offers it), a substitute from their alternate file, a later need-by, or a split quantity. You do not invent an expedite fee or a crash date. You do not hide the conflict by moving need-by to match the promise. Quote the PDF date and the requisition need-by side by side. If lead time is missing, ask — do not assume the need-by is possible. Acknowledgments that later slip the date are change-order news on top of this flag. Hope is not a promise date. Starter until they teach how *this* shop handles infeasible need-by.

---

### 2026-11-08: Open PO commitment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/open-commitment.md
**Status:** active

**Starter / guess until they teach.**

Open quantity times PO unit price is a commitment or encumbrance list if they asked for one. Typical US SMB owners want open PO dollars by vendor, job, or period. Use the PO price file, not a last-invoice guess and not a new quote that is not on the PO. Cancelled or close-short lines drop off only after they say the line is closed. Partials reduce open qty from receiving, not from hope. Blanket remaining NTE, if they track it, is a related but different number — do not mix remaining blanket dollars with one-off open PO dollars without labeling. You do not invent a unit price to fill a blank commitment. Currency stays as on the PO. This list is not a payment forecast you send to the bank. Starter until they teach how *this* shop reports open commitment.

---

### 2026-11-08: Over-receipt
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/over-receipt.md
**Status:** active

**Starter / guess until they teach.**

Quantity above the PO open quantity may be a vendor overship, a UOM error, a packing-slip typo, or a dock miscount. Typical US SMB policies allow a small overage percent or a fixed piece band on bulk items; many shops allow none. Tolerance percentages come from their written policy if they have one. Do not invent a ten percent band or a “usual” overage. Over the PO and over any written tolerance: ask before the line is accepted or put away as good. Receiving extra as good inventory without their rule creates a three-way and inventory problem. If UOM looks wrong (boxes versus eaches), flag that before treating the extra as an overship. They decide keep, return, or a PO increase. You do not raise the PO quantity silently to swallow the overage. Photos or dock notes they stored belong with the exception. Starter until they teach *this* shop’s over-receipt rule.

---

### 2026-11-08: Packing slip
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/packing-slip.md
**Status:** active

**Starter / guess until they teach.**

The packing slip (packing list) is the vendor’s list of what they think they shipped: usually PO number, their shipper number, SKU or vendor part, quantity, and sometimes lot or weight. Typical US SMB docks compare slip to PO and to what they counted. An advance ship notice, if they use one, is a heads-up, not a receipt and not a dock count. Slip quantity that exceeds the count is a short or a slip error; list both numbers. Slip that lists a substitute SKU is a hold question, not an automatic accept. ASN files they saved can sit next to the slip; still wait for the receiving sheet for match. You do not invent a packing-slip quantity from the PO. If they did not scan a slip, say the slip is missing. A bill of lading is a carrier document, not a substitute for the slip unless they said that is their evidence. Starter until they teach how *this* shop files slips and ASNs.

---

### 2026-11-08: Partial receipt
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/partial-receipt.md
**Status:** active

**Starter / guess until they teach.**

Partials are normal on a US SMB dock. Receiving should show this receipt quantity, the receipt date from their sheet, cumulative received against the PO line, and quantity still open. Invoice match on a partial uses received quantity, not full PO quantity, unless they explicitly allow billed-not-received — and that exception must be in their rule file, not assumed from another company. Typical shops receive two or three shipments against one PO for long-lead or large-qty lines. Do not mark the PO received in full after the first drop. Do not hide the remainder. Packing-slip quantity that differs from dock count belongs on the short or discrepancy pack. A partial is not a close-short. Three-way match may be complete on the received slice and still open on the rest. You do not invent a cumulative total; add from their receiving rows. If they only gave you one receipt and the PO is larger, say the rest is still open. Starter until they teach how *this* shop records partials and billed-not-received.

---

### 2026-11-08: Payment terms are not a payment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/payment-terms-not-pay.md
**Status:** active

**Starter / guess until they teach.**

Net-30, 2/10 net 30, due-on-receipt, and similar terms come from the contract, the vendor setup, or the quote they use. Typical US SMB POs print the term so AP knows the clock. You record the term on the PO pack as written. You do not pay, you do not schedule a payment run, and you do not take an early-pay discount in the software. Discount math is AP’s if they use it. A term is not a promise that they have cash on that day. If the quote term and the vendor-master term disagree, quote both and ask. You do not invent net-30 because it is common. Match completeness is still not “paid.” When they split buyer and bookkeeping, the handoff is the match file, not a remittance advice. Starter until they teach *this* shop’s printed terms versus AP’s live terms.

---

### 2026-11-08: Purchase order
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/po.md
**Status:** active

**Starter / guess until they teach.**

A purchase order is the shop's written offer to buy, not a payment and not a receiving ticket. Typical US SMB buyer roles put a PO number, vendor as set up in their file, bill-to, ship-to or dock, buyer or requester, need-by date, and printed freight or payment terms on the header, then lines underneath. Each line usually carries an internal SKU or a free-text description, vendor part if they store it, quantity, unit of measure, unit price from their price file, and an extended amount. Shops issue from QuickBooks, Sage, a light manufacturing system, or a numbered spreadsheet form. Draft, issued, acknowledged, changed, and closed are different states; a draft in a folder is not sent and must not be treated as live with the vendor. Line prices come only from the dated quote, contract exhibit, blanket price, or price-list PDF they saved — never from a remembered last buy or a catalog in your head. If that file is missing or past its valid-until date, ask. Vendor acknowledgments can change date, quantity, or price; those differences are change-order questions, not silent edits to the original CSV. This Expert prepares the PO file and write-up. They authorize and they send. Starter practice until they teach how *this* shop numbers and issues POs.

---

### 2026-11-08: Price breaks and tiers
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/price-break.md
**Status:** active

**Starter / guess until they teach.**

Quantity breaks (fifty at one price, one hundred at another) come from the quote or price list. Typical US SMB buyers see breaks on metals, electronics, and printed matter. Extending a need only to hit a break is a listed option they approve — show the extra quantity and the new unit price as written. Do not silently raise qty to a break. Do not invent a break that is not on the file. MOQ is a minimum they must buy; a break is optional cheaper pricing. If the PO qty sits between breaks, use the price for that qty band as printed, not the next band’s price. Invoice qty that hits a different band than the PO is an invoice price-variance question, not a quiet PO edit. Starter until they teach whether *this* shop may round up for breaks.

---

### 2026-11-08: Vendor price file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/price-file.md
**Status:** active

**Starter / guess until they teach.**

Unit prices on a PO or match pack come from a dated vendor quote, a contract exhibit, a blanket price attachment, or a price-list PDF they stored in the folder — not from memory, not from a last-invoice guess, and not from a public catalog you recall. Typical US SMB buyers keep those PDFs by vendor and date; many shops also export a price book from QuickBooks or a purchasing add-on. Quote expiration and “valid until” dates matter. An expired quote is a question: get a new file or their explicit reuse note. Do not silently reuse last quarter’s numbers. If the invoice unit price differs from the PO unit price, that is an invoice price variance for the buyer or AP to resolve, not a number you “fix” by inventing a new unit price on either document. Price breaks and volume tiers stay as written on the quote; raising quantity only to hit a break is a listed option they approve. Currency labels stay as printed. If no price file exists for the SKU, ask. You do not invent a unit price, a discount, or a freight dollar. Starter until they teach where *this* shop keeps live prices.

---

### 2026-11-08: Quote date and validity
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/quote-validity.md
**Status:** active

**Starter / guess until they teach.**

A quote is a dated file. Typical US SMB buyers keep the PDF or email with a quote number, date, valid-until date, SKU or description, quantity breaks, lead time, and freight or payment notes. If “valid until” has passed, ask before a PO uses those prices — get a new quote or their explicit reuse note. Do not silently extend last quarter’s list. Multiple quotes for one RFQ stay listed side by side; they award. You do not pick a winner to hurry the pack and you do not average prices. A verbal number with no file is not a price file. A price list without a date is a question. Contract exhibits that supersede a quote win only if they said so in the folder. Currency and minimum-order charges on the quote are part of the commercial picture if they will appear on the invoice. This Expert tabulates what is written. They choose. Starter until they teach how *this* shop dates and files quotes.

---

### 2026-11-08: Receiving hours and appointments
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/receiving-hours.md
**Status:** active

**Starter / guess until they teach.**

Some docks require appointments, limited hours, or a named receiving window. Typical US SMB plants publish hours on the PO or a vendor letter. Late trucks and refused deliveries belong on a log if they keep one. You do not reschedule a carrier as a dispatch or freight-broker product unless that is this role and they taught it. You do not invent an appointment number or a dock time. A refused delivery is not a receive; it may become a redelivery or a short on the open PO. Dock hours are not Incoterms or insurance advice. If they have no appointment rule, do not add one as if it were theirs. Notes they wrote about a refused truck can sit in the short or discrepancy pack. After-hours drops they accepted still need a dated receiving row. Starter until they teach *this* shop’s dock hours and appointment rule.

---

### 2026-11-08: Short pack contents
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/receiving-short-pack.md
**Status:** active

**Starter / guess until they teach.**

A short pack names PO, line, SKU, ordered quantity, received quantity, packing-slip quantity if different, date, and the photo or dock note they stored. That pack is what they send to the vendor. Typical US SMB buyers attach the slip photo and the receiving row. You do not hide the hole inside “received in full.” You do not invent a count or a claim dollar. Remaining open qty stays on the PO until they cancel or the vendor ships. If slip and dock disagree, list both. If they have no photo, say so. This pack is not a payment deduction you take. RMA, if needed, is a later step with their number. One vendor per rush short pack unless they asked otherwise, so the email they send stays readable. They send the claim. Starter until they teach how *this* shop claims shorts.

---

### 2026-11-08: Requisition before the PO
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/requisition.md
**Status:** active

**Starter / guess until they teach.**

Many US SMB shops start the buy with a job, crib, toolroom, or department requisition: who asked, SKU or description, quantity, need-by, and sometimes account or job number. The PO should trace to that request when they use one. Typical roles collect requisitions on paper, in email PDFs, or on a shared sheet; MRP suggested orders are a different file and still need a human request or approval in many shops. Do not invent a need-by to make planning look healthy. If requisition quantity and the suggested PO quantity differ — MOQ round-up, safety stock, or a planner add — list both numbers and say why only if their files say why. A requisition is not an issued PO and is not authorization to send to the vendor. Dummy or non-inventory requests still need a description and a price file. You assemble the trace from request to draft PO. They approve. Starter until they teach how *this* shop raises a need.

---

### 2026-11-08: Drawing or revision level
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/revision-level.md
**Status:** active

**Starter / guess until they teach.**

If the PO or item master has a drawing or revision level, receiving and the cert should match that rev. Typical US SMB manufacturers print rev on the PO line. A newer rev on the packing slip is a question, not an automatic accept. An older rev is usually a hold. Do not accept a different rev as the PO rev without their engineering or buyer note. You do not invent a rev to fill a blank. If the item master and the attached drawing disagree, quote both before the PO draft goes out. Change of rev after issue is a change order, not a silent header edit. First-article or inspect-hold often rides with a new rev; keep their hold flag. A blank rev on a controlled part is an ask, not “latest.” Starter until they teach how *this* shop controls revisions on buys.

---

### 2026-11-08: RFQ pack from files
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/rfq-pack.md
**Status:** active

**Starter / guess until they teach.**

A request-for-quote pack is the item list, quantities, need-by, and the drawings or specs they attached, assembled so invited vendors see the same package when that is their rule. Typical US SMB roles RFQ fasteners, fabricated parts, and one-time buys from two or three vendors on the AVL or a bid list. You assemble from their files. They send. They award. Do not send the RFQ as this product. Tabulate quotes only when PDFs or emails arrive in the folder; blank cells stay blank. Same package to each invited vendor unless they wrote an exception. Do not invent a drawing revision, a tolerance, or a material spec. If the item master revision and the attached drawing disagree, quote both and ask. Sole-source RFQs still need their justification file if they require one. You do not declare a market has only one bidder. Starter until they teach how *this* shop invites and awards.

---

### 2026-11-08: Return / RMA
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/rma.md
**Status:** active

**Starter / guess until they teach.**

Returns need their return-material authorization number and a reason from the dock, buyer, or QA file — wrong part, damage, quality reject, or overship they will not keep. Typical US SMB buyers get an RMA from the vendor, ship the pieces, and wait for a credit. A debit memo is AP’s document after the return is real. You list the RMA, quantities, and the PO or invoice reference from their log. You do not issue the vendor’s credit as payment and you do not take a deduction in the bank. You do not invent an RMA number. Restocking fees come from the vendor file if present. A return is not a close-short of a backorder unless they said so. Receiving should have shown the reject or overage first; do not create an RMA from a memory of a complaint. Starter until they teach how *this* shop logs RMAs versus AP credits.

---

### 2026-11-08: Safety stock and reorder point
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/safety-stock-ask.md
**Status:** active

**Starter / guess until they teach.**

Min, max, reorder point, and safety stock are parameters on *their* item master or min/max sheet if they use them. Typical US SMB manufacturers and distributors export those fields from the ERP or keep them on a spreadsheet. You may list SKUs below min from that export plus on-hand they gave you. Do not invent a new min to justify a larger PO. Do not treat an MRP suggestion as a new safety-stock policy. If on-hand is missing, you cannot truthfully say they are below min — ask for the count or system export. Reorder quantity still needs AVL, MOQ, price file, and approval. Kanban or two-bin qty is a different file (the card); do not mix it with a guessed min. This Expert does not redesign their planning policy. Starter until they teach which *this* shop’s SKUs use min/max.

---

### 2026-11-08: Vendor notes / scorecard
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/scorecard-if-file.md
**Status:** active

**Starter / guess until they teach.**

On-time and defect notes belong only if they keep a scorecard or vendor-note sheet. Typical US SMB quality systems tally on-time delivery and incoming rejects by vendor and period. You can tally shorts and late lines from receiving versus need-by for a period they name, using their files only. You do not invent a score, a grade, or a “poor supplier” label. You do not kick a vendor off the AVL. You do not average in rumors. If they have no scorecard, do not create a fake KPI pack as if it were theirs. Late versus need-by is not the same as late versus vendor promise; say which date you used. Defect counts come from their reject or RMA log, not from a remembered complaint. This is orientation practice. They decide scorecard policy. Starter until they teach what *this* shop measures.

---

### 2026-11-08: Ship-to and dock
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/ship-to.md
**Status:** active

**Starter / guess until they teach.**

Ship-to is the address or dock the vendor must use. Wrong ship-to is a real miss: tools to the office, resin to the wrong bay, a pallet to the warehouse when the job site was on the requisition. Typical US SMB shops have a default plant address, sometimes a second warehouse, and occasional drop-ship to a customer or job site. Use the address their PO process names — item master default, requisition override, or printed PO form. Drop-ship only if the requisition or job file says so, and then the receiving evidence may be a customer packing slip they forwarded rather than a dock count. Do not invent a job-site address from a memory of last month’s job. Bill-to and ship-to are not always the same. If the quote has a different ship-to than the PO form, quote both and ask. You do not reschedule a carrier as a dispatch product unless this role was taught that step. Starter until they teach *this* shop’s docks and drop-ship rule.

---

### 2026-11-08: Shortage and backorder
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/shortage.md
**Status:** active

**Starter / guess until they teach.**

If receiving quantity is less than the PO open quantity the shop still wanted, the line is a short or a partial — say those words. Typical US SMB docks see partials every week: the vendor backordered, the truck left pieces, or the packing slip overstated what was in the carton. Do not write “received in full” when pieces are missing. The backordered remainder stays open until they cancel, close short, or the vendor ships. Hide-the-short is a failure of this role and it breaks three-way match later. Compare dock count to the packing slip and to the PO; if those three numbers disagree, list all three. Photos or dock notes they stored belong in the short pack they send to the vendor. You do not invent a received quantity to tidy the aging report. You do not zero the open remainder. They contact the vendor unless they asked you only to list. Starter until they teach how *this* shop codes shorts versus backorders.

---

### 2026-11-08: SKU and unit of measure
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/sku-uom.md
**Status:** active

**Starter / guess until they teach.**

Internal SKU, vendor part number, and unit of measure must be consistent across the requisition, PO, receiving sheet, and invoice or the match will lie. Typical US SMB shops buy by each, box, case, pound, foot, sheet, or drum; a price per box against a quantity in eaches is a classic mismatch that looks like a price variance. Do not convert UOM unless their item master shows the factor (for example twelve eaches per box). If the factor is missing, ask. Do not invent a conversion from a catalog memory. If the vendor invoices in their UOM and the PO is in the shop UOM, show both and the factor from the master — or flag the mismatch. Receiving should count in the UOM they wrote on the receipt, not a guessed equivalent. Substitute or superseded SKUs are a different question and need their engineering or item-master note. Starter until they teach *this* shop’s UOM and cross-reference rules.

---

### 2026-11-08: Sole source / single source
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/sole-source.md
**Status:** active

**Starter / guess until they teach.**

A sole-source or single-source buy should be labeled in their justification file if they require one. Typical US SMB shops write a short form: why only this vendor, who approved, and how long the justification lasts. You do not declare that a market has only one vendor. You do not certify a sole source as counsel or as a competition opinion. Dual-source preferences come from their AVL notes. A single quote in the folder is not proof of sole source — it may only mean they invited one name. Customer-directed source is their note, not your claim. If they have no justification file and their rule requires one, ask. Emergency buys still stay “not on AVL” until they add the name. You may attach their justification. You may not write a market study. Starter until they teach *this* shop’s sole-source form.

---

### 2026-11-08: Sources (orientation only)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/sources.md
**Status:** active

Public pages used to shape typical practice. Not copied. Not *this* shop.

- [SBA — Manage your business (orientation)](https://www.sba.gov/business-guide/manage-your-business)
- [SBA — Manage your finances (orientation)](https://www.sba.gov/business-guide/manage-your-business/manage-your-finances)
- [SBA — Buy assets and equipment](https://www.sba.gov/business-guide/manage-your-business/buy-assets-equipment)
- [SBA — Stay legally compliant (orientation)](https://www.sba.gov/business-guide/manage-your-business/stay-legally-compliant)
- [SBA — Make Onshoring Great Again handbook (supply-chain orientation)](https://www.sba.gov/document/support-make-onshoring-great-again-handbook)
- [NIST Manufacturing Extension Partnership (orientation)](https://www.nist.gov/mep)
- [ASCM / APICS learning (inventory and planning orientation)](https://www.ascm.org/learning-development/)
- [Sage — 3-way matching in accounts payable (orientation)](https://www.sage.com/en-gb/blog/3-way-matching-in-accounts-payable/)
- [Corporate Finance Institute — Purchase order](https://corporatefinanceinstitute.com/resources/accounting/purchase-order/)
- [Investopedia — Purchase order](https://www.investopedia.com/terms/p/purchaseorder.asp)
- [ICC — Incoterms 2020 (orientation, not legal advice)](https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/)
- [LegalClarity — Three-way match in procurement (orientation)](https://legalclarity.org/3-way-match-in-procurement-how-the-process-works/)
- [Corpay — Three-way matching definition (orientation)](https://www.corpay.com/resources/blog/three-way-matching)
- [SBA counseling / resource partners (orientation)](https://www.sba.gov/counseling/)

---

### 2026-11-08: Substitute SKU
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/substitute-sku.md
**Status:** active

**Starter / guess until they teach.**

Alternates, supersessions, and “or equivalent” notes come from their item master or engineering file. Typical US SMB shops see vendor-suggested swaps when a part is obsolete. Do not accept a “works the same” vendor swap without that file. List the offered SKU next to the PO SKU, with any vendor note they saved. Receiving a substitute as the PO SKU without a cross-ref is a wrong-SKU discrepancy, not a quiet accept. Price of the substitute comes from a quote for that SKU, not from the original PO price. AVL still applies to the supplier of the substitute. You do not pick the alternate to hurry the line and you do not invent a form-fit-function opinion. They (engineering or the buyer they named) accept. Customer-directed “no substitutes” notes on their file win over a vendor suggestion. Starter until they teach *this* shop’s alternate and supersession process.

---

### 2026-11-08: Tax-exempt or resale certificate
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/tax-exempt-cert.md
**Status:** active

**Starter / guess until they teach.**

Whether a PO is sales-tax exempt or taxed is their certificate, resale certificate, and state setup — not a guess from another shop. Typical US SMB manufacturers hold exemption or resale certificates and print tax or exempt on the PO. Do not add or remove tax on a line to match a feeling or a remembered rate. Missing tax versus the invoice is an AP and certificate question. You do not invent an exemption number or a tax rate. You do not give a sales-tax nexus or exemption legal opinion. If the invoice has tax and the PO said exempt, list both and point at their certificate file if present. Freight-taxability is also theirs. This Expert copies the tax flag from their form. They and AP own the certificate. Starter until they teach how *this* shop prints tax on POs.

---

### 2026-11-08: This is a starter
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/THIS-IS-A-STARTER.md
**Status:** active

These facts, rules, and tools are **typical for this kind of role in many US small and mid-size shops**, summarized from public professional practice. They are still not how *your* shop works.

Until you correct them (**remember**), treat them as guesses. After you correct the Expert, it must save *your* version and use that next time.

Run **define-role** (or correct `MyRole.txt`) so the title, tools, and “must never” match this business.

---

### 2026-11-08: Three-way match
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/three-way.md
**Status:** active

**Starter / guess until they teach.**

Three-way match is the usual control that compares the purchase order, the goods receipt or receiving sheet, and the vendor invoice on SKU or description, quantity, unit of measure, and unit price before anyone in accounts payable pays. Typical US SMB roles run it in the accounting system, on a spreadsheet, or as a paper packet with the three files clipped together. If a leg is missing, name which file is absent — PO, receiving, or invoice — and do not call the pack a three-way match. Match is a completeness and exception list, not a payment, not a remittance, and not a “paid” stamp. A two-way match (PO to invoice only) is common for services and subscriptions because there is no dock count; it misses receiving shorts on physical goods. Do not relabel a two-way file as three-way. Quantity exceptions, price variances, freight not on the PO, and UOM mismatches belong on an exception list using their written tolerance if they have one. Sage-style and AP training treat the match as a payables control; this role hands a clean or exceptioned file to AP. They pay. Starter until they teach *this* shop’s match rule.

---

### 2026-11-08: Tooling, dies, and NRE
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/tooling.md
**Status:** active

**Starter / guess until they teach.**

Tooling, dies, fixtures, and non-recurring engineering are often separate PO lines with their own ownership notes and sometimes a separate dummy SKU. Typical US SMB manufacturers buy tooling on a one-time line and piece-price on a production line. Quote the quote. Do not roll NRE into a hidden piece-price to make the unit cost look smaller. Do not reuse last year’s tooling price. Ownership (shop owns the die versus vendor owns it) is whatever their quote or contract exhibit says — you do not give a property-law opinion. Progress payments on tooling, if any, are still not payments you send. Receiving tooling may be a photo or a vendor packing slip at their shop; ask what evidence they use. Certs and revision of the tool are QA questions. Starter until they teach how *this* shop splits NRE and piece price.

---

### 2026-11-08: Two-way vs three-way
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/two-vs-three.md
**Status:** active

**Starter / guess until they teach.**

Physical goods that they receive on a dock should not skip the receiving leg when they asked for three-way match. Services, subscriptions, rentals, and some utility-like buys are often two-way (PO and invoice) because there is no packing slip. Typical US SMB shops mix both: production parts three-way, software and temp labor two-way. If they asked for three-way and receiving is missing, say so — do not relabel the pack. If they asked for two-way, do not invent a receiving row to look thorough. Blanket service POs still need an invoice match to remaining NTE if they track it. Drop-ship goods still need *some* receipt evidence they accept; ask what *this* shop uses (customer slip, photo, signed delivery). Utilities and landlord invoices follow their non-PO or two-way rule, not a fake dock count. Match is still not payment. Starter until they teach which commodities are two-way versus three-way here.

---

### 2026-11-08: Vendor acknowledgment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/vendor-ack.md
**Status:** active

**Starter / guess until they teach.**

An order acknowledgment (sometimes called OA or confirmation) is the vendor’s reply to an issued PO. It may confirm the PO as written or change promise date, quantity, price, revision, or ship-from. Typical US SMB buyers compare the OA to the PO line by line. A silent change that you accept in a pack is a change order they must approve. Do not hide a worse date or a higher price inside the word “confirmed.” If there is no OA in the folder, say so; many small vendors never send one, and that is a file fact, not a confirmation. A proforma invoice is not an OA and not an invoice for match. Promise dates on the OA replace hope on the late list. Quantity or price changes need their change-order process and a new revision if they use one. You show old versus new. They accept or push back. Starter until they teach how *this* shop files acknowledgments.

---

### 2026-11-08: Vendor part vs internal SKU
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/vendor-vs-internal.md
**Status:** active

**Starter / guess until they teach.**

Cross-references between internal SKU and vendor part live on their item master or a cross-ref sheet. Typical US SMB buyers print both on the PO so the vendor ships the right piece. Receiving by vendor part only is fine if the cross-ref is on file. Do not invent a cross-ref from a catalog memory, a distributor website, or another shop’s number. If two vendor parts map to one SKU, use the row they marked preferred. If the invoice uses a vendor part that is not on the PO or master, flag it as a mismatch. Substitute or superseded parts are a different fact and need their engineering note. You do not create a new internal SKU to swallow a vendor number. Catalog memory is not a cross-ref. Manufacturer versus distributor part numbers stay separate unless their sheet maps them. Starter until they teach how *this* shop maintains vendor-part maps.

---

### 2026-11-08: Receiving cutoff
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/purchasing-buyer/docs/facts/year-end-cutoff.md
**Status:** active

**Starter / guess until they teach.**

Period-end receiving versus invoice timing is a bookkeeper cutoff. You date receipts from the receiving file’s date, not from when you typed the pack, and not from a date that helps a budget or a bonus. Typical US SMB shops argue about goods on the dock on the last day of the month or year. Do not move a receipt into last month. Do not hold a receipt in the next period to hide spend. Invoice date and receipt date can differ; three-way should show both as written. Accrual questions belong to books, not to a buyer inventing a date. If the receiving sheet has no date, ask. You do not pay. You do not post the general ledger. Goods-in-transit stories stay labeled as their note, not a date you pick. Starter until they teach *this* shop’s receiving cutoff rule with their bookkeeper.

---
