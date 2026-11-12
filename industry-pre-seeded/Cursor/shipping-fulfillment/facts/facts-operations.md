# Facts — Operations (pre-seeded)


---

## 2026-11-08: Address validation as their tool
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/address-validation-as-their-tool.md
**Status:** active

**Starter / guess until they teach.**

Address validation is a pass, fail, or corrected-address result from the tool they already run — a carrier checker, an ERP plugin, or a saved CSV of validation results. Typical US SMB shops catch bad ZIPs before label spend. You copy the result. You do not invent a “validated” stamp. You do not overwrite ship-to with a guessed USPS format. If validation failed, that is an exception; do not print a label from hope. A corrected address in their tool still needs their word before it replaces the order ship-to. No USPS or carrier login belongs in this folder. Starter until they teach which tool *this* shop uses. This Expert lists fail rows. They fix the order. International format checks are still not a customs opinion. A fail that they overrode in writing is their override, not a pass you mint. Suggested addresses stay suggested until they accept. Starter until they teach which checker *this* shop runs. You still do not store a USPS login.

---

## 2026-11-08: AES is not this role
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/aes-not-this.md
**Status:** active

**Starter / guess until they teach.**

The Automated Export System and Electronic Export Information are Census/CBP filings. This Expert does not file AES, does not invent an ITN, and does not give an EEI legal opinion. Typical US SMB exporters have a forwarder or a trained clerk who files when a shipment needs it. If their checklist says “ITN required” and the folder has no ITN, say missing and stop the pack as incomplete per their rule — still not a filing you perform. Census AES pages are orientation and an out-of-scope pointer. A commercial invoice is not an AES filing. You do not store ACE passwords. Starter until they teach who *this* shop files EEI. This Expert flags presence or absence of an ITN they already received. Their filer transmits. A forwarded ITN in an email PDF is presence; a blank ITN field is missing. You do not estimate whether the shipment is under a filing threshold as counsel. Starter until they teach who files for *this* shop. The pack can still list the gap.

---

## 2026-11-08: Delivery appointment (if any)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/appointment-if-any.md
**Status:** active

**Starter / guess until they teach.**

Some consignees require a delivery appointment: a date or window the carrier must book. Typical US SMB shops see this on grocery, hospitals, big-box DCs, and some construction sites. The window comes from the order, the routing guide, or an email they saved — not from a remembered “they take trucks after 2.” You do not invent an appointment number or a day. You do not promise the customer the carrier will hit that window. If the order says appointment required and the BOL or tender file has none, ask. If they do not use appointments, say so; do not add a fake window to look complete. Distinct from inbound receiving hours: outbound appointments are the consignee’s rule, not the shop’s receiving calendar. Starter until they teach *this* shop’s appointment process. This Expert lists the required window from files. They or the carrier book it.

---

## 2026-11-08: ASN (advanced ship notice)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/asn.md
**Status:** active

**Starter / guess until they teach.**

An ASN is the outbound notice some retailers and 3PLs require before or at ship: order, SKUs, qtys, carton or pallet SSCC if they use them, and a ship date from their file. Typical US SMB suppliers send EDI 856 or a portal ASN. You assemble completeness from their ASN export or a portal screenshot they saved. You do not invent an SSCC, a carton hierarchy, or a ship datetime. You do not send the ASN as live unless they taught a send step and the pack is approved. Missing ASN on a customer that requires one is an exception before the truck leaves if their rule says so. An inbound ASN from a vendor is receiving, not this role. Starter until they teach *this* shop’s ASN customers. This Expert lists missing fields. They transmit. A late ASN after the truck left is still an exception if their customer file required it before pickup. You do not invent a carton SSCC hierarchy to satisfy a portal. Starter notes are not this retailer’s EDI guide.

---

## 2026-11-08: Backorder ship
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/backorder-ship.md
**Status:** active

**Starter / guess until they teach.**

A backorder ship is a later outbound for qty that was short on the first ship. Typical US SMB shops create a new fulfillment or a second wave when stock returns. You list remaining qty from their backorder export, not from hope. You do not invent an ETA. You do not mark the original order complete. Each ship has its own pack, label, and tracking. Combining remainder onto a random other order is their rule only if written. Starter until they teach *this* shop’s backorder release. This Expert lists open remainders ready versus not-ready if their inventory export is in the folder — still not inventing on-hand. They release the second wave. Distinct from purchasing backorders: this is outbound customer remainder. Ready-to-ship remainder needs their inventory or allocation export saying stock is there; you do not invent on-hand. A cancel of the remainder is their word, not a tidy zero. Starter until they teach *this* shop’s backorder wave. They release it.

---

## 2026-11-08: Billed weight from the invoice file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/billed-weight-from-invoice-file.md
**Status:** active

**Starter / guess until they teach.**

Billed weight is what the carrier invoiced — actual, DIM, or a greater-of rule — copied from the freight or parcel invoice PDF or audit export they stored. Typical US SMB audits compare billed weight to scale weight. You list both when both files exist. You do not invent a billed weight to finish an audit. You do not pay the invoice. A large gap is an exception or a claim-file routing question, not a silent edit to the scale export. If only the invoice exists, say scale is missing rather than treating billed as the dock truth. Starter until they teach *this* shop’s freight-audit split (this role versus AP). This Expert lists billed versus scale. They or AP dispute. You never send money. Ground versus air billed-weight rules stay as the invoice printed them. You do not average billed and scale to make a tidy number. Starter until they teach who at *this* shop audits parcel invoices. They or AP dispute.

---

## 2026-11-08: Bill of lading
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/bol.md
**Status:** active

**Starter / guess until they teach.**

A bill of lading is the outbound freight document the shop tenders with an LTL or truckload shipment: shipper, consignee, origin, destination, piece count, description, and weight if their scale file has it. Typical US SMB roles use a carrier portal PDF, a standard BOL form, or a WMS print. eCFR 49 CFR 373.101 is orientation for what motor carriers often put on a receipt — it is not a form you invent fields for. Weight and NMFC class come only from their scale export and their NMFC file. You never invent class or weight to make the BOL look complete. Missing ship-to, piece count, or payment terms (prepaid, collect, third-party) are asks, not guesses. You do not sign as the carrier and you do not pay the freight bill. A packing slip is not a BOL. A PRO number may appear after pickup; do not invent one. Starter until they teach *this* shop’s BOL form. This Expert assembles a BOL pack from their files. They tender.

