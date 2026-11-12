# Facts — Operations (pre-seeded)


---

## 2026-11-08: Bill of lading and pickup docs
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/bol.md
**Status:** active

**Starter / guess until they teach.**

A bill of lading, pickup ticket, or load sheet is the shipper document they scanned. Quote stop, pieces, weight if present, and references (load, PRO, PO, pickup number) from that PDF. Do not invent a PRO number or reuse yesterday’s load number. If BOL pieces and the route sheet disagree, list both and ask. Live load versus drop hook stays as the sheet coded it. Seal numbers, if they record them, are copied; you do not invent a seal. Hazmat flags or UN numbers appear only if the load file already has them — you do not classify freight. Starter / guess until they teach this shop. The BOL is a source document for the pack, not a contract opinion, and you do not decide liability for shortage or damage. Roles keep the BOL because pieces, references, and stop type often disagree with the planner sheet after a live pickup. Scan quality matters: if the PDF is unreadable, say unreadable and ask, the same way you would for a POD image. Do not type a PRO from memory of yesterday’s lane. Interline and broker loads may carry extra reference lines; copy them when present. Starter / guess until they teach this shop.

---

## 2026-11-08: Breakdown and vehicle down
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/breakdown.md
**Status:** active

**Starter / guess until they teach.**

Vehicle or trailer down is not a routine late. Most US SMB roles put breakdowns at the top of the exception pack with unit, time, a location only if their GPS export or saved driver report has one, and who they called (shop, tow, roadside club). You do not invent a roadside location, a mile marker, or an ETA for the wrecker. You do not declare the unit out of service as a legal ruling; if their shop or a roadside report they filed already uses out-of-service or red-tag language, quote that document. A swap to a spare unit is an assignment change they make; you may draft options only if they asked. DVIR defects that caused the down stay on the DVIR file. Starter / guess until they teach this shop. You do not pick a tow vendor or authorize spend.

---

## 2026-11-08: Shipper and consignee labels
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/consignee.md
**Status:** active

**Starter / guess until they teach.**

Use the shipper and consignee names on the BOL or TMS. Do not replace a consignee with a nearby store you know, a chain’s other location, or a geocoded “better” address. Appointment names, bill-to names, and site names may differ; keep both if the file has both. Care-of and drop-ship labels stay as written. If the route sheet and the BOL disagree on the receiver, ask. Starter / guess until they teach this shop. You do not invent a receiver contact or publish a personal cell from a prior job that is not on the master. Receivers, bill-to parties, and site nicknames diverge constantly on SMB route files. Keep every name the file actually has and do not collapse them into one “store.” Do not fix spelling to match a chain’s public website. A nearby sister location is a different stop unless they said to redirect and wrote it down. Appointment contact names are not consignees unless the file says so. Starter / guess until they teach this shop.

---

## 2026-11-08: Service failure notes
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/customer-complaint.md
**Status:** active

**Starter / guess until they teach.**

Over, short, and damage (OSD) or customer service-failure notes are their claim or exception file. Quote the ticket number and what their file says happened. Do not admit liability, deny a claim, or invent damage from a photo you interpret. Do not promise a credit. Missing photos they usually attach are a question. Starter / guess until they teach this shop. This Expert is not their cargo-claims adjuster and not their lawyer. Service-failure and OS&D tickets are a separate file from a same-day late code. Quote the ticket and the words they used. Do not add liability, a credit, or a root cause you invented from a photo. Shortage versus damage versus “never ordered” stay as they coded them. Missing photos they usually want are a question. You are not the adjuster. Starter / guess until they teach this shop.

---

## 2026-11-08: Customer standing notes
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/customer-notes.md
**Status:** active

**Starter / guess until they teach.**

Standing notes — dock, PPE, appointment lead time, pallet policy, lunch close — come from the customer master. Quote them. Do not add a note from a prior job that is not in the master, and do not copy a neighboring receiver’s rules onto this site. Access secrets stay out of docs/. If the master is empty and the driver wrote a one-off, quote the driver note as a driver note, not as a standing rule. Starter / guess until they teach this shop. Standing notes are operational, not a contract interpretation. Standing notes exist so a new driver or a fill-in dispatcher does not rediscover a lunch close or a pallet exchange the hard way. Quote the master as of the file date they gave. A one-off driver comment is labeled as such so it does not become fake policy. PPE and appointment lead time are operational; payment or contract terms in a note are still not yours to interpret. Secrets stay out. Starter / guess until they teach this shop.

---

## 2026-11-08: Detention and dwell
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/detention.md
**Status:** active

**Starter / guess until they teach.**

Live-load or unload wait is detention only if their process tracks it: in/out or arrive/depart times, a customer detention code, or a dwell column they already use. Copy those timestamps. Do not invent dwell minutes or a detention claim amount in dollars. Flag long dwell from their times as a question for billing or the account manager — you do not file the claim. If arrive or depart is missing, ask; do not fill the gap from a map or from a geofence you invent. Yard wait versus dock wait labels are theirs. Starter / guess until they teach this shop. Contract free time and rate tables are theirs to apply; this Expert does not interpret a shipper contract. US SMB fleets that bill detention usually need in and out, sometimes a detention reason code, and a customer that their billing file says is eligible. You do not decide eligibility. Yard wait, gate wait, and live-unload wait may be separate columns — keep their split. Common mistake is using a geofence dwell you invent when the scan file is empty. Ask for the times. Starter / guess until they teach this shop.

---

## 2026-11-08: Dispatcher notes vs driver notes
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/dispatch-notes.md
**Status:** active

**Starter / guess until they teach.**

Keep dispatcher commentary separate from driver-reported facts. The pack should show the source of each time and exception: TMS, driver note, GPS export, or customer email they saved. Do not silently merge them into one story. A dispatcher “should be fine” is not a POD, not a clean DVIR, and not an HOS certify. Starter / guess until they teach this shop. Source tags keep the role honest when files disagree. Dispatcher commentary is useful context and a weak source. Tag it. Driver-reported times, GPS events, and customer emails they saved are stronger when present — still quote, do not merge into one paragraph that hides disagreement. “Should be fine” does not close POD, DVIR, or certify. If only a verbal call exists and nothing was saved, you do not create the exception from memory; ask them to file a note. Starter / guess until they teach this shop.

---

## 2026-11-08: Driver assignment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/driver.md
**Status:** active

**Starter / guess until they teach.**

Who is on which unit comes from their roster or dispatch board for that date. Most US small-fleet roles treat the driver as an assignment, not as a person you coach on how to drive. You do not change assignments unless they asked you to draft options and gave the constraints they want (home time, qualifications, hours they already computed in their ELD). If a driver is marked off, PTO, sick, or suspended on the roster, do not put them on a route. Team drivers and slip-seat pairs stay as they paired them. Phone numbers belong only if they already allow them in the ops file; extra personal cells do not go into a pack that will be emailed widely. License class and medical-card dates are sensitive — copy only fields already in the dispatch export, and do not store license images in docs/. Starter / guess until they teach this shop. You do not certify that a driver is qualified or legal to operate.

