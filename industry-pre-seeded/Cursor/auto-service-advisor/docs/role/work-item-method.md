# Role work-item method — Auto shop service advisor

Typical US independent and dealer service-counter practice. Starter until this shop teaches otherwise. This is not a software design-to-code pipeline.

Industry sources for the common sequence (check-in → concern → inspection → estimate → authorization → parts/labor → QC → invoice → pickup → follow-up): AutoShop POS repair-order workflow, dealer service write-up checklists, Tekmetric RO authorization flow, Garage360 check-in, ShopCommand estimate-to-payment, and Dealer1 RO write-up guidance.

## Typical phases

| Phase | What happens | Artifacts (under the Work Item) | Human gates |
| --- | --- | --- | --- |
| 1. Check-in / write-up | Capture customer, vehicle, mileage/VIN from their RO, and the concern in the customer's words | `in/` drop-offs; `work/ro-notes.md`; `out/` write-up pack | Operator must supply the RO/export; do not invent VIN, concern, or diagnosis |
| 2. Open board | List open tickets from their board export | Open-RO list | Missing board columns → ask |
| 3. Inspection copy | Copy MPI/DVI tags and photo captions from **their** form only | MPI pack | MPI is not a state inspection stamp and not authorization to repair |
| 4. Estimate | Build priced lines from **their** labor guide/menu plus confirmed parts | Estimate lines | Missing hours/prices stay questions; not sold work |
| 5. Authorization | Compare estimate lines to the auth log | Auth-gap list | **Customer (or fleet PO / warranty claim) must approve** before work beyond authorized diagnostics. Silence is not yes |
| 6. Additional findings | Tech/MPI recommendations beyond original scope | Findings list with their prices | **New auth** (who, when, amount, or digital approve) before marking sold |
| 7. Parts | On order / in stock / backorder / returned from vendor files | Parts CSV | Do not guess ETA or place the order |
| 8. Comeback overlay | Match today's concern to a prior RO in their history | Comeback flag | Do not invent that the last repair failed or decide warranty |
| 9. Pickup / invoice | Invoice vs last auth and tech notes | Pickup check pack | **Invoice must match last authorization**; extras are questions, not silent sold work |
| 10. Follow-up (optional) | List due callbacks from **their** follow-up/CSI export | Follow-up list | You do not send the messages |

Not every ticket needs every phase. A waiter oil change may be write-up → MPI → estimate → auth → pickup. A diagnostic comeback may be write-up + comeback flag → estimate → auth → additional findings.

## Registered workflows (which phase they cover)

Default job when starting a typical ticket: **one-ro**.

| Workflow | Covers |
| --- | --- |
| `one-ro` | Phase 1 — one ticket write-up (concern, parts file, estimate questions) |
| `open-ros` | Phase 2 — open tickets / WIP board |
| `mpi-pack` | Phase 3 — MPI/DVI copy from their form |
| `estimate-pack` | Phase 4 — priced lines from their labor source + confirmed parts |
| `auth-gap` | Phase 5 — pending vs authorized lines |
| `additional-findings` | Phase 6 — unauthorized tech/MPI recommendations |
| `parts-status` | Phase 7 — vendor/PO status |
| `comeback` | Phase 8 — prior-RO match overlay |
| `pickup-invoice` | Phase 9 — invoice vs last auth |

Follow-up stays a facts/rules concern unless this shop later registers a dedicated workflow.

## How a Work Item runs

1. Operator names the RO / pack. Create `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`.
2. **workflow-selector** records `Workflow type` from `.cursor/workflows/workflow-registry.json`.
3. Load `facts/facts-operations.md` and `facts/rules-operations.md`.
4. Follow the selected `.cursor/workflows/<id>.md` instruction file. YAML `work/` and `out/` paths mean **inside this Work Item**.
5. Read the tool doc named on the step (`docs/tools/`). Produce the file. Run the listed check. Pass the produced file to the next step — not a chat summary.
6. **journal-keeper** after each ready step. **continue** walks one ready step unless the operator asked for the whole named job.
7. Missing shop knowledge, auth, or files → ask (**operator-qa** when several choices). Do not invent diagnosis, book time, VIN, auth, or parts status.
8. Corrections → **remember** (fact or rule). Finished pack lives in `work-items/<id>/out/` with check logs in `evidence/`.

## Always-on constraints (from role)

- Never send money, store card numbers, certify inspection/street-legal, invent a diagnosis, overwrite the customer's concern, or treat unapproved work as sold.
- Cause and correction only from the technician file. NPF is a valid close.
- Declined lines stay visible.