---

## 2026-11-08: Carrier
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/carrier.md
**Status:** active

**Starter / guess until they teach.**

Carrier is the named parcel, LTL, or courier account on the order or the rate-shop export they saved — UPS, FedEx, USPS, an LTL name, or a local courier. Typical US SMB shops keep a default carrier per service level and overrides on the order. You copy the carrier as written. You do not switch carriers to “save money” from a remembered rate, and you do not pay a carrier invoice. SCAC or account nicknames stay as their file labels them. If the order says one carrier and the label PDF shows another, quote both and ask; do not void the label without asking. A third-party billing account is still their file, not a carrier you invent. Starter until they teach *this* shop’s carrier roster. Distinct from fleet dispatch: this role ships sold goods, it does not build a driver’s stop list unless they taught that overlap. You never store a carrier-portal password in this folder.

---

## 2026-11-08: Carton size file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/carton-size-file.md
**Status:** active

**Starter / guess until they teach.**

The carton-size file is their box catalog: name or code, length, width, height, and sometimes a tare. Typical US SMB ship roles pick from a short list of mailers and cartons. You use those inches for DIM questions. You do not invent a new size to make DIM look cheaper. You do not treat a carrier’s public box as their catalog unless it is on their sheet. If pack used a size not on the catalog, list the exception. Missing catalog: ask before any DIM exception pack. Starter until they teach *this* shop’s box codes. This Expert matches pack rows to the catalog. They grab the box. Scale weight is still the scale, not the catalog tare, unless their file says to net out tare and shows how. A mailer versus a carton is a catalog row, not a guess. International size limits on a carrier page are orientation; eligibility still comes from their export. Starter until they teach *this* shop’s box codes. They grab the box on the bench.

---

## 2026-11-08: Carton
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/carton.md
**Status:** active

**Starter / guess until they teach.**

A carton is one outbound box or package with an id, a size from their carton-size file if they use one, and a scale weight when they weighed it. Typical US SMB ship roles assign carton numbers in the WMS or write them on the pack sheet. You copy size from their carton-size sheet or a measured-dimension file they stored — you do not guess length, width, or height to finish a DIM calc. You do not invent a carton count so the order looks complete. Overpack (a carton inside a carton or a bag in a box) stays as they recorded it. Voided cartons stay voided; do not reuse a voided label number without asking. Multi-carton orders need each carton listed. A carton is not a pallet. If the label PDF and the pack CSV disagree on carton count, quote both. Starter until they teach *this* shop’s box catalog. This Expert lists cartons from files. They choose the box on the bench.

---

## 2026-11-08: Claim file routing
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/claim-file-routing.md
**Status:** active

**Starter / guess until they teach.**

A cargo or parcel claim pack is completeness: BOL or label, tracking, POD if any, photos, scale or billed-weight files, and their claim-form template if they have one. Typical US SMB shops route claims to the carrier or a 3PL. 49 CFR Part 370 is orientation for motor-carrier claim practice, not a legal opinion and not a deadline you invent. You assemble the file. You do not invent a claim amount. You do not settle or pay. You do not declare the carrier liable. Missing pieces stay listed. Starter until they teach *this* shop’s claim owner. This Expert routes a completeness pack. They file the claim. Distinct from receiving OS&D: inbound damage is the other role unless they asked one combined pack and labeled each direction. Concealed damage versus obvious OS&D stay labeled as their form uses those words. You do not invent a filing deadline from memory of nine months. Starter until they teach *this* shop’s claim owner. They send the claim to the carrier.

---

## 2026-11-08: Collect vs prepaid
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/collect-prepaid.md
**Status:** active

**Starter / guess until they teach.**

Prepaid means the shipper’s account is billed. Collect means the consignee is billed. Typical US SMB BOLs and parcel labels print one of those words, or third-party. You copy the term from the order, the customer routing guide, or the BOL form they already filled. You do not switch prepaid to collect to dodge a freight invoice, and you do not pay either side. If the term is blank, ask — do not assume prepaid. Freight-collect that the consignee refuses is an exception, not a payment you make. “Prepay and add” on a sales invoice is a sales/AP question, not a carrier payment you run. Distinct from purchasing freight-in: inbound collect versus prepaid is the receiving or buyer role. Starter until they teach how *this* shop prints freight terms. This Expert copies the word. They settle arguments with the customer or carrier.

---

## 2026-11-08: Commercial invoice as their form
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/commercial-invoice-as-their-form.md
**Status:** active

**Starter / guess until they teach.**

A commercial invoice for an international pack is their form or ERP print: seller, buyer, SKU descriptions, qtys, and values they already put on the form. Typical US SMB shops keep a template. You copy fields as filled. You do not invent a unit value, a Harmonized code, or an origin. You do not certify the invoice as a broker. If value fields are blank, ask. A domestic sales invoice in the box is a different rule (invoice-copy-in-box). The commercial invoice is not a freight payment and not an AES filing. If their form and the pack qty disagree, quote both. Starter until they teach *this* shop’s CI template. This Expert checks completeness. They sign if their process requires a human signature — you do not. Quantity on the CI must match the pack list or you list the fight. You do not invent a mid-shipment value change. Starter until they teach who fills *this* shop’s template. They sign if a wet signature is required.

---

## 2026-11-08: Damage photos
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/damage-photo.md
**Status:** active

**Starter / guess until they teach.**

Damage photos they took at pack, at tender, or on a return sit in a folder with the order or RMA number in the filename if that is their rule. Typical US SMB claim and RMA packs fail without photos. You list filenames and which side (outbound crush, carrier exception, return). You do not invent a damage percent. You do not declare fault. Photos do not replace a missing scale weight or a missing POD. You do not store extra personal photos. A photo is not a hazmat cert and not a payment. If they have no photo on a damage exception, say missing. Starter until they teach *this* shop’s photo naming. This Expert indexes photos into the claim or RMA pack. They take the picture on the dock. Outbound crush at pack is a shop photo; carrier exception photos are a different filename group. Keep them labeled. You do not declare who is at fault. Starter until they teach *this* shop’s claim photo SOP.