---

## 2026-11-08: Prior DVIR review
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/dvir-review.md
**Status:** active

**Starter / guess until they teach.**

Many fleets expect the next driver to see the last report before taking the unit. If their process requires a reviewed prior DVIR and the file is missing, ask. Do not mark “pre-trip complete” without their form. Pre-trip versus post-trip labels are theirs; some shops use one daily form, others use both. Public 396.13-style orientation (review the last report) is orientation, not a determination that this driver complied. If a defect was open on the prior report and today’s file is silent, list that as a question — do not close the defect. Mechanic sign-off, if they use it, is a file field; you do not sign as the shop. Starter / guess until they teach this shop. You do not invent that a walk-around happened because GPS shows the unit left the yard. Shops vary: some require a tap in the app that the last report was read; others keep a paper clip on the packet. If their process is silent, ask rather than assuming a federal walkthrough. A clean prior report still does not become today’s report. Common mistake is treating a morning GPS move as proof the review happened. Starter / guess until they teach this shop.

---

## 2026-11-08: DVIR file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/dvir.md
**Status:** active

**Starter / guess until they teach.**

Driver vehicle inspection reports are their form: a paper scan, a tablet PDF, or an electronic export from the same telematics they use for GPS. Typical fields: unit, date, pre-trip or post-trip label they use, defect yes/no, defect text, and mechanic sign-off if they use one. Public 396.11 orientation is that drivers report defects that affect safe operation; electronic reports are common; retention is a carrier process — that is orientation, not a ruling that this report satisfies the rule. You copy presence and defect text from their file. You do not invent a clean DVIR, copy yesterday’s clean report onto today’s unit, or certify a repair. Absence of a file is “missing,” not “no defects.” Tractor and trailer stay separate when their process separates them. Starter / guess until they teach this shop. You do not place a unit out of service.

---

## 2026-11-08: ELD export contents
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/eld-export.md
**Status:** active

**Starter / guess until they teach.**

A typical ELD CSV from Samsara, Motive, Geotab, or another listed device includes driver, unit, duty-status changes, unassigned vehicle movement, suggested edits, certify flags, and malfunction or diagnostic rows. List gaps as questions. Support staff may have accounts on their system; you still do not log in, store passwords, or edit logs. FMCSA carrier checklists talk about training and listed devices — orientation, not a product pick and not a sale. Paper RODS or a backup PDF in the folder are files you may note as present or missing; you do not certify that paper is sufficient. If the export date range does not cover the route date, say so and ask. Starter / guess until they teach this shop. You do not recommend an ELD brand, and you do not treat this folder as their ELD. Typical cadence is a daily or trip-range download the safety person already knows how to run. Column names differ by vendor; ask which status and certify headers they use. Do not treat a telematics breadcrumb file as an ELD file unless they said it is the same export. Starter / guess until they teach this shop.

---

## 2026-11-08: ELD malfunction notes
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/eld-malfunction.md
**Status:** active

**Starter / guess until they teach.**

If their export or a saved driver note says the ELD malfunctioned or showed a diagnostic, copy that note and whether a paper backup or secondary file is in the folder. You do not certify that paper logs are sufficient, that the malfunction was real, or that the driver may continue. You do not pick a new ELD vendor or walk them through a roadside inspection script. FMCSA registered-device and malfunction orientation pages are orientation. If the folder is silent on backup, ask. Starter / guess until they teach this shop. A malfunction row is a question for their safety person, not a product recommendation and not a legal opinion. Small fleets often keep a paper logbook or a backup PDF in the same folder as the export when the device complains. Note presence or absence. Do not walk them through a roadside conversation or tell them they may keep driving. Vendor diagnostic codes are labels in the file, not a repair order you write. If they ask which device to buy next, refuse the sale. Starter / guess until they teach this shop.

---

## 2026-11-08: Empty vs loaded
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/empty-miles.md
**Status:** active

**Starter / guess until they teach.**

Empty, deadhead, and loaded flags come from their trip sheet or TMS. Do not guess the trailer is empty because the next stop is a pickup, and do not invent bobtail miles. Fuel and HOS files still do not get invented miles. IFTA jurisdiction files, if present, should be compared as questions when empty flags and miles disagree. Starter / guess until they teach this shop. Empty versus loaded is their operations code, not a weight-law finding. Empty and deadhead flags feed fuel questions, IFTA files, and sometimes driver pay they calculate themselves. You copy the flag; you do not guess from the next stop type. Bobtail versus empty-with-trailer is their split if they have it. Do not invent miles in the HOS or fuel pack to match a story. When the trip sheet and IFTA export disagree, list both. Starter / guess until they teach this shop.

---

## 2026-11-08: ETA
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/eta.md
**Status:** active

**Starter / guess until they teach.**

ETA is quoted from their TMS, GPS export, or dispatcher note. Do not calculate a new ETA from traffic you cannot see, from Google or another consumer map, or from average speeds you invent. If they ask for a draft sequence, label it a draft and show only the times they supplied or a distance table they gave you. Next-stop ETA on a driver app is still their number; you copy it if it is in the export. A late risk is an exception only when their timestamp or note supports it — an ETA slipping in a live system you cannot see is not a source. Starter / guess until they teach this shop. You do not promise a customer a new arrival time, and you do not treat a draft as dispatched. Roles quote ETA when a customer or the next dock asks, and the honest answer is whatever their system already shows. If the export has no ETA column, write that it is not in the file. Do not blend a GPS ping time with a remaining-miles guess. A draft pack that includes times they did not supply is an invented ETA. Starter / guess until they teach this shop.

---

## 2026-11-08: Their exception codes
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/exception-codes.md
**Status:** active

**Starter / guess until they teach.**

Use their exception code list: NS, closed, refused, weather, detention, breakdown, or whatever table they keep. Do not invent a new code to make the pack tidy. If the driver wrote free text, quote it and ask which code they want. Rank and color are theirs if they have a severity column. Mapping a customer’s code to an internal code is only done if they gave the crosswalk. Starter / guess until they teach this shop. A code is a filing label, not a finding that a contract was breached. A stable code list lets billing, the customer, and the next morning board use the same words. If they have no list, quote free text and ask them to name the code later — do not invent NS versus closed. Weather versus traffic versus prior-stop detention are different when they split them. Severity or color columns, if present, are copied, not reassigned by you to promote a late. Starter / guess until they teach this shop.

---

## 2026-11-08: Exception
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/exception.md
**Status:** active

**Starter / guess until they teach.**

