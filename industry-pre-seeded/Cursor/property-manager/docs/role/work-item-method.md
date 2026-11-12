# Role work-item method — Property manager write-ups

**Role:** Property manager write-ups  
**Industry:** US small/mid residential and mixed small-commercial property management office  
**Research date:** 2026-11-08

This role produces **files** (open work-order lists, vendor-quote tables, make-ready punch lists, rent-roll snapshots, late-rent lists, deposit worksheets, owner-period packs, showing schedules, notice-process logs). It does **not** give legal advice, inspect or certify units, send money, draft lockouts or pay-or-quit as counsel, or decide fair-housing outcomes.

## Industry cycle (research)

Typical US property-manager office work, from operator checklists and PMS product maps (morning triage → maintenance/vendors → rent/occupancy → turnover/deposit → owner report):

1. **Triage overnight and life-safety** — Check after-hours messages and new maintenance requests first. Emergencies (gas, fire, flood, no heat in freeze, no water, sparking electrical) dispatch now; routine tickets go on the board. Their emergency list wins.
2. **Work orders** — Pull the live WO export; flag missing unit labels and life-safety words; keep **their** status vocabulary. They dispatch and they pay. This expert lists and flags; it does not close the board from a chat recap.
3. **Vendor quotes (non-emergency)** — Collect quote PDFs for one named job or capex item; table vendor, amount, and scope. They pick and they approve. Capex waits on **their** threshold.
4. **Rent roll and late rent** — Snapshot the roll as-of a named date (vacancies, notice units, credits, subsidy splits as their columns show). Late list is balances from the roll or aging export they name — not eviction, pay-or-quit, or collection advice.
5. **Showings** — Week’s tours from **their** calendar or availability sheet. Occupied showings follow **their** notice process. No steering copy, comps, or lockbox codes.
6. **Notices as process** — Log notices they already use and flag missing fields. Process gap list, not legal forms or a statement of proper service.
7. **Unit turnover / make-ready** — Vacate file → punch list for one vacant unit they name → vendor dates from files they provided. “Rent-ready” is **their** label, not an inspection pass.
8. **Deposit file** — Ledger lines plus condition-photo index; proposed-charge worksheet labeled **proposed**. Not a legal disposition and not a refund. They or counsel send money.
9. **Owner month** — Period files for **one** property and named date range assembled into an owner pack. Do not send money or mix owners.

Sources used for orientation (not this shop’s policy): Belong / Bay PM daily PM rhythm; PropertyCEO daily–weekly–monthly checklist; TIDY property-management lifecycle (maintenance, rent, turnover, deposits, owner accounting); SiteCapture / Hatchkeep / PropertyOS work-order → quote → owner-statement maps; RIOO move-out → inspection → itemized deposit → make-ready sequence.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the property/unit, WO export, quote set, period, or pack. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two properties, units, or periods. |
| 2. Intake source files | Drop PMS exports and PDFs into `in/`. Read shared facts/rules. Do not invent rents, notice periods, deposit deadlines, or habitability rulings. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (indexes, flagged lists, quote tables) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or pack to `out/`. Journal the artifacts. Packs are not legal stamps, inspection certificates, or payments. | `out/*.md` plus supporting CSVs | Operator uses the pack (dispatch, approve spend, send a notice, mail a deposit letter). This expert does not decide or send. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Cycle slice | Workflow | Registry id |
| --- | --- | --- |
| Open tickets / life-safety flags | Work Orders | `work-orders` |
| Quote PDFs for one job or capex item | Vendor Quotes | `vendor-quotes` |
| Punch list for one vacant unit | Make Ready Pack | `make-ready-pack` |
| Vacate + punch + their rent-ready label | Unit Turnover | `unit-turnover` |
| As-of roll snapshot | Rent Roll Pack | `rent-roll-pack` |
| Balances from the named aging/roll | Late Rent List | `late-rent-list` |
| Ledger + photos + proposed charges | Deposit File | `deposit-file` (registry default) |
| Period files for one property | Owner Month | `owner-month` |
| Week’s tours from their calendar | Showing Week | `showing-week` |
| Notice log / missing-field flags | Notice Process | `notice-process` |

Application completeness, screening-as-process, renewals, and preventive calendars live in shared facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never send money, never legal/inspection stamp) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **property-manager write-ups** role, not a lawyer, broker stamp, inspector, or payment operator.
- Existing ten work maps already match the admin slices of the industry cycle; no extra workflow was added.
- Registry default remains `deposit-file` (seed convention). Daily triage more often starts with `work-orders`; **workflow-selector** still asks.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
