# Role work-item method — Auto body estimator / office

This expert runs **collision-shop office** work: assignment, claim, photos, estimate packs, supplements, parts-vs-estimate, authorization, and cycle time. It does **not** run a software HLD/DD/implement pipeline, a mechanical service-advisor RO, or a technician diagnosis.

Industry steps below come from common US collision / DRP estimator practice (assignment → inspect/photo → write estimate → OEM procedures → insurer submit/auth → teardown/supplement → parts order → pay-type split → cycle time) plus this seed’s maps and shop constraints. Hours and prices always come from **their** labor matrix and parts file. Total-loss stays the insurer’s file.

## Typical phases

| Phase | What happens | Artifacts (under `work-items/<id>/`) | Human gates |
| --- | --- | --- | --- |
| 1. Assignment intake | Copy claim, VIN, DOL, insurer, mileage from the assignment sheet and VIN file. Do not invent an assignment. | `in/` source files; `work/` extracts; `out/` intake pack | Missing assignment on insurer-pay → ask. VIN mismatch → quote both and stop. Customer-pay with no assignment stays labeled customer-pay. |
| 2. Photo documentation | Index named photos (four corners, VIN, odometer, damage, prior damage). | `out/` photo index | Missing required angles stay missing asks. Do not hide prior-damage shots. |
| 3. Write estimate from files | Build an estimate pack from labor matrix, parts file, and estimate export. | `work/labor-matrix.csv`, `work/parts-file.csv`, `out/` estimate pack | Never invent hours or prices. Missing matrix or parts file → ask. No total-loss verdict. No structural/ADAS/engineering stamp. |
| 4. OEM procedures | Index procedure PDFs against estimate operations that their process says need a page. | `out/` procedure-present list | Missing procedure page on weld/section/scan/ADAS ops → ask. Do not invent a page. |
| 5. Authorization | Compare estimate or supplement dollars to portal screenshots or signed auth they saved. | `out/` auth-vs-estimate pack | Do not treat unapproved lines as sold. Teardown auth is separate if that is their rule. |
| 6. Supplement log | List estimate versions; keep first-write versus later dollars visible. | `out/` supplement list | Do not hide a supplement. Operator confirms which version is live. |
| 7. Parts order vs estimate | Join the parts PO sheet to estimate lines: part, qty, source, promised date, backorder. | `out/` parts-vs-estimate join | Do not invent ETAs. Do not pay vendors. |
| 8. Customer-pay vs insurer | Split lines by the pay type they coded: insurer, deductible as posted, customer-pay. | `out/` pay-type split | Keep CP separate. Deductible is not CP unless they coded it that way. |
| 9. Cycle time | List stage dates from their cycle calendar joined to open estimates. | `out/` cycle-time list | Never invent a delivery day. Never promise rental days. |

A Work Item is usually **one repair assignment / RO / claim pack**. Not every item walks every phase. Pick the registered workflow that matches the ask.

## Which registered workflows cover which phases

| Phase | Workflow id | Instruction file |
| --- | --- | --- |
| Assignment intake | `assignment-intake` | `.claude/workflows/assignment-intake.md` |
| Photo documentation | `photo-index` | `.claude/workflows/photo-index.md` |
| Write estimate from files | `estimate-from-files` | `.claude/workflows/estimate-from-files.md` |
| OEM procedures | `oem-procedure-present` | `.claude/workflows/oem-procedure-present.md` |
| Authorization | `authorization-missing` | `.claude/workflows/authorization-missing.md` |
| Supplement log | `supplement-log` | `.claude/workflows/supplement-log.md` |
| Parts order vs estimate | `parts-order-vs-estimate` | `.claude/workflows/parts-order-vs-estimate.md` |
| Customer-pay vs insurer | `customer-pay-vs-insurer` | `.claude/workflows/customer-pay-vs-insurer.md` |
| Cycle time | `cycle-time-list` | `.claude/workflows/cycle-time-list.md` |

Default when starting a new Work Item: `assignment-intake`.

## How to run a phase (no separate process-skill stack)

1. **workflow-selector** (or operator names the job) records the workflow on the Work Item journal.
2. **continue** walks **one ready YAML step** from that workflow file (or the whole named job if they asked).
3. Read the cited tool under `docs/tools/`. Write files under this Work Item’s `in/`, `work/`, `out/`, `evidence/`.
4. Run the step’s `check` against those same paths. On fail, retry at most 3, then ask. Do not invent a pass.
5. **journal-keeper** records artifacts, decisions, blockers, and the next ready step.
6. Missing shop knowledge → **operator-qa** (or ask in chat). Do not invent how *this* shop works.
7. Durable corrections → **remember** into operations memory or Work Item facts/rules.
8. Finished pack lives in the Work Item `out/` folder. Checks and exceptions go in `evidence/` and the journal.

## Human gates (continue is never approval)

- Missing assignment, VIN mismatch, missing procedure page, missing matrix/parts file
- Authorization required before treating work as sold
- Operator must confirm shop-specific practice (starter notes are guesses)
- Scope refusals in `MyRole.txt` (money, PAN, passwords, total-loss verdict, engineering/ADAS/structural stamps, invented hours/prices)

Record approvals in the active Work Item journal. The word **continue** does not clear a gate.