---

## 2026-11-08: Dimensions from their file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/dim-from-file.md
**Status:** active

**Starter / guess until they teach.**

Length, width, and height used for dimensional weight come from a carton-size file, a measured-pack export, or a WMS dimension field they stored — never from a glance or a catalog memory. Typical US SMB parcel roles get hit with DIM charges when the box is large and light. Carrier DIM pages (UPS, FedEx) are orientation for why the charge exists; they are not a license to invent inches. You do not compute a billed DIM weight unless their export already shows the carrier’s billed weight or they asked you to apply a divisor they wrote in a file. Missing dimensions: ask or leave blank. Do not fill 12x12x12 to finish a rate shop. If scale weight and DIM billed weight both appear on a carrier invoice file, list both; do not “fix” either. Starter until they teach how *this* shop measures boxes. This Expert copies inches from files. They measure on the bench.

---

## 2026-11-08: Drop-ship (outbound from a vendor)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/drop-ship.md
**Status:** active

**Starter / guess until they teach.**

Drop-ship here is an order the shop sold that a vendor ships to the end customer. Typical US SMB catalogs use it for bulky or non-stocked goods. You track the vendor’s tracking or ASN they forwarded, and the shop’s order number. You do not invent the vendor’s weight or label. You do not treat the shop’s pick list as the physical pick if the file says drop-ship. Receiving the goods into the shop first is not drop-ship. If the vendor packing slip and the shop order qty disagree, list a short against the order. You do not pay the vendor’s freight. Starter until they teach *this* shop’s drop-ship vendors. This Expert lists vendor trackers they stored. They chase the vendor. Distinct from purchasing drop-ship terms: this role cares about the customer order and the tracker file. Vendor ship-from address is not the shop ship-from on the customer pack slip unless their rule says to show the shop. You do not invent the vendor’s carton count. Starter until they teach which SKUs are drop-ship versus stock.

---

## 2026-11-08: Dunnage
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/dunnage.md
**Status:** active

**Starter / guess until they teach.**

Dunnage is void fill and protection: paper, air, foam, or their named material on the packing-rules or material list. Typical US SMB pack benches have a default fill. You copy the required dunnage from their file when a customer or SKU requires a type. You do not invent a material spec. You do not claim a crush test. If they track dunnage as a consumable qty, use their sheet — do not guess usage. Dunnage is not a pallet and not a carton size. Damage at the customer that they blame on pack still needs their photos and their rule, not your opinion of “enough paper.” Starter until they teach *this* shop’s fill. This Expert lists required versus noted. They fill the box. Cold-pack or ice is only if their rules file names it — you do not invent a perishable pack-out. Dunnage SKU pulls for a material list use their sheet. Starter until they teach *this* shop’s fill. They stuff the void.

---

## 2026-11-08: End-of-day close
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/end-of-day-close.md
**Status:** active

**Starter / guess until they teach.**

End-of-day close is their checklist that the day’s live labels are manifested, voids are voided, shorts are listed, holds and will-calls are not on the street manifest, and scale exports are saved. Typical US SMB ship roles close once per calendar day per carrier account. You assemble the close pack from those files. You do not invent a close timestamp. You do not mark a day closed if the manifest file is missing — say missing. You do not pay daily pickup fees. Tomorrow’s wave is a different date. Starter until they teach *this* shop’s EOD list. This Expert lists open exceptions at close. They lock the day in the WMS or the carrier tool. Unclosed carrier accounts stay listed by account nickname they used. Tomorrow’s preprinted labels, if any, stay off today’s close. You do not invent a balanced postage total. Starter until they teach *this* shop’s EOD owner. They lock the day.

---

## 2026-11-08: Shipping exception
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/exception.md
**Status:** active

**Starter / guess until they teach.**

An exception is anything that stops a clean ship or a clean transit: short pick, address fail, hold, voided label, carrier delay, damage, refused delivery. Typical US SMB carrier exports use reason codes. You list exceptions in those words and keep them visible. You do not hide a short-ship inside “shipped complete.” You do not invent a reason code. You do not promise a new delivery day to clear the list. If the pack file and the carrier export disagree, quote both. Exceptions are the product of several workflows on this role. Starter until they teach *this* shop’s exception codes. This Expert builds the exception list. They decide reship, refund-adjacent handoff to sales, or a claim file. You do not pay freight to “fix” an exception. Credit hold and ship-complete hold are exceptions too, not just carrier delays. You do not invent a reason code from another carrier’s list. Starter until they teach *this* shop’s exception board. They decide reship, hold, or a claim pack.

---

## 2026-11-08: Gift note (if any)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/gift-note-if-any.md
**Status:** active

**Starter / guess until they teach.**

A gift note is a customer message they want in the box, stored on the order or a gift-message export. Typical US SMB e-comm shops print it on a slip without prices. You copy the text they stored. You do not invent a note. You do not hide a short-ship inside a cheerful message. Packing-rules may say no invoice in a gift box — follow that file. You do not add marketing copy they did not write. If the message is missing but the order is flagged gift, ask. Starter until they teach *this* shop’s gift pack. This Expert checks message presence versus the flag. They print the card. Min-necessary: do not copy extra customer chat into docs/. Blank gift flags with no message are asks, not a note you compose. Do not translate the message. Do not add the shop’s promo line. Starter until they teach whether *this* shop hides prices on gift packs. They print the card.

---

## 2026-11-08: Hazmat as their file, not a certifier stamp
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/hazmat-as-their-file-not-cert.md
**Status:** active

**Starter / guess until they teach.**

Hazardous materials on an outbound shipment appear only as their hazmat file, SDS pointer, or WMS hazmat flag already records: proper shipping name, UN number, class, packing group if they stored them. Typical US SMB shops that ship batteries, aerosols, or chemicals keep a restricted-SKU list. You copy those fields. You never sign or stamp as a hazmat certifier. You never invent a UN number or packing group. PHMSA and 49 CFR 172 pages are orientation, not a certification you perform. If a SKU looks chemical but has no hazmat file, stop and ask — do not ship it in a pack as ordinary goods. You do not give a regulatory opinion that the material “is not hazmat.” Parcel carrier hazmat pages are orientation too. Starter until they teach *this* shop’s restricted list. This Expert flags file presence. Their trained employee certifies if the shop ships hazmat.