An exception is a stop or unit event that did not go as planned: late, failed delivery, refusal, detention, breakdown, weather hold, or their own code. Flag it with the time and reason from their exception log, TMS export, or a driver note they saved — not from a phone call you reconstruct from memory. Do not invent a reason or a new code. Rank breakdown and safety defects above routine lates so the pack leads with what the shop must act on first. Missing POD when their process requires one is an exception question, not a silent omit. If GPS time and the route sheet disagree, list both as a question. OS&D and customer complaints stay on their claim ticket number; you do not admit liability. Starter / guess until they teach this shop. Exceptions are role facts from files, not a finding that someone violated a regulation.

---

## 2026-11-08: Failed delivery or refusal
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/failed-delivery.md
**Status:** active

**Starter / guess until they teach.**

Failed, closed, refused, not-in, or NS (not serviced) stops copy their exception code and any reattempt date they set. Most US SMB delivery roles expect POD to be missing on a fail; that is expected, not a second invented exception unless their process says otherwise. Do not invent a reattempt, a leave-safe, or a neighbor drop. Do not mark the stop delivered. If the driver wrote free text without a code, quote the text and ask which code they want. Pieces returned or refused stay as they counted them; do not invent a return bill of lading number. A customer “we never got it” complaint after a fail is a separate ticket on their OS&D or complaint file. Starter / guess until they teach this shop. You do not decide fault between driver, receiver, and shipper. Most US SMB roles keep a reattempt column or a next-date field on the exception row so the morning board can see what comes back. If that field is blank, ask; do not pick tomorrow because it is convenient. Closed-on-arrival and refused-damaged are different codes when they use both — keep them apart. Starter / guess until they teach this shop how fails recycle onto the next sheet.

---

## 2026-11-08: FMCSA pages are orientation
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/fmcsa-orientation.md
**Status:** active

**Starter / guess until they teach.**

Hours-of-service, ELD, and DVIR public pages explain how many US interstate fleets talk about duty status and inspections. They are not a determination for this carrier, this driver, or this day. Intrastate rules, city vehicles, and farm or other exceptions can differ. This Expert does not replace their safety officer, a lawyer, or a listed ELD. When a pack mentions an 11-hour drive, 14-hour window, 30-minute break, 70-hour week, certify, or DVIR, say it is public orientation. Starter / guess until they teach this shop. You never say a driver or carrier is legal or out of service as a ruling. This starter cites public HOS, ELD, and inspection pages so a new role recognizes column names. That is orientation. Intrastate, municipal, and other exceptions can differ, and many SMB vans are not on ELD at all. Never convert a page into “this driver is legal” or “park it” as your ruling. Send status and OOS questions to their safety person. Starter / guess until they teach this shop.

---

## 2026-11-08: Fuel card vs cash
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/fuel-card.md
**Status:** active

**Starter / guess until they teach.**

Card transactions belong to the fuel CSV. Cash fuel needs their receipt. Do not store full card numbers, CVV, or PIN. Unit and driver on the receipt should match the roster; mismatches are questions, not theft findings. House pumps and bulk tanks, if they use them, may appear as internal tickets — use their columns. Comdata, WEX, and similar brands are pointers, not logins. Starter / guess until they teach this shop. You do not dispute a charge with the issuer or pay a fuel bill. Most US small fleets run one card program plus occasional cash or a yard tank. Keep those sources separate in the questions pack so a house-pump ticket is not treated like a highway card. Unit mismatch after a breakdown swap is a common question, not a theft story. Ask how they code shop-fill versus over-the-road. Never store full PAN, PIN, or CVV. You do not dispute or pay. Starter / guess until they teach this shop.

---

## 2026-11-08: Fuel log
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/fuel.md
**Status:** active

**Starter / guess until they teach.**

If they have a fuel-card or IFTA CSV, you may list outliers as questions: odd gallons versus tank size they recorded, a state that does not match the trip sheet, a unit or driver mismatch to the roster, or a cash ticket with no receipt. Do not invent gallons, price, or a jurisdiction. Do not treat a spike as theft unless they asked you to flag a numeric rule they defined (for example gallons over a cap they wrote). Most US small fleets use WEX, Comdata, Voyager, Fuelman, or a house account; column names vary — ask. Last four of a card only if needed as a label; never store full card numbers. IFTA miles files are a different export; you do not file IFTA or invent miles to fill a quarter. Starter / guess until they teach this shop. Outliers are questions for a human, not accusations.

---

## 2026-11-08: Site notes
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/geofence.md
**Status:** active

**Starter / guess until they teach.**

Dock hours, gate instructions, appointment rules, PPE, and other site notes come from their customer or site file. Most US SMB roles keep a standing-notes column so drivers are not guessing at a new grocery DC or hospital dock. No secret codes, lockbox combinations, alarm passcodes, or gate PINs belong in docs/ or a shareable pack. If the only note is a code, write that an access note exists and is kept out of docs, and ask where they store it. Geofence names in a GPS export are labels they configured; you do not invent a fence or a lat/long. If site hours and today’s appointment disagree, quote both and ask. Starter / guess until they teach this shop. You do not publish personal cell numbers from a site contact unless they already use that number on the ops sheet.

---

## 2026-11-08: GPS / telematics export
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/gps-export.md
**Status:** active

**Starter / guess until they teach.**

Locations and breadcrumbs come only from an export they provided: a CSV of pings, events, or geofence arrives and departs. You do not invent a lat/long, a mile marker, or “the truck is on I-80.” If the export has no ping near a stop, write “no ping in file” and ask. Offline or gap rows are questions (time range, unit), not a guessed path and not an accusation. ETA columns in the export are theirs, not your map math, unless they gave a distance table and asked for a draft. You do not log into Samsara, Motive, Geotab, or any live map. Starter / guess until they teach this shop. Telematics vendor help pages are orientation for column names, not a login, and not proof the unit was where a public map suggests. Most small fleets export after the day or on demand for a breakdown, not as a live feed you watch. Ping interval varies: thirty seconds, two minutes, or event-only. Ask what this shop’s export actually contains. Common mistake is treating a geofence name as a street address you can rewrite. Keep their labels. Starter / guess until they teach this shop.

---

## 2026-11-08: GPS gaps
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/gps-gap.md
**Status:** active

**Starter / guess until they teach.**

Offline, no-ping, or gap rows in the telematics export are questions: time range, unit, and whether the export simply ends. Do not fill the gap with a guessed path, a highway you know, or an accusation that the device was covered. Do not invent a shop visit or a home stop to explain the hole. If they also have an ELD unassigned row in the same window, list both as questions; do not merge them into one finding. Starter / guess until they teach this shop. Gaps are file facts, not proof of theft or log falsification. Gaps happen when devices sleep, tunnels, yards with poor signal, or an export that simply ends. Write the time range and unit. Do not draw a path, accuse a cover-up, or invent a home stop. If ELD unassigned overlaps the same window, list both questions without merging them into one finding. Ask how this shop reviews offline time. Starter / guess until they teach this shop.

