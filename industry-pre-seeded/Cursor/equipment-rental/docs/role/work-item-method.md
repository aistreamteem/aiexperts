# Role work-item method — Equipment rental role

This role does **not** run software HLD/DD/implement. A Work Item is one rental job, day-list, or pack (a contract, reservation day, delivery run, inspection set, COI chase, meter exception, PM conflict, return-damage pack, or utilization list).

Industry sources for the phase list (typical US/UK hire-role practice, not this yard until the operator confirms): L Lynch hire-role procedure; construction-rental software stage models (quote → allocate → inspect → dispatch → on-rent → return → service/reporting); rental-coordinator contract completeness; gate check-out / check-in inspection with photos and meters; COI before release; utilization by class.

## Typical phases

| Phase | What happens | Artifacts (under the Work Item) | Human gates |
| --- | --- | --- | --- |
| 1. Identify the job | Name the day, contract, reservation, serial, or pack. Open one Work Item so jobs do not mix. | `work-items/<id>/` (`in/`, `work/`, `out/`, `evidence/`) | Operator names the job; do not dump into another item’s folder. |
| 2. Intake source files | Read what they dropped: fleet export, rate file, reservation CSV, contract PDFs, inspection sheets, photos, COI folder, zone sheet, PM file, meter/telematics export. | Copies or pointers in `in/` | Missing required file → ask. Do not invent a rate, meter, serial, zone, deposit, or fee. |
| 3. Availability and reservation | Reserved vs available vs on-rent; overlaps only by their overbook rule. | Reservation list, exception notes | Substitution and overbook are questions unless their file already says how. They call renters. |
| 4. Contract completeness | Required fields vs PDFs and the rate file: renter, unit/serial, dates, rate lines, waiver/RPP box, tax/exempt pointer, PO, COI if required. | Missing-fields list | Draft is not signed out. They sign and they collect. No PAN in the pack. |
| 5. Release screening | COI presence and checklist fields; outgoing inspection (meter, fuel, kit, photos, manual). | COI miss list; outgoing incompletes | They hold the gate. No coverage opinion. No operator-license stamp. No indoor-height engineering. |
| 6. Dispatch | Delivery and pickup tickets with zone from their zone sheet. | Run list, address/zone exceptions | Do not invent miles, zone letter, or ETA. Do not pay the hauler. Gate codes stay out. |
| 7. On-rent watch | Meter/telematics vs inspection hours; PM-due vs reservation or on-rent. | Meter exceptions; maintenance conflicts | Do not invent hours or a PM interval. Do not diagnose a rolled meter or a repair. They shop, sub, or override. |
| 8. Return and condition | Return inspection vs outgoing: new marks, missing kit, fuel and cleaning codes, photos. | Difference list | Do not invent damage, repair dollars, or fees. No collection lawsuit. They post charges. |
| 9. Fleet reporting | Utilization from their export or written formula; idle and shop stay visible. | Utilization list | Do not invent a percent or a dollar view. They decide transfers, sales, or rate-file changes. |
| 10. Close the pack | Finished files in `out/`, check logs in `evidence/`, journal updated. Promote durable shop facts/rules if asked. | Pack + journal STATUS | Operator accepts the pack. Starter notes are guesses until they confirm this yard. |

## Which registered workflows cover which phases

| Workflow | Phases |
| --- | --- |
| `reservation-day` | 1–3 |
| `contract-completeness` | 1–2, 4 |
| `renter-coi-missing` | 1–2, 5 |
| `outgoing-inspection` | 1–2, 5 |
| `delivery-tickets` | 1–2, 6 |
| `meter-exceptions` | 1–2, 7 |
| `maintenance-due` | 1–2, 7 |
| `return-damage` | 1–2, 8 |
| `utilization` | 1–2, 9 |

Default job when the operator has not named one: `contract-completeness`.

## How a Work Item runs (expert skills, not old role glue)

1. **continue** / **workflow-selector** — pick the registered job; keep state in `journals/work-items/<id>/`.
2. Follow the selected `.cursor/workflows/<id>.md` file. Each step names a tool under `docs/tools/`, a file to produce, and a check command.
3. Paths `work/` and `out/` in a work map mean **inside** `work-items/<id>/`.
4. **journal-keeper** after each ready step, operator answer, or blocker.
5. Missing shop knowledge or a conflict with a saved file → **operator-qa** (or ask in chat). Do not invent how this yard works.
6. Durable notes → **remember** into `facts/facts-operations.md` or `facts/rules-operations.md` (or the Work Item `facts/` files).
7. Finished pack lives in the Work Item `out/`; checks and command logs in `evidence/`.

## Out of this method

Repair diagnosis, inventing rates, paying vendors, running cards, operator-license stamps, indoor-height engineering, and debt collection as a lawsuit. See `MyRole.txt`.
