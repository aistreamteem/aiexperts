# Role work-item method — Self-storage office

**Role:** Self-storage office  
**Industry:** US self-storage facility office (SiteLink / storEDGE / SSM / spreadsheet exports)  
**Research date:** 2026-11-08

This role produces **files** (unit-mix counts, occupancy lists, rate tables, waitlists, move-in completeness sheets, late lists, photo indexes, auction-file gap packs). It does **not** hang or remove overlocks, issue gate codes, take or send money, approve a lien or auction, or give legal advice.

## Industry funnel (research)

Typical US facility-manager / storage-office work, from operator manuals and PMS practice (inventory → rent → occupancy → delinquency ladder → lien/auction file):

1. **Unit mix and rates** — Know what sizes and climate vs standard units exist; quote street / web / in-place / promo numbers only from the live rate file. Offices keep a unit master and a dated rate sheet (SiteLink inventory map; mix CSV).
2. **Waitlist** — Keep names in **their** existing order with size wanted and date added. A seat is not a hold unless occupancy already codes a reservation. They call the next person.
3. **Move-in packet** — Agreement PDF, ID under min-necessary, insurance/protection or waiver if their checklist requires it, rate from the rate file. Completeness is present-or-missing. They take payment and they issue access.
4. **Occupancy / rent roll** — Occupied, vacant, reserved, company, damaged, and auction-hold as **their** export coded them. Do not invent vacant from a photo.
5. **Transfers** — Old unit, new unit, date, whether a new agreement exists. They approve the swap.
6. **Condition photos** — Index named photos against occupancy or vacant units. They shoot and they mark ready.
7. **Late list / delinquency ladder** — From payment-status and their late export: units coded past due, paid-through, autopay-failed flags. They contact occupants. Overlock is a status they coded, never a combination in docs. This expert does not hang metal or rerun cards.
8. **Auction / lien file completeness** — Compare **their** auction checklist to notices, certified-mail log, inventory form, photos, calendar date, buyer log. Completeness is not permission to sell. State lien law is theirs and counsel’s.

Physical lock walks, daily bank deposits, hanging overlocks, and mailing lien notices are **on-site manager work**. This expert packs the lists and gap files those steps need.

Sources used for orientation (not this shop’s policy): Arizona Self Storage Association training & procedures manual (daily occupancy/collections, weekly lien-file review); SiteLink / Storable occupancy map and StorageAuctions integration (checklist fields, photos, sale date they enter); facility-manager job descriptions (HandyLock, Sentry, Boxer — lock-action reports, collections worksheet, auction files); Callsphere-style morning delinquency ladder (overlock list, declined ACH, lien-notice clock); MyTeamTask / SOP daily checklists (move-in ID + insurance + photo; document every lien step).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the unit, move-in, occupancy date, late pull, auction file, or period. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two units unless they named a combined pack. |
| 2. Intake source files | Drop SiteLink / storEDGE / SSM / spreadsheet exports and PDFs into `in/`. Read operations facts/rules. Do not invent rates, late fees, hours, or auction dates. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (lists, missing-forms, indexes) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or completeness pack to `out/`. Journal the artifacts. Completeness packs are not legal stamps or collections calls. | `out/*.md` plus supporting CSVs | Operator uses the pack (call a late occupant, chase a missing agreement, add a unit to **their** auction calendar). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Auction / lien file present-or-missing | Auction File Completeness | `auction-file-completeness` (default) |
| Past-due units from their export | Late List | `late-list` |
| Agreement + ID + insurance checklist | Move In Packet Completeness | `move-in-packet-completeness` |
| Occupied / vacant / hold as they coded | Occupancy | `occupancy` |
| Named photos vs units | Photo Condition Pack | `photo-condition-pack` |
| Street / web / in-place / promo table | Rate From File | `rate-from-file` |
| Unit swaps and leftover agreements | Transfer List | `transfer-list` |
| Size × climate vs standard counts | Unit Mix | `unit-mix` |
| Waitlist in their order | Waitlist | `waitlist` |

Overlock, gate-access **process**, NSF flags, insurance asks, and “do not invent a fee” live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never lien/auction legal, never store codes or PAN) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **storage-office admin** role, not a licensed auctioneer, facility-manager owner pack, or attorney.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Default registry job remains `auction-file-completeness` (highest-risk file pack on this role).