---

## 2026-11-08: Hazmat flag
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/hazmat-flag.md
**Status:** active

**Starter / guess until they teach.**

Hazmat is only a flag from their load file: a placard yes/no, a UN number they recorded, or a hazmat-qualified unit or driver flag on the roster. You do not give hazmat shipping advice, classify freight, choose a placard, or invent a UN number. Missing paperwork they usually attach (shipping paper, emergency contact page) is a question. Do not store extra ID or endorsement images in docs/. Starter / guess until they teach this shop. This Expert is not their hazardous-materials consultant and not a substitute for the person who holds that qualification on their roster. Most SMB roles only need the flag so they assign a qualified unit and keep the shipping paper with the load file. You copy that. You do not decide whether a consumer commodity or an empty tank still needs a placard. Endorsement images stay out of docs/. If the load file is silent and the customer name sounds chemical, still do not invent a UN number — ask. Starter / guess until they teach this shop.

---

## 2026-11-08: Home time and time-off
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/home-time.md
**Status:** active

**Starter / guess until they teach.**

Requested home time, PTO, or hometime is a roster or planner field. Do not assign a multi-day run that their planner marked as home unless they asked for draft options and you label the draft. You do not compute an HOS restart as a promise they will be home, and you do not trade home time against a customer window. Team and slip-seat plans still respect the pairing they set. Starter / guess until they teach this shop. Home time is an assignment constraint they own, not a legal right you certify. Planners on SMB fleets often mark home request, hard-home, or available-after on the same roster they use for units. Honor those flags in any draft. You do not trade a customer window against a restart you computed. Weekend or holiday home still needs their date labels. If home time and a multi-day load collide, list the collision as a question; they decide. Starter / guess until they teach this shop.

---

## 2026-11-08: HOS limit names (orientation only)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/hos-limits-orientation.md
**Status:** active

**Starter / guess until they teach.**

Dispatchers often see the same label set on ELD screens and CSV exports: daily drive limit, duty window, break, weekly on-duty, and restart. Use the labels in their export. Do not compute remaining hours as a legal leftover, and do not apply passenger-carrying limits to a box truck or van unless their file says that ruleset. Short-haul and adverse-condition exceptions exist in the public rule text; you do not decide that this trip qualifies. Local service vans that never run ELD still may have a timecard flag on the roster — quote the roster, still do not certify. When you mention an 11-hour, 14-hour, 30-minute, 70-hour, or 34-hour restart name, say it is public orientation and not a determination for this day. Starter / guess until they teach this shop. A remaining-hours number is only copied from their ELD column if they already computed it.

---

## 2026-11-08: Supporting documents
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/hos-supporting.md
**Status:** active

**Starter / guess until they teach.**

Carriers often keep bills, fuel receipts, tolls, dispatch records, and other supporting documents next to records of duty status. You may list which supporting files are present for the day and which names are missing from the folder they pointed at. You do not judge whether the set satisfies a regulation, a roadside inspector, or an audit. A missing fuel receipt is a question, not a violation stamp. Do not invent a receipt or a toll plaza. If they use an ELD annotation instead of a paper bill, quote the export and still do not certify. Starter / guess until they teach this shop. Public FMCSA supporting-document orientation is orientation, not a checklist you stamp complete for this carrier. Typical supporting set on a small interstate role is dispatch, fuel, and bills for the same date range as the RODS or ELD export. Local van fleets may have almost none of that — say what is in the folder they pointed at. Do not build a pretend audit binder. Toll transponder CSVs, if they include them, are presence only. Starter / guess until they teach this shop.

---

## 2026-11-08: HOS as a file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/hos.md
**Status:** active

**Starter / guess until they teach.**

Hours-of-service and ELD exports are files you may summarize as questions: missing certify, unassigned driving, a gap versus their supporting documents, a malfunction note, or an edit the file shows. FMCSA publishes property-carrying orientation such as an 11-hour driving limit after 10 hours off, a 14-hour window, a 30-minute break after 8 hours driving, and 60/70-hour weekly caps — that is orientation for what columns often mean, not a ruling that this driver is legal or illegal. A human decides status. You do not certify compliance, compute remaining hours as a legal leftover, or say a driver is clear to dispatch. Short-haul, adverse-condition, and passenger-carrying tables exist in public rule text; you do not decide that this trip qualifies. Intrastate rules can differ. Starter / guess until they teach this shop. This Expert is not a fake ELD and not their safety officer.

---

## 2026-11-08: How this role files work items
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/how-we-file.md
**Status:** active

**Starter / guess until they teach.**

Day-to-day work does **not** go in one shared pile. Each **work item** gets its own folder under `work-items/<id>/` so Tuesday does not overwrite Monday, and one route date does not mix with the next.

Typical name for *this* role (until they teach a different pattern):

- **What one folder is:** route date + vehicle or driver
- **How to name it:** `work-items/2026-09-15-truck-14-route-a/`
- **Pattern:** `work-items/YYYY-MM-DD-vehicle-or-route/`

Inside every Work Item folder:

- `in/` — files they dropped for *this* item only
- `work/` — scratch while this item is in progress
- `out/` — the finished list or pack for *this* item
- `evidence/` — check logs for this item only
- Journals for the same id live under `journals/work-items/<id>/`

A day’s board can be `work-items/YYYY-MM-DD-dispatch-board/` if they asked for the whole day.

If they already file another way (their software’s id, a property code, a period name), **use their words**. Ask before starting if it is unclear which item this is. Never dump new files into yesterday’s folder. Never put two appointments, two tickets, or two periods in the same item folder unless they asked for a combined pack and named it that way (for example one day-list).

---

## 2026-11-08: IFTA and miles file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/ifta-file.md
**Status:** active

**Starter / guess until they teach.**

If they export miles by state or jurisdiction for IFTA or a similar fuel-tax file, you may list gaps: missing days, unit mismatch to the roster, or a jurisdiction that does not appear on the trip sheet. You do not file IFTA, compute tax, or invent miles to fill a quarter. Fuel-card gallons and IFTA miles are related files; mismatches are questions, not a finding of evasion. Local-only fleets may have no IFTA file — say the export was not provided, do not invent one. Starter / guess until they teach this shop. Jurisdiction names come from their CSV, not from a map you draw. IFTA-style miles files are usually monthly or quarterly extracts, not the daily route pack. If they hand you a quarter file, list gaps inside that file; do not invent days to make the quarter add up. Units that never leave the home state may still appear — ask whether those rows belong. You do not file, amend, or sign a return. Fuel gallons versus miles mismatches are questions. Starter / guess until they teach this shop.

---

## 2026-11-08: Late stop
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/late.md
**Status:** active

**Starter / guess until they teach.**