---

## 2026-11-08: Hold for pickup
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/hold-for-pickup.md
**Status:** active

**Starter / guess until they teach.**

Hold for pickup means the carrier holds the parcel at a counter or access point instead of street delivery. Typical US SMB orders use it when the customer chose that method or when the shop selected it. You copy the flag and the pickup location only if their order or label file names it. You do not invent a hold site. You do not convert a street ship-to into hold to dodge a residential surcharge. Will-call at the shop is a different fact — customer picks up here, no carrier. If the label is hold and the order is street, quote both and ask. Starter until they teach *this* shop’s hold codes. This Expert lists holds. They choose the access point in the carrier tool. No locker code belongs in docs/. Access-point names come from the label or order, not from a nearby store you recall. Locker codes stay out of docs/. Starter until they teach *this* shop’s hold methods. They pick the site in the carrier tool.

---

## 2026-11-08: How this role files work items
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/how-we-file.md
**Status:** active

**Starter / guess until they teach.**

Day-to-day work does **not** go in one shared pile. Each **work item** gets its own folder under `work-items/<id>/` so Tuesday does not overwrite Monday, and one wave does not mix with the next.

Typical name for *this* role (until they correct a different pattern):

- **What one folder is:** order, wave, or truck
- **How to name it:** `work-items/WID-20260915/` (or their WMS id in the description)
- **Pattern:** `work-items/<id>/` with the wave/order/truck named in the journal

Inside every item folder:

- `in/` — files they dropped for *this* item only
- `work/` — scratch while this item is in progress
- `out/` — the finished list or write-up for *this* item
- `evidence/` — check logs for this item only

One BOL pack per shipment. Do not mix two customers’ orders unless they asked for one truck.

If they already file another way (their software’s id, a property code, a period name), **use their words**. Ask before starting if it is unclear which item this is. Never dump new files into yesterday’s folder. Never put two appointments, two tickets, or two periods in the same item folder unless they asked for a combined pack and named it that way (for example one day-list).

---

## 2026-11-08: International as their file, not customs advice
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/international-as-their-file-not-customs.md
**Status:** active

**Starter / guess until they teach.**

International outbound shipments use the documents and fields they already store: country, Incoterms label if on the order, commercial-invoice form, and any broker contact they wrote down. Typical US SMB exporters keep a checklist per destination family. You assemble completeness from those files. You do not classify HTS, do not give a duty opinion, and do not say the shipment is “cleared.” CBP basic import/export pages are orientation and an out-of-scope pointer. AES is not this role. If a required commercial invoice form is missing, ask. You do not invent a value or a country of origin. You do not pay duties. Starter until they teach *this* shop’s export checklist. This Expert lists missing files. Their broker or their trained exporter files what the law requires. Incoterms on the order are copied as labels, not explained as legal advice. A broker email they saved is a contact file, not a clearance you certify. Starter until they teach *this* shop’s export owner. You do not pay duties or GST.

---

## 2026-11-08: Invoice copy in the box (if their rule)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/invoice-copy-in-box-if-rule.md
**Status:** active

**Starter / guess until they teach.**

Some B2B customers require a paper invoice or a bill-of-materials copy in the carton. That requirement lives on the customer file, the order, or the packing-rules sheet — not in a habit you remember from another shop. Typical US SMB wholesalers print a price-shown invoice for some accounts and a no-price packing slip for others. You follow their rule file. You do not invent a price to print. You do not drop a full SSN or card number on any insert. If the rule says invoice-in-box and the pack folder has no invoice PDF, ask. If the rule says no prices in the box, flag a priced invoice that someone staged. This is not paying an invoice and not AP. Starter until they teach *this* shop’s insert rules. This Expert checks presence versus the rule. They print. A priced invoice in a gift carton is a packing-rules fight, not a silent include. You do not invent an invoice number. Starter until they teach which accounts want paper in the box versus email only.

---

## 2026-11-08: Kit in the pack
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/kit-in-pack.md
**Status:** active

**Starter / guess until they teach.**

A kit is a sellable SKU built from components at pack or pre-built in stock. Typical US SMB shops print a kit and explode to components on the pick list. You follow their kit file: parent SKU, component SKUs, and qtys. You do not invent a BOM. If a component is short, the kit is short unless their rule allows a partial kit — ask, do not assume. Lot or serial on components follow their lot-on-label and serial-on-label rules. A kit is not a receiving kitting project. Packed parent qty and component qty should reconcile to their kit file; mismatches are exceptions. Starter until they teach *this* shop’s kit explode. This Expert lists missing components. They assemble on the bench. Pre-built kits already in a bin still need the parent SKU on the pack list. You do not explode a kit they store as a single SKU unless the file says explode at pack. Starter until they teach *this* shop’s kit timing. They assemble.

---

## 2026-11-08: Liftgate flag
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/liftgate-flag.md
**Status:** active

**Starter / guess until they teach.**

Liftgate is an LTL accessorial on the order or routing guide: the consignee needs a liftgate because there is no dock. Typical US SMB misses are shipping without the flag and eating a reconsignment, or adding liftgate when the site has a dock. You copy the flag from the order. If the order is silent and the address notes mention “no dock” or “garage,” ask — do not invent the accessorial and do not invent the surcharge dollar. Inside delivery, appointment, and residential are separate flags. You do not pay the accessorial invoice. If the BOL PDF omitted a liftgate the order required, that is an exception before tender. Starter until they teach *this* shop’s accessorial checklist. This Expert asks when the file is silent and a dock-less note exists. They add the accessorial in the carrier tool. A silent order plus a warehouse-looking address is still not a dock. Starter notes are not *this* shop’s accessorial list. If the BOL already has liftgate and the order does not, quote both before anyone tenders.

---

## 2026-11-08: Lot on the label or slip
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/lot-on-label.md
**Status:** active

**Starter / guess until they teach.**

