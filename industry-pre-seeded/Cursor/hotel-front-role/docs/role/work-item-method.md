# Role work-item method — Hotel / inn front role

**Role title:** Hotel / inn front role  
**Research date:** 2026-11-08  
**Sources (industry practice, not this property):** StayNTouch hotel PMS front-role workflow (pre-arrival → check-in → in-stay → checkout → shift handover → night audit); RMS Cloud daily procedures (today’s arrivals, due-outs, in-house, housekeeping status); LuxOps front-role daily checklist (night-audit report, VIP/arrivals, room status with housekeeping, written handover); SetupMyHotel / ExecuTech group SOP (block, pickup, cutoff, rooming list); BookingCenter / RoomMaster night-audit SOP (folio review, no-shows, house accounts, manager reports).

This Expert is a **file role**, not a card-running or live-PMS operator. The operator drops PMS exports and PDFs. The Expert builds lists and exception packs. They assign rooms, check guests in or out, post charges, run cards, and run night audit.

Starter notes in operations memory are typical US inn practice until the operator confirms how *this* property works.

## Typical phases for a Work Item

| Phase | What happens | Artifacts (under `work-items/<id>/`) | Human gates |
| --- | --- | --- | --- |
| 1. Identify the job | Name the stay date (or reservation/group) and the registered role job. Open one Work Item so days do not mix. | `in/` ready; journal workflow type set | Operator names the job and date. Unclear item → ask. |
| 2. Intake source files | Collect the PMS export, room-status sheet, folio PDFs, tax file, group sheet, or night-audit PDF this job needs. | Files in `in/` (copies in `work/` as steps require) | Missing export, rate grid, or tax file → ask. Do not invent. Visible PAN → stop and ask for a redacted file. |
| 3. Walk the registered workflow | Follow the named file under `.cursor/workflows/`. Read each `docs/tools/` note. Produce the step file. Run the listed check. | `work/*.csv` (or copied PDFs) | A step whose `needs` file is missing does not start. Check fail → retry at most 3, then ask. |
| 4. Flag exceptions and asks | DNR matches, overbook/walk risk, OOO vs sellable-type clash, tax-off without a cert, comp without a code, blank cutoff, blank OOO return. | Exception rows on the working sheet | Manager asks stay asks. ADA stays inventory labels, not law. Rates/taxes stay their file. |
| 5. Pack | Assemble the list plus a short operator pack (docs used, artifacts, checks). | `out/<job>.md` and supporting files | Operator reviews the pack. Corrections → **remember** (or Work Item facts/rules). |
| 6. Close | Journal completion. Optional **promote-facts-rules** for durable property knowledge. | Journal STATUS; optional promotion | Pack accepted or exceptions recorded. |

**Continue** walks **one ready step**. It is not approval of an open question.

## Registered workflows (which phase they cover)

Default job: `arrivals-day`.

| Registry id | Industry moment | Phase coverage |
| --- | --- | --- |
| `arrivals-day` | Pre-arrival / check-in prep | Expected arrivals vs room-status ready/not-ready. They check guests in. |
| `departures-due-out` | Checkout / due-outs | Due-out list from in-house + status. Unsettled folios are exceptions. They check guests out. |
| `house-count` | In-stay / flash | Tonight’s occupied, vacant-sellable, OOO, arrivals-not-in, due-outs from their report. |
| `ooo-and-status` | In-stay / rooms | OOO and status-board rooms; clash when OOO ate the last sellable type. |
| `group-block-vs-pickup` | Groups | Contracted block vs pickup, cutoff, wash as written. They cut or wash. |
| `folio-exceptions` | Billing review | Missing/duplicate posts, tax-off without cert, comps without code, POS mismatch. They adjust. |
| `tax-exempt-completeness` | Billing / tax | Tax-exempt folios vs certificates present, expired, name-mismatch. They apply or reverse tax. |
| `no-show-list` | Close of day | Arrivals that did not check in vs night-audit codes. Fees from *their* policy only. They post. |
| `night-audit-file-check` | Night audit packet | Completeness of the packet they dropped vs PMS export. They run audit and roll the date. |

Shift open, cash drawer, key encode, and live check-in/out stay **their** PMS and **their** process. This Expert does not run those as a product.

## Canonical expert skills (process)

Starting work → **workflow-selector** + Work Item under `work-items/<id>/` + **continue**.  
Stepping a job → this method + the registered workflow file + **journal-keeper**.  
Clarification → **operator-qa**.  
Durable notes → **remember** / **integrate-docs**.  
Scope and refuse → `MyRole.txt` + `facts/rules-operations.md` + `.cursor/rules/expert.mdc`.

Process needs are covered by **continue**, **journal-keeper**, **workflow-selector**, **operator-qa**, **remember**, **integrate-docs**, Work Item folders, and these registered workflow files.

## Assumptions

- This seed is a **hotel / inn front-role file Expert**, not a card-running role, night auditor who rolls the date, ADA counsel, or OTA product.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Breakfast count and BEO remain operations facts, not extra registry jobs.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