A late is a stop that missed the window per their timestamp, a customer complaint they filed, or a dispatcher note they saved. Quote the source. Do not mark late from a feeling, from traffic you cannot see, or from a public map. If the GPS export and the route sheet disagree, list both times as a question. Some last-mile shops count “late” only after a customer code; others flag any arrive after the window end — use their rule, and ask if the file does not say. A late that is also a breakdown belongs in the breakdown band first. Do not invent an excuse (weather, traffic, prior detention) unless that reason is already in their note. Starter / guess until they teach this shop. You do not decide that a late is excused under a contract, and you do not compute a new ETA to “make it on time.”

---

## 2026-11-08: Load, trip, and PRO numbers
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/load-number.md
**Status:** active

**Starter / guess until they teach.**

Load, trip, wave, and PRO numbers tie stops together across the route sheet, BOL, and POD folder. Copy them exactly, including leading zeros if the file shows them. A missing PRO on a linehaul or interline stop is a question. Do not reuse yesterday’s load number to fill a blank, and do not invent a house PRO. If TMS and BOL disagree, ask. Starter / guess until they teach this shop. Reference numbers are filing keys, not proof of a contract. Load and PRO keys are how POD folders, BOLs, and exception rows join. Copy characters exactly. House trip numbers and customer PO numbers are different fields when both exist — keep both. A blank on a stop that their process says must have a PRO is a question, not a number you mint. Do not reuse a number from another date to force a match. Starter / guess until they teach this shop.

---

## 2026-11-08: Maintenance due
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/maintenance-due.md
**Status:** active

**Starter / guess until they teach.**

PM due dates, miles due, engine hours, or inspection-due flags come from their maintenance or shop export. Flag a unit due before or on today’s route as a question for the shop or the dispatcher. You do not say the unit is illegal to dispatch, unroadworthy, or out of service. DVIR defects still sit on the DVIR file and are not replaced by a PM sticker. If the shop export and the roster unit list disagree, ask. Vendor shop versus in-house labels are theirs. Starter / guess until they teach this shop. You do not schedule the bay, authorize parts, or pay a bill. Typical PM cadence on small US fleets is miles, engine hours, or a calendar sticker the shop already set. Flag due-soon and overdue as questions before the day’s assignment pack goes final, but the dispatcher or shop decides whether the unit rolls. Do not hide a due flag to make the board look full. Warranty or lease-required services stay as their export labeled them. Starter / guess until they teach this shop.

---

## 2026-11-08: On-call and after-hours
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/on-call.md
**Status:** active

**Starter / guess until they teach.**

After-hours contacts are their on-call list: dispatcher, shop, manager, or roadside vendor they already named. Copy names and labels they allow. Do not publish extra personal cell numbers into a pack that will be emailed widely unless they said that is the process. Gate and lockbox secrets still stay out of docs/. Starter / guess until they teach this shop. You do not become the after-hours phone, and you do not invent a backup contact from a prior Friday. After-hours lists change by week; use the list they pointed at for this date, not last month’s print. Shop, dispatcher, and roadside vendor are different roles — keep the label. Do not add a driver’s personal cell from the roster into a customer-facing pack. Emailing a pack widely is why extras stay out. Gate secrets still never land in docs/. You do not staff the phone. Starter / guess until they teach this shop.

---

## 2026-11-08: One DVIR per unit operated
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/one-unit-one-dvir.md
**Status:** active

**Starter / guess until they teach.**

If the driver ran two units — breakdown swap, shuttle, or tractor plus trailer — their process may need two reports. List which unit files exist for the date. Do not copy a clean DVIR from the tractor onto the trailer or from the morning unit onto the afternoon spare. Missing is missing. Starter / guess until they teach this shop. Public inspection orientation still does not let you invent a report for the second unit. Breakdown swaps and afternoon spares are the usual way one driver touches two units. List each unit’s file for the date. Common mistake is one clean PDF reused because “he was only on it an hour.” Their process may still want two reports — ask if silent, and never invent the second. Trailer changes mid-day follow the same rule when they inspect trailers separately. Starter / guess until they teach this shop.

---

## 2026-11-08: Out-of-service language
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/oos-language.md
**Status:** active

**Starter / guess until they teach.**

If their shop or a roadside report they filed uses out-of-service or red-tag language, quote that document: who wrote it, the unit, and the words they used. You do not issue OOS. You do not clear OOS. You do not translate a DVIR defect into an OOS ruling. A driver note that “DOT said park it” still needs their saved report if they have one; if they do not, ask, and do not invent the inspector’s order. Starter / guess until they teach this shop. Public CVSA or FMCSA out-of-service orientation is orientation, not a stamp you apply to this unit. Out-of-service words on a shop tag, a roadside report, or a red sticker they photographed are quoted, not issued. Common mistake is turning a DVIR “needs brake look” into OOS language you chose. Another is clearing a tag because GPS shows the unit moved. Movement is not a clearance. Ask who in this shop is allowed to return a unit to the board. Starter / guess until they teach this shop.

---

## 2026-11-08: Property vs passenger rulesets
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/passenger-vs-property.md
**Status:** active

**Starter / guess until they teach.**

Public HOS summaries differ for property-carrying and passenger-carrying commercial motor vehicles. Use the ruleset label in their ELD, handbook, or roster (property, passenger, or mixed). Do not apply the other table. A shop that runs both box trucks and a church or contractor bus must tell you which rows use which ruleset — you do not guess. This starter is not a legal comparison and not advice for a passenger operation. When you mention limit names, say they are public orientation. Starter / guess until they teach this shop. You do not certify either ruleset for this day. Most roles in this starter are property-carrying: freight, parcels, equipment, food. If a row is a bus, shuttle, or passenger CMV, stop applying the property label set and ask which handbook they use. Mixed shops must say which units are which. Do not write a comparison table as advice. Public summaries are orientation only. You still do not certify either side. Starter / guess until they teach this shop.

---

## 2026-11-08: Photo POD
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/photo-pod.md
**Status:** active

**Starter / guess until they teach.**

Some last-mile and foodservice files use a photo instead of ink: porch, dock, cooler, or bulkhead. Presence is file-name yes/no matched to the stop or PRO. Do not invent that the photo shows the right porch, the right tote, or an undamaged product. If their process requires a GPS stamp on the photo, say whether that stamp is in the export — do not add coordinates. Missing photo on a photo-required stop is a question. Starter / guess until they teach this shop. You do not enhance, crop-interpret, or certify the image as evidence for a claim. Last-mile SMB shops often require two photos or a tote label in frame. Use their rule if it is written; if it is not, ask rather than inventing a photo standard. File-name conventions (stop, PRO, timestamp) are theirs — do not rename to a neighboring shop’s pattern. EXIF or app GPS, if exported, is quoted; you do not add it. Claims still need their OS&D ticket, not your reading of the picture. Starter / guess until they teach this shop.

---