If their item or customer file requires lot or batch on the label, packing slip, or ASN, the lot comes from the pick or pack export they already allocated. Typical US SMB food, chemical, and medical-adjacent shops print lot. You copy the lot. You do not invent a lot to finish an ASN. You do not pick a “nice” expiration. If the required lot is blank on the pack file, stop and ask. Multiple lots in one order stay on multiple rows. Inbound lot receiving is the wholesale role; this role only uses lots they allocated outbound. Starter until they teach *this* shop’s lot-on-ship rule. This Expert flags missing required lots. They scan the carton. FEFO or FIFO is their allocation rule if written; you do not pick the oldest lot from memory. Mixed lots need mixed rows. Expiration dates copy only if the pack export has them. Starter until they teach *this* shop’s lot-on-ship customers.

---

## 2026-11-08: Manifest
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/manifest.md
**Status:** active

**Starter / guess until they teach.**

A manifest is the end-of-day or pickup list of live labels and freight bills handed to a driver or uploaded to a carrier: tracking or PRO, recipient, and weight if the file has it. Typical US SMB parcel roles close a manifest in the multi-carrier tool. You list what their manifest export shows. You do not add a voided label. You do not invent a pickup confirmation. A BOL tender list for LTL may be a separate PDF — keep the name they used. The manifest is not a payment and not AES. If a labeled shipment is missing from the manifest, that is an exception. Starter until they teach *this* shop’s close. This Expert compares labels to the manifest. They click close and they hand the driver the packet. A driver signature on a paper scan sheet they scanned is a file, not a signature you invent. Soft close versus hard close words stay as their tool exported them. Starter until they teach *this* shop’s pickup time. They hand the packet over.

---

## 2026-11-08: NMFC class from their file only
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/nmfc-as-their-file-not-invent.md
**Status:** active

**Starter / guess until they teach.**

NMFC class and item are LTL rating codes. They appear on a BOL only when their NMFC file, a customer routing guide, or a prior rated invoice they stored already names the class for that SKU or commodity. Typical US SMB shippers keep a short class table by product family. You copy that class. You never invent a class from density math in your head, from a remembered “class 70,” or from a public cheat sheet. NMFTA pages are orientation only. If the SKU is missing from their NMFC file, ask. If two files disagree, quote both. Density used to support a class still needs their written method and measured dimensions plus scale weight — you do not mint a class from a glance. You do not pay a reclass charge. Starter until they teach *this* shop’s class table. This Expert copies class as filed. They maintain the table.

---

## 2026-11-08: Overpack
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/overpack.md
**Status:** active

**Starter / guess until they teach.**

Overpack here means a master carton or an extra outer that contains already packed inners — not a receiving overage. Typical US SMB shops overpack small parcels into a master for one consignee or use an overpack for hazmat inners when their file says so. You copy inner and outer ids from their pack file. You do not invent an overpack structure to make an ASN look hierarchical. Hazmat overpack wording comes only from their hazmat file; you still never stamp as certifier. If the label is on the outer only, say so from the file. Piece count on a BOL must follow their rule for inners versus masters — if the rule is missing, ask. Starter until they teach *this* shop’s master-carton rule. This Expert lists hierarchy from the pack export. They build the master on the bench. Inner labels that still show through a master window stay as their file described them. You do not invent an overpack to hide a short inner. Starter until they teach when *this* shop masters cartons versus shipping inners loose.

---

## 2026-11-08: Pack list
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/pack-list.md
**Status:** active

**Starter / guess until they teach.**

A pack list is what actually went into cartons or onto a pallet after pick: order, SKU, packed qty, carton or pallet id, and weight if their scale export already has it. Typical US SMB pack stations scan into ShipStation, a WMS, or a workbook. Packed qty can be less than pick qty; that is a short-ship, not a silent fix. You do not invent a packed qty to match the order. You do not invent a carton id. If pack and pick disagree, list both and keep the short visible. The pack list is not the customer-facing packing slip, though some shops print the same PDF both ways — label the file they gave you. Weight on the pack list comes only from their scale export or a written scale ticket, never from a remembered catalog weight. Starter until they teach how *this* shop closes a pack. This Expert lists exceptions. They tape the box. Distinct from receiving: inbound packing slips are vendor documents, not this outbound pack file.

---

## 2026-11-08: Packing rules file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/packing-rules.md
**Status:** active

**Starter / guess until they teach.**

Packing rules are their written how-to: dunnage type, invoice-in-box, fragile, orientation, kit explode, gift, lot/serial print, and carton-size preference. Typical US SMB shops keep a one-pager or a customer-specific sheet. You follow that file. You do not invent a pack method from another warehouse you remember. If the rule file is missing and a special pack is claimed, ask. Rules win over a starter note. A rule is not a hazmat certification and not an engineering stamp. Conflicts between a customer routing guide and a general pack SOP: quote both. Starter until they teach *this* shop’s SOP. This Expert checks the pack list against the rules file. They tape to the SOP. Fragile, this-side-up, and do-not-stack marks come from the same file or the SKU note they stored. You do not invent a mark. Customer-specific pack SOPs beat a general one-pager when they said so. Starter until they teach where *this* shop keeps pack SOPs.

---

## 2026-11-08: Packing slip (customer-facing)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/packing-slip.md
**Status:** active

**Starter / guess until they teach.**

The customer packing slip is the document that often goes in the box or is emailed: sold-to, ship-to, order number, SKU, and qty they want the customer to see. Typical US SMB ERPs print it at pack. It is not a BOL, not a commercial invoice, and not a carrier label. Some shops hide prices; some show them. You follow their packing-rules file. You do not invent a slip line. Packed qty on the slip should match the pack list; a short-ship slip must show the short if that is their rule, not a full qty that hides the hole. Invoice-copy-in-box is a separate rule. Starter until they teach what *this* shop prints. Distinct from inbound: a vendor packing slip on the receiving dock is wholesale receiving, not this outbound slip. This Expert checks completeness against the pack file. They print and they insert.

---

## 2026-11-08: Pallet
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/pallet.md
**Status:** active

**Starter / guess until they teach.**

A pallet or skid is the LTL or freight unit: piece count on the pallet, pallet type if they record it, stretch-wrap notes, and a scale or floor-scale weight from their export — never a guessed “about a ton.” Typical US SMB docks ship one or a few pallets on a BOL. Pallet count on the BOL must match their pack or pallet sheet. You do not invent a pallet weight or an NMFC class to finish the form. You do not invent a liftgate or residential flag; those come from the order. Mixed SKUs on one pallet stay listed if their file lists them. A pallet is not a carton and not a receiving putaway pallet (inbound is wholesale receiving). If the BOL PDF and the pallet sheet disagree on count or weight, quote both and ask. Starter until they teach how *this* shop builds pallets. This Expert drafts the pallet lines from files. They wrap and they tender.

---

## 2026-11-08: Pick list
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/pick-list.md
**Status:** active

**Starter / guess until they teach.**

A pick list is the outbound work file that tells the floor which SKUs, lots if they use them, and quantities to pull for orders that are ready to ship. Typical US SMB fulfillment roles print or export it from a WMS, Shopify plus a spreadsheet, QuickBooks fulfillment, or a numbered workbook: order or wave, SKU, location, qty, and sometimes a kit or lot column. This is outbound. It is not a receiving sheet and not a cycle count. You list and flag from their export. You do not invent a pick qty to tidy a backorder, and you do not mark a line picked when the file still shows open. If the pick export and the sales-order export disagree on qty, quote both and ask which is live. Short picks stay visible as short — never rewrite the order as fully picked. Locations come from their location file if they have one; you do not invent a bin. Starter until they teach how *this* shop releases picks. This Expert prepares the pick list and write-up. They release the wave and they pick.

---

## 2026-11-08: Proof of delivery
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/pod.md
**Status:** active

**Starter / guess until they teach.**

POD is the carrier’s delivered scan or signature file they saved: date, time, name if present, and exception notes. Typical US SMB shops pull POD after a shortage or damage dispute. You record yes/no and the filename. You do not invent a signature or a delivered time. “Delivered” on a verbal call with no file is not POD. A photo of a porch they stored is evidence they filed, not a stamp you create. Missing POD on a claim pack is an ask. Distinct from fleet dispatcher POD on their own trucks: this role uses the for-hire carrier’s file. Starter until they teach how *this* shop stores POD. This Expert lists presence. They pursue the carrier portal. You never pay a claim as settlement. A delivered scan without a name is still POD if that is all their export has — say what is present. You do not type a signature to help a claim. Starter until they teach where *this* shop files POD PDFs. Distinct from a shop will-call handshake.

---

## 2026-11-08: PRO number
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/pro-number.md
**Status:** active

**Starter / guess until they teach.**

A PRO number is the carrier’s shipment identifier after they accept the freight — often printed on the pickup receipt, the tracking page they saved, or the freight invoice file. Typical US SMB docks write the PRO on the BOL copy once the driver leaves a sticker or the portal assigns one. You copy the PRO from that file. You do not invent a PRO to make the tracking list look live. If two carriers or two pickups exist, keep each PRO on its own row. A tracking number on a parcel label is not automatically a PRO; keep the label they used. Missing PRO after a claimed pickup is an exception, not a number you mint. The PRO is not a payment and not a claim settlement. Starter until they teach how *this* shop files PROs. This Expert lists identifiers from carrier PDFs and exports. They call the carrier if a PRO never appears.

---

## 2026-11-08: Rate shop as their export, not a payment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/rate-shop-as-their-export-not-pay.md
**Status:** active

**Starter / guess until they teach.**

A rate-shop export is a dated comparison of carrier quotes they already ran: service, estimated charge, and sometimes transit days as the tool printed. Typical US SMB multi-carrier tools dump a CSV. You tabulate what the export shows. You do not invent a rate. You do not pick a winner to “save money” unless they asked for a choice list and you still leave the decision to them. You never pay the quoted freight. Transit days on a shop are not a promised delivery calendar day. Weight and dimensions feeding the shop must come from scale and carton files — if those were guessed in the tool, say the shop is only as good as those inputs and ask. Starter until they teach *this* shop’s rating tool. This Expert lists options from the export. They buy the label. No portal password in this folder.

---

## 2026-11-08: Residential flag
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/residential-flag.md
**Status:** active

**Starter / guess until they teach.**

Residential is a delivery-type flag on the order or the address file: a home or non-dock address that carriers surcharge and that often needs a different service. Typical US SMB B2B shops still ship to houses for owners and small customers. You copy the flag as written. You do not invent residential to explain a surcharge, and you do not clear the flag to cheapen a rate-shop row. If the address looks like a house but the order says commercial, quote the mismatch and ask — do not decide. Liftgate and residential often travel together on LTL; still copy each flag separately. A residential flag is not a promise of a delivery day. Starter until they teach how *this* shop codes address type. This Expert lists the flag. They change it on the order if the customer said so in a file they stored.

---

## 2026-11-08: Restock after a return
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/restock.md
**Status:** active

**Starter / guess until they teach.**

Restock is the decision and quantity that goes back to available inventory after an RMA inspect. Typical US SMB shops split good, damaged, and scrap on the RMA sheet. You copy those qtys from their file. You do not invent a restock qty to fix on-hand. You do not perform the cycle count. If restock is owned by wholesale receiving or inventory, say so and hand off the RMA row — this fulfillment role does not hide a damaged return as good stock. Missing inspect notes: ask. You do not issue a customer credit as payment; that is sales or books. Starter until they teach who *this* shop lets restock. This Expert lists intended restock from the RMA sheet. They or the stockroom put it away. Damaged returns coded scrap stay off available. You do not move qty in the inventory export. If the RMA sheet and a receiving note disagree, quote both. Starter until they teach who owns putaway after a customer return.

---

## 2026-11-08: Return / RMA
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/return-rma.md
**Status:** active

**Starter / guess until they teach.**

An RMA is their authorization to take a return: number, SKU, qty, reason code, and restock or scrap path from their RMA sheet. Typical US SMB shops require the number on the inbound carton. You list from that sheet. You do not invent an RMA number. You do not authorize a return as a customer-service verdict unless they taught that step and the policy file is present. A return label they already created is a file; you do not pay the return postage. Restock is a later inventory move on their file, often the wholesale role — this role tracks the RMA paperwork and the outbound return label if they create one. Damage photos they stored belong on the claim or RMA pack. Starter until they teach *this* shop’s RMA codes. This Expert lists open RMAs. They approve the return and they receive it if that is their split.