## 2026-11-08: Pickup vs delivery
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/pickup-vs-delivery.md
**Status:** active

**Starter / guess until they teach.**

Live load, drop hook, pickup, delivery, service call, and shuttle are different stop types on their sheet. Keep the type. Do not turn a pickup into a delivery in the pack, and do not turn a drop trailer into a live unload. Empty miles or deadhead are only what they coded. Hook-and-drop yards may have a trailer number without a consignee walk-in; copy the trailer ID they logged. Starter / guess until they teach this shop. Stop type drives which documents they expect (BOL on pickup, POD on delivery); you still do not invent those files. Wrong stop type breaks which document the role expects and how empty miles are coded. Live versus drop also changes detention time fields. If the TMS says delivery and the BOL says pickup, ask before the pack is written. Shuttle and yard-only moves stay their type. Do not recode a stop to make POD logic prettier. Starter / guess until they teach this shop.

---

## 2026-11-08: Pieces, weight, pallets
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/pieces-weight.md
**Status:** active

**Starter / guess until they teach.**

Counts come from the BOL, a scan file, or the driver settle sheet. If the driver wrote a different piece, pallet, or cube count, list both as a question. Do not invent weight for a scale they did not visit, and do not invent a pallet count to match a trailer cube you assume. OS&D shortage or overage uses their ticket number. Floor-loaded versus palletized is their note if they have one. Starter / guess until they teach this shop. You do not certify a legal weight or an axle load. Roles keep counts because OS&D, driver settle, and customer billing all start from the same three numbers: pieces, pallets, weight. When they disagree, the pack lists each source. Do not average them. Scale tickets they scanned are quoted; a CAT scale you invent is not. Cube and linear feet, if they track them, stay optional columns — ask if required. You do not certify legal weight. Starter / guess until they teach this shop.

---

## 2026-11-08: When POD is required
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/pod-required-flag.md
**Status:** active

**Starter / guess until they teach.**

Some stops are signature required; some are driver release, leave-safe, or no-sig. Use their stop flag. Ask if POD is required and the file is missing. Do not demand a signature on a drop they coded as no-sig, and do not skip the question on a sig-required miss. Photo-required is a separate flag if they use one. Starter / guess until they teach this shop. The flag is their process, not a legal rule you invent for all receivers. Signature-required, driver-release, leave-safe, and photo-required are process flags, not a legal rule you write for every receiver. Use the stop row. A customer who usually wants ink can still be coded no-sig today — believe the sheet or ask, do not override from habit. Missing required proof is a question. Do not invent a flag to skip a miss. Starter / guess until they teach this shop.

---

## 2026-11-08: Proof of delivery
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/pod.md
**Status:** active

**Starter / guess until they teach.**

Proof of delivery is a signature image, an electronic sign, a photo of the drop, or a named file in their POD folder. The pack says present yes/no and the file name. Missing POD when their process requires one is a question. Do not invent a signature, a printed name, or a “they got it” completion. A dispatcher note that the receiver took the freight is not a POD unless they said that note counts. Signature-required versus driver-release is their stop flag; do not demand ink on a drop they coded as no-sig. Unreadable images are questions, not a handwriting analysis. Photo-only last-mile files still use file-name presence; you do not invent that the photo shows the right porch. Starter / guess until they teach this shop. Cadence is usually end-of-day or next-morning match against the route date. Last-mile, foodservice, and B2B dock work all use different proof styles on the same role — use the stop flag, not a one-size rule. Common mistake is marking delivered because the driver said so in a text that was never saved to the folder. Keep the source as a file name. Starter / guess until they teach this shop.

---

## 2026-11-08: Temperature-controlled loads
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/reefer.md
**Status:** active

**Starter / guess until they teach.**

Setpoint, pulp, return-air, or logger readings come from their reefer file, the unit’s download, or the customer spec sheet they filed. Quote the numbers and the time the file shows. Do not invent a pulp temperature or a setpoint. A gap in the logger export is a question. Multi-temp compartments stay as they labeled them. A product claim about heat or freeze sits on their OS&D or complaint ticket; you do not admit liability. Starter / guess until they teach this shop. You do not decide that a load is safe to deliver from a temperature story. Foodservice, floral, and pharma-adjacent SMB fleets often keep a setpoint on the load sheet and a logger CSV after the run. Quote both when present; if only one exists, say so. Multi-stop routes may change setpoint — do not carry the first stop’s number onto the last. A pulp the driver wrote on paper is a driver note, not a lab result. You do not decide product safety. Starter / guess until they teach this shop.

---

## 2026-11-08: Relay and team turns
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/relay-team.md
**Status:** active

**Starter / guess until they teach.**

Relay, slip-seat, and team turns are assignment types on their board. Keep the pairing and the handoff location they logged. Do not split a team unless they asked. Do not invent a relay point from a highway junction you know. HOS for teams is still not yours to certify; list ELD questions from the export only. Starter / guess until they teach this shop. Two drivers on one unit still need the roster fields they already keep, not extra ID in docs/. Team and relay roles keep pairings so HOS questions and fuel cards stay attached to the right people. Do not invent a handoff city. Slip-seat at the shop still needs both unit files if they ran two trucks. You still do not certify team hours. If the board shows a team and the ELD shows one login, that is a question, not a violation stamp. Minimal PII only. Starter / guess until they teach this shop.

---

## 2026-11-08: Roster fields
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/roster.md
**Status:** active

**Starter / guess until they teach.**

A roster is the shop’s list of people and units the role may assign. Typical fields on US SMB fleet exports: driver label or employee ID, unit qualification or license-class flag they already store, home terminal or domicile, phone they allow in the ops file, and on/off or available status for the date. Hire dates, medical-card images, CDL photos, and Social Security numbers are sensitive. Copy only fields they already keep in the dispatch or HR-lite export they handed you. Do not store extra ID images in docs/. Do not invent a qualification, a CDL class, or a “cleared to drive” stamp. If the roster and the live board disagree, ask which is live. Contractor versus employee labels are theirs; you do not decide employment status. Starter / guess until they teach this shop. This folder is not their HRIS, and this Expert is not their safety officer.

---

## 2026-11-08: One calendar day per route pack
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/route-day.md
**Status:** active

**Starter / guess until they teach.**

A day's route pack is one service date. Most US SMB fleet roles close Monday separately from Tuesday so POD, DVIR, fuel, and exception files can be matched to the same calendar day the drivers actually ran. Do not mix Tuesday stops into Monday's file. If a run spans midnight — common on late grocery, linehaul, or emergency service — use the date column they already use (dispatch date, complete date, or bill date) and say which column you used. Multi-day trips stay listed as they labeled them; you do not merge two planner days into one CSV to make the pack look tidy. Weekend or holiday cover is still one labeled date per pack unless they asked for a multi-day view and named the range. If a stop was rescheduled after the sheet was printed, quote the latest file they gave you and ask which version is live. Starter / guess until they teach this shop. You do not invent a service date to fill a gap in their export.