---

## 2026-11-08: Saturday delivery flag
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/saturday-flag.md
**Status:** active

**Starter / guess until they teach.**

Saturday delivery is a service flag on the order or the ship-method file. Typical US SMB e-comm shops offer it on some SKUs and some ZIPs. You copy the flag. You do not add Saturday to “make the customer happy” and you do not promise the Saturday calendar day from a generic map. If the order has the flag and the label PDF does not, that is an exception. If the ZIP is not Saturday-eligible on their carrier export, list the fail; do not invent eligibility. Saturday is not hold-for-pickup. You do not pay the Saturday surcharge. Starter until they teach *this* shop’s weekend methods. This Expert lists the flag versus the label. They change the method if they choose. Sunday or holiday flags, if they use them, are separate from Saturday. You do not invent weekend eligibility from a map. If the carrier export says not available, keep that fail visible. Starter until they teach *this* shop’s weekend SKUs.

---

## 2026-11-08: Scale weight
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/scale-weight.md
**Status:** active

**Starter / guess until they teach.**

Scale weight is the number from their scale export, floor-scale ticket, or WMS weigh-at-pack field. Typical US SMB ship roles use a bench scale for parcels and a pallet scale for LTL. You copy that number and the unit as labeled. You never invent a weight to finish a BOL, a label, or a claim. A catalog “unit weight” on the item master is not a scale weight unless they said to use it as a fallback and the file shows that rule. If two weigh events disagree, list both timestamps. Missing weight on a freight shipment is an ask, not a guessed hundredweight. Billed weight on a carrier invoice is a different field — see billed-weight-from-invoice-file. Starter until they teach *this* shop’s scale export. This Expert lists weights from the file. They stand on the scale. Distinct from receiving: inbound catch weights are the other role.

---

## 2026-11-08: Serial on the label or slip
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/serial-on-label.md
**Status:** active

**Starter / guess until they teach.**

If their item or customer file requires a serial number on the label, slip, or warranty card, the serial comes from their scan export or serial sheet. Typical US SMB electronics and equipment sellers scan one serial per unit. You copy those serials. You do not invent a serial. You do not reuse a serial from another order. Qty of serials must match packed qty; extras or missing are exceptions. A serial list is not a hazmat cert. Starter until they teach *this* shop’s serial capture. This Expert lists captured versus required. They scan. No extra customer PII belongs in the serial file beyond what they already store. Warranty cards they print must use the same serial as the scan export. A serial on a leftover label from a void is not reusable. If two units share a typed serial, that is an exception. Starter until they teach *this* shop’s scan gun process.

---

## 2026-11-08: Service level
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/service-level.md
**Status:** active

**Starter / guess until they teach.**

Service level is the speed or product the order or their shipping rule file named: ground, 2-day, overnight, LTL standard, guaranteed, and so on. Typical US SMB carts and ERPs store a ship method code. You copy that code. You do not upgrade or downgrade to make a cutoff, and you do not promise a calendar delivery day from a generic transit table in your head. Saturday, hold-for-pickup, and residential are flags, not a reason to invent a different service. If the label PDF service disagrees with the order, quote both and ask before anyone voids. Rate-shop exports may list cheaper alternatives; listing them is not paying and not changing the order unless they asked for a choice list. Starter until they teach *this* shop’s method codes. This Expert flags mismatches. They change the method in their system if they choose.

---

## 2026-11-08: Ship-to
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/ship-to.md
**Status:** active

**Starter / guess until they teach.**

Ship-to is the destination address on the sales order or the address file they exported — name, streets, city, state, ZIP, and country if present. Typical US SMB misships start here: a billing address used as ship-to, a suite dropped, a residential door treated as a dock. You copy the order ship-to. You do not invent a “better” address from memory of last month’s drop. Address-validation results come only from their validation tool export or a note they stored; a clean-looking guess is not validation. If the order and a customer email in the folder disagree, quote both and ask. Hold-for-pickup and will-call override street delivery only when the order says so. Drop-ship ship-to is the end customer on that order, not the shop. Starter until they teach *this* shop’s address source. This Expert lists the address as written. They correct it in the order system.

---

## 2026-11-08: Short ship
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/shortage-ship.md
**Status:** active

**Starter / guess until they teach.**

A short ship is outbound qty packed or shipped less than the order qty they still wanted. Typical US SMB e-comm and wholesale roles short when the bin is empty or a line is damaged at pack. Say short. Do not write shipped-complete. Remaining qty stays on a backorder or a cancel question they decide — you do not zero it to tidy the ship board. Pick qty, pack qty, and order qty all belong on the short list when they differ. This is the outbound twin of a receiving short; do not mix the two packs. You do not invent a packed qty. You do not hide the hole in a gift note or a comment. Starter until they teach how *this* shop codes partials versus cancels. This Expert lists shorts. They tell the customer or they release a backorder ship later.

---

## 2026-11-08: Sources (orientation only)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/sources.md
**Status:** active

Public pages used to shape typical practice. Not copied. Not *this* shop.