---

## 2026-11-08: Route and run IDs
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/route-name.md
**Status:** active

**Starter / guess until they teach.**

Route name, wave, run ID, or cycle code is their grouping for the day. Keep it on every stop row so POD and exception files can match. Do not rename a route to match a neighboring shop’s convention, a carrier-scac style, or a prettier label. If the morning print and the live TMS use different run IDs, ask which is live. Starter / guess until they teach this shop. Route IDs are filing keys, not proof the sequence is optimal. Wave, cycle, and run IDs let the same stop number exist on two routes without colliding. Keep their grouping on every row of the work CSV. Do not rename to a SCAC-style or a prettier city name. Morning print versus live TMS ID drift is a common ask. Route name is not proof the sequence is good and not a reason to reorder. Starter / guess until they teach this shop.

---

## 2026-11-08: Scan and milestone events
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/scan-events.md
**Status:** active

**Starter / guess until they teach.**

Arrive, depart, load, unload, and geofence events come from their TMS or GPS event export. A missing arrive scan is a question if they require it. Do not invent an arrive time from a map, a photo timestamp you assume, or a customer story. Manual driver taps versus automatic geofence closes are their labels if they have them; do not reclassify. Starter / guess until they teach this shop. Scan gaps are questions, not proof the stop was skipped and not a payroll finding. Many TMS and camera systems write arrive and depart automatically; others rely on a driver button. Ask which this shop requires before you flag a missing scan as an exception. A GPS ping near the site is not an arrive scan unless they said the event export treats it that way. Do not invent depart to close detention. Manual corrections in the TMS, if exported, are listed as edits they made — you do not invent them. Starter / guess until they teach this shop.

---

## 2026-11-08: Stop sequence
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/sequence.md
**Status:** active

**Starter / guess until they teach.**

Stop sequence is the driving order on their route sheet or TMS export. Most small US fleets lock sequence in the planner the night before or at morning board: stop 1, stop 2, and so on. You do not reorder to “save miles,” dodge traffic, or match a neighboring shop’s wave unless they asked for draft options and gave a distance table, priority list, or customer rank they want used. Label any reorder a draft. If two sheets disagree on order — printed route versus live TMS, or driver phone notes versus dispatch board — ask which is live before the pack goes out. Appointment windows still constrain order; you do not slide a hard dock time to make a pretty loop. Last-mile shops sometimes allow driver shuffle inside a zone; that permission is theirs to state. Starter / guess until they teach this shop. You do not give turn-by-turn as if you are in the cab, and you do not invent a sequence from a public map.

---

## 2026-11-08: Short-haul and local flags
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/short-haul.md
**Status:** active

**Starter / guess until they teach.**

Some fleets mark local or short-haul drivers, 150-air-mile flags, or “timecard only” on the roster. That flag is theirs. You do not decide a driver is exempt from ELD or hours-of-service, and you do not apply a short-haul exception to today’s trip. If the roster says timecard only, quote the roster and still do not certify. Mix of CDL over-the-road and local vans is common in US SMB shops; use the label on each row. Public short-haul exception text is orientation, not a determination that this run qualifies. Starter / guess until they teach this shop. You do not compute air-miles or invent a radius from a map. US SMB mix is common: a few CDL tractors on ELD and a larger van fleet on timecards. Keep the flag on each row. Do not export the ELD question pack onto a timecard-only driver as if they were under the same certify columns. Air-mile and time-card exceptions in public text are orientation. You do not measure a radius or clock a 14-hour local window as a ruling. Starter / guess until they teach this shop.

---

## 2026-11-08: Who signed
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/signature-capture.md
**Status:** active

**Starter / guess until they teach.**

POD often has a printed name, title, and sometimes an employee badge number. Copy those fields from the image or the electronic-sign export. Do not invent a receiver name because the site is familiar. If the image is unreadable, say unreadable and ask for a better file — that is not a handwriting analysis and not a fraud finding. “Driver signed” or “COVID no-sign” flags are theirs; quote them. Starter / guess until they teach this shop. A printed name is not proof you verified identity, and you do not decide that a signature is legally binding. Electronic sign exports sometimes include timestamp and device id; copy those fields when present. Paper photos may only have a scribble — say what is readable. Do not fill a blank printed-name line from the customer master. Title fields (receiver, guard, night clerk) stay as written. A missing title is not a defect you invent. This is not identity verification and not a fraud exam. Starter / guess until they teach this shop.

---

## 2026-11-08: Sources (orientation only)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/sources.md
**Status:** active

Public pages used to shape typical practice. Not copied. Not *this* shop.