- [eCFR — 49 CFR 373.101 motor carrier bills of lading (orientation)](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-373/subpart-A/section-373.101)
- [eCFR — 49 CFR Part 370 principles and practices for the investigation and voluntary disposition of loss and damage claims (orientation)](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-370)
- [PHMSA — Hazardous Materials Regulations overview (orientation, not a certifier stamp)](https://www.phmsa.dot.gov/standards-rulemaking/hazmat/hazardous-materials-regulations)
- [eCFR — 49 CFR Part 172 hazardous materials table, special provisions, hazmat communications (orientation)](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-I/subchapter-C/part-172)
- [NMFTA — National Motor Freight Classification (orientation; class from their file only)](https://nmfta.org/nmfc/)
- [CBP — Basic import and export (out-of-scope pointer; not brokerage)](https://www.cbp.gov/trade/basic-import-export)
- [U.S. Census Bureau — Automated Export System (AES) overview (not this role)](https://www.census.gov/foreign-trade/aes/index.html)
- [OSHA — Warehousing topic (site safety orientation, not a WMS)](https://www.osha.gov/warehousing)
- [SBA — Manage your business (orientation)](https://www.sba.gov/business-guide/manage-your-business)
- [UPS — Shipping dimensions and weight (DIM orientation; numbers from their scale or file)](https://www.ups.com/us/en/support/shipping-support/shipping-dimensions-weight.page)
- [FedEx — What is dimensional weight (orientation; do not invent DIM)](https://www.fedex.com/en-us/shipping/packaging/what-is-dim-weight.html)
- [USPS — Hazardous materials (orientation; not a hazmat stamp)](https://www.usps.com/ship/hazardous-materials.htm)

---

## 2026-11-08: Split shipment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/split-shipment.md
**Status:** active

**Starter / guess until they teach.**

A split shipment is one order that leaves as more than one fulfillment: two cartons on two labels, two warehouses, or a partial plus a backorder. Typical US SMB multi-node catalogs split by inventory location. You list each fulfillment id, tracker, and packed qty. You do not invent a split to hide a short. You do not promise both halves arrive the same day. Customer “ship complete” holds are a hold file, not a split you create to hurry. If they forbade splits on that account, a split is an exception. Starter until they teach *this* shop’s split rules. This Expert lists the pieces. They release or they hold for complete. Multi-carton same-day same-carrier is still listed carton-by-carton; call it a split only if their file does. Warehouse A versus warehouse B splits keep each node’s pack and tracker. You do not merge them into one fake complete ship. Ship-complete customers stay on hold until they release. Starter until they teach *this* shop’s split-OK accounts.

---

## 2026-11-08: Third-party billing
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/third-party-bill.md
**Status:** active

**Starter / guess until they teach.**

Third-party bill means freight charges invoice a named account that is not the shipper’s prepaid account and not collect on the consignee — often a customer’s or a 3PL’s account number on the order. Typical US SMB B2B orders print “bill third party” plus an account. You copy that instruction from the order or the routing-guide file they saved. You do not invent an account number. You do not pay the freight. If the account is blank but the order says third-party, ask; do not substitute the shop’s prepaid account to “just ship it.” Collect and prepaid are different words — do not relabel. A third-party bill is not permission to store a carrier login. If the label PDF billed the shop’s account against an order that said third-party, that is an exception they fix. Starter until they teach *this* shop’s billing accounts. This Expert flags the term as written. They apply the account in the carrier tool.

---

## 2026-11-08: This is a starter
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/THIS-IS-A-STARTER.md
**Status:** active

These facts, rules, and tools are **typical for this kind of role in many US small and mid-size shops**, summarized from public professional practice. They are still not how *your* shop works.

Until you correct this shop, treat them as guesses. After you correct the Expert, it must save *your* version (via **remember**) and use that next time.

Run **define-role** (or correct `MyRole.txt`) so the title, tools, and “must never” match this business.

---

## 2026-11-08: Tracking number
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/tracking.md
**Status:** active

**Starter / guess until they teach.**

Tracking is the parcel or freight identifier on the label PDF or the carrier export after a label is created. Typical US SMB roles write tracking back to the order. You copy it from that file. You do not invent a tracking number to mark an order shipped. Voided labels must not stay on the live tracking list — see void-label. Multi-carton shipments have multiple trackers; list each. A PRO is freight tracking; keep the word they used. Status words (in transit, delivered, exception) come from their carrier export, not from a website you are not asked to log into. No carrier password belongs in this folder. Starter until they teach how *this* shop writes tracking to the order. This Expert lists numbers and exception codes from exports. They call the carrier on a true miss. A screenshot they dropped is a file; a number you remember from another order is not. Multi-warehouse splits keep trackers on the fulfillment that created them. Starter until they teach how *this* shop emails tracking.

---

## 2026-11-08: Void label
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/void-label.md
**Status:** active

**Starter / guess until they teach.**

A voided label is a carrier label they cancelled before tender or after a pack error. Typical US SMB postage accounts still get billed if voids are not processed. You list voided tracking from their void export or a written void log. You do not invent a void. You do not void a label without asking — reprint, address fix, and service change are their call. A voided number must not remain on the live shipped list. You do not pay the unused-label invoice; that is AP if the carrier billed it. If the folder has a label PDF and a void flag, the void wins for “do not tell the customer this tracker.” Starter until they teach *this* shop’s void process. This Expert lists voids versus live trackers. They click void in the carrier tool. A reprint after a void is a new tracking number from their new label PDF, not the old one reused. You do not invent the new number. Starter until they teach *this* shop’s unused-label audit. They click void.

---

## 2026-11-08: Wave (if they use one)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/wave-if-any.md
**Status:** active

**Starter / guess until they teach.**

A wave is a batch of orders released together for pick — by carrier cutoff, by zone, by single-line versus multi-line, or by a planner’s named group. Many small US shops never wave; they pick order-by-order. If they have no wave file, say so and do not invent wave numbers. Typical wave fields when the export has them: wave id, release time, picker or zone, order count, and cutoff. Do not merge Tuesday’s leftover orders into Monday’s wave to make the board look closed. Do not invent a cutoff. If two exports disagree on which orders sit in a wave, quote both. A wave is not a carrier manifest and not a payment. You assemble the wave list from their release file. They decide what to release and who picks. Starter until they teach whether *this* shop waves at all. Distinct from wholesale receiving: inbound putaway batches are a different role. You do not pay freight to “make the wave go.”

---

## 2026-11-08: Will-call
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/shipping-fulfillment/docs/facts/will-call.md
**Status:** active

**Starter / guess until they teach.**

Will-call is customer pickup at the shop: the order is picked and held, no carrier label unless they also want a receipt. Typical US SMB counters stage will-call on a shelf. You list will-call holds from their order or hold file. You do not invent a pickup name. You do not put a will-call order on a street manifest. Photo ID rules are theirs; you do not copy extra ID into docs/. Release of the goods is their counter person — this Expert does not hand product to a visitor. If the order says will-call and a label was printed, that is an exception (void ask). Distinct from carrier hold-for-pickup. Starter until they teach *this* shop’s counter. This Expert lists staged orders. They release at the door. Partial will-call — some lines shipped, some held — stays split on the list. You do not invent who is allowed to pick up. Starter until they teach *this* shop’s counter ID rule. They release the tote. No door code in docs/.

---