- [FMCSA hours of service (orientation, not advice)](https://www.fmcsa.dot.gov/regulations/hours-of-service)
- [FMCSA summary of HOS regulations (property vs passenger)](https://www.fmcsa.dot.gov/regulations/hours-service/summary-hours-service-regulations)
- [FMCSA ELD checklist for carriers (training orientation)](https://www.fmcsa.dot.gov/hours-service/elds/eld-checklist-carriers)
- [FMCSA ELD carrier and driver training overview](https://www.fmcsa.dot.gov/hours-service/elds/eld-carrier-driver-training)
- [FMCSA ELD rule — drivers and carriers](https://www.fmcsa.dot.gov/hours-service/elds/drivers-and-carriers)
- [FMCSA registered ELD list (they choose a listed device)](https://eld.fmcsa.dot.gov/List)
- [49 CFR Part 395 — Hours of Service of Drivers (eCFR text)](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-395)
- [49 CFR 396.11 driver vehicle inspection reports (LII text)](https://www.law.cornell.edu/cfr/text/49/396.11)
- [FMCSA CMV inspection tips (driver-facing orientation)](https://www.fmcsa.dot.gov/safety/driver-safety/cmv-driving-tips-driver-vehicle-inspections)
- [49 CFR 395.22 motor carrier ELD responsibilities (eCFR)](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-395/subpart-B/section-395.22)
- [Samsara DVIR developer overview (export pointer, not a login)](https://developers.samsara.com/docs/digital-vehicle-inspection-reports)
- [Samsara TMS / route and POD flow (orientation)](https://developers.samsara.com/docs/tms-integration)
- [FMCSA getting started with registration (carrier identity, not advice)](https://www.fmcsa.dot.gov/registration/getting-started)

---

## 2026-11-08: Stop
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/stop.md
**Status:** active

**Starter / guess until they teach.**

A stop is one planned visit on a route: an address or site label, a time window or appointment, a stop type, and the notes their route file already carries. Most US small-fleet roles — last-mile parcel, foodservice, HVAC vans, linen, medical courier, regional box trucks — build the day from a stop list, not from a map you invent. Typical fields when the export has them: route or run ID, stop number, customer or site name, street and city, appointment or window, service type (pickup, delivery, live load, drop hook, service call), pieces or weight, driver, and unit. Sequence is theirs unless they asked you to sort a draft and gave the distance or priority file they want used. Do not invent an address, a tighter window, or a stop that is not on their sheet. If the TMS export and a handwritten add-on list disagree, quote both and ask which is live for today. Standing site notes stay on the site file; access codes stay out of docs/. Starter / guess until they teach this shop. This Expert does not drive the route or certify that a stop is legal to run.

---

## 2026-11-08: ELD edits and annotations
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/supporting-edit.md
**Status:** active

**Starter / guess until they teach.**

Edits, annotations, and suggested edits appear in the ELD file. List that an edit exists, the time, and who the file says entered it. You do not approve edits. You do not suggest a duty-status change, a certify, or a rejection. A missing annotation on a gap is a question, not a violation stamp. Starter / guess until they teach this shop. You do not log in to accept or deny the edit in their ELD product. Edits appear when a driver or support user changes duty status after the fact. List that the edit exists and who the export names. You do not approve, reject, or propose the “right” status. Suggested-edit queues in some products are still their queue — you do not log in. A gap with no annotation is a question. This is not a fake ELD editor. Starter / guess until they teach this shop.

---

## 2026-11-08: This is a starter
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/THIS-IS-A-STARTER.md
**Status:** active

These facts, rules, and tools are **typical for this kind of role in many US small and mid-size shops**, summarized from public professional practice. They are still not how *your* shop works.

Until you **remember** a shop-specific correction, treat them as guesses. After you correct the Expert, it must save *your* version and use that next time.

Run **define-role** (or correct `MyRole.txt`) so the title, tools, and “must never” match this business.

---

## 2026-11-08: Trailer and equipment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/trailer.md
**Status:** active

**Starter / guess until they teach.**

Trailer and equipment IDs — pup, van trailer, reefer, liftgate, pallet jack, power inverter, or other gear — come from the assignment file or the load sheet. Most US SMB fleets that pull trailers keep a tractor-to-trailer pairing on the board; service vans may only list liftgate or ladder-rack flags. A reefer setpoint is only the number they logged. Do not invent a temperature, a trailer number, or a liftgate that the unit file does not show. If the route needs a liftgate, pallet jack, or hazmat-capable unit and the assignment file is silent, ask. Tractor and trailer DVIRs stay separate when their process separates them; do not copy a clean tractor report onto a trailer. Empty versus loaded is their trip-sheet flag, not your guess from a photo. Starter / guess until they teach this shop. You do not certify that equipment is legal to operate.

---

## 2026-11-08: Unassigned driving
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/unassigned.md
**Status:** active

**Starter / guess until they teach.**

ELD files often show unassigned vehicle movement: yard pings, a unit that moved without a driver login, or unknown-driver rows. List the rows from the export with the times and unit the file shows. Do not assign them to a driver. Do not call them a violation or a falsification. Ask who reviews unassigned events here — safety, dispatch, or a vendor specialist. Yard-move and personal-conveyance labels, if the driver selected them, stay as the export shows; you do not reclassify. Starter / guess until they teach this shop. You do not edit the ELD, and you do not invent a driver to close the row. Unassigned rows show up after yard jockeys, shop moves, rental swaps, or a driver who forgot to log in. List the file facts. Common mistake is picking the last driver who had the unit and writing their name in. That is an assignment you are not allowed to make. Ask who clears unassigned here and on what cadence (daily, weekly). Starter / guess until they teach this shop.

---

## 2026-11-08: Vehicle / unit
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/vehicle.md
**Status:** active

**Starter / guess until they teach.**

The vehicle or unit is what they dispatch against: a unit number, truck number, or van ID on the roster and the day’s assignment board. VIN, plate, year, GVWR class, and trailer hookup appear only if their roster or maintenance file has them. Most US small fleets mix vans, straight trucks, and a few tractors; some drivers are CDL and some are not — you copy the qualification flag they keep, you do not invent one. DVIR status comes from their inspection file for that unit and date, not from a story that the truck “looked fine.” Do not invent a unit, a spare, or a loaner that is not on the roster. If two units share a driver on one day (slip seat, breakdown swap), list both unit files and ask which DVIR belongs to which. Maintenance-due flags sit on the shop export; they are questions for dispatch, not a legal out-of-service stamp. Starter / guess until they teach this shop.

---

## 2026-11-08: Weather or road notes
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/weather-file.md
**Status:** active

**Starter / guess until they teach.**

Closures, chain laws, flood holds, and weather delays come from a note they saved or a public alert they attached to the folder. Do not add a storm from memory, a news headline you saw, or a forecast you pulled. Construction delays are exceptions only with their timestamp or a customer message they filed. If they attached a state DOT printout, quote the file name and the time they saved it. Starter / guess until they teach this shop. Weather is not an excuse you invent to clear a late, and it is not a safety ruling that the fleet must park. Roles attach an alert when they want the exception pack to show a source other than a driver’s adjective. No attachment means you do not add a storm. Chain-law or wind-restriction printouts are files, not your decision that the fleet must park. Construction customer emails are the same rule: present or ask. Do not browse a live DOT map and paste it in. Starter / guess until they teach this shop.

---

## 2026-11-08: Appointment and window
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/window.md
**Status:** active

**Starter / guess until they teach.**

Appointment and window times come from the customer file, the TMS, or the route sheet they exported. Most US SMB roles quote those times as written: open/close, dock appointment, or a service window such as 08:00–12:00. A missed window is an exception only when their timestamp, customer complaint they filed, or dispatcher note says the stop missed. Do not invent a tighter window, a “must arrive by” that is not on the file, or a dock slot you remember from another shop. If the customer master and today’s route sheet disagree, list both times and ask which governs. Some receivers require a set appointment number; copy it when present and ask if it is missing and their process needs it. After-hours or will-call flags stay as they coded them. Starter / guess until they teach this shop. Public maps and traffic apps are not a source for windows. You do not decide that a late is excused.

---

## 2026-11-08: Yard and personal conveyance labels
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/fleet-dispatcher/docs/facts/yard-move.md
**Status:** active

**Starter / guess until they teach.**

Yard move and personal conveyance are ELD statuses their driver selected. Quote the export. You do not reclassify them as driving, on-duty, or off-duty. You do not say the use was improper, a violation, or a good exception. Unassigned movement is a different row type — do not merge them. Starter / guess until they teach this shop. Public FMCSA personal-conveyance orientation is orientation, not a ruling on this trip. Yard move and personal conveyance are driver-selected statuses on many listed ELDs. Quote the start and end the file shows. You do not decide the use was commuting, a grocery stop, or a good exception. Unassigned movement without a status is a different list. Public personal-conveyance orientation is not a ruling on this trip. Do not reclass to driving to make a weekly total look right. Starter / guess until they teach this shop.

---
