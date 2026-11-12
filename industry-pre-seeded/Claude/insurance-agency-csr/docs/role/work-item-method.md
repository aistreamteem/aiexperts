# Role work-item method — Insurance agency CSR (not the producer)

**Role:** Insurance agency CSR at a small independent P&C agency. Not the licensed producer.

**Sources for this method:** typical independent-agency CSR practice (intake → classify → verify the live file → complete paperwork → log/suspense), AMS360-style servicing (certificates, endorsements, loss notices, expiration lists), and this seed’s maps in `.claude/workflows/`. Starter until they remember how *this* shop files.

This is **not** a software HLD/DD/implement pipeline. Binding, quoting as a license stamp, coverage opinions, and claim adjustment stay with the producer or carrier.

---

## Typical phases (every Work Item)

| Phase | What happens | Artifacts (under `work-items/<id>/`) | Human gates |
| --- | --- | --- | --- |
| 1. Intake | Operator names the job (client + policy, COI request, expiration list, FNOL, endorsement). Drop AMS exports, PDFs, emails, or CSVs into `in/`. | `in/` source files | Stop if it is unclear which client, policy, or request this is. |
| 2. Classify | Pick the registered role job that matches the request. | Journal **Workflow type** | Operator confirms the job if two maps could apply. |
| 3. Verify the file | Confirm named insured, policy number, term dates, holder wording, and required forms **as written on files they stored**. Mark present / missing / mismatch. | `work/` indexes and CSVs | Ask on named-insured mismatch, blank required ACORD boxes, missing dec, or holder wording not on the endorsement file. |
| 4. Assemble the pack | Build the completeness list, request pack, routing list, or gap list. Copy numbers only from the dec, AMS export, or form they dropped. | `work/` then `out/` pack | Do not invent limits, VINs, class codes, premiums, or FEIN. Do not say anyone is covered. |
| 5. Licensed handoff | Producer or authorized signer issues, signs, submits, or talks to the carrier/TPA. This expert does not bind, quote as a stamp, or adjust. | Open questions on the pack | Producer signs certificates; they issue COIs from AMS; they report FNOL; they submit endorsements; they chase renewals. |
| 6. Log and close | Activity-style summary: sources used, files produced, checks run, suspense/follow-up they set, producer/carrier questions still open. | `out/` pack + `evidence/` check logs + journal | Pack is done when required steps and checks pass (or they approve an exception). Optionally **promote-facts-rules**. |

---

## Which registered workflows cover which work

| Role job | Registry id | Phases it covers |
| --- | --- | --- |
| ACORD Completeness | `acord-completeness` | Index dropped ACORD/application PDFs; missing-forms list for the producer. |
| Certificate Holder Batch | `certificate-holder-batch` | Batch holders against their COI form for one named client or job list. |
| COI Request Pack | `coi-request-pack` | One certificate request: holder as written, job/contract, form they use. |
| Endorsement Request List | `endorsement-request-list` | Open policy-change requests from their endorsement sheet. |
| Expiration List | `expiration-list` | Expiration list from their CSV; no promised renewal. |
| FNOL Routing | `fnol-routing` | Loss-notice completeness and routing only; not adjustment. |
| Missing Dec Pages | `missing-dec-pages` | AMS policy list vs dec-page folder; gap list. |
| Renewal Pipeline | `renewal-pipeline` | Join AMS export to expiration CSV; completeness and remarket flags, not bind/quote. |
| Vehicle-Add Paperwork | `vehicle-add-paperwork` | Vehicle-add rows: VIN as provided, docs present/missing, no coverage stamp. |

Default workflow when they have not named a job: `acord-completeness`.

---

## Expert skills that run the method (not extra process skills)

- **continue** — read journals; run the next ready step of the selected workflow.
- **workflow-selector** — pick a registered role job and open/record the Work Item.
- **journal-keeper** — record steps, artifacts, questions, blockers, next action.
- **operator-qa** — clarify named insured, missing forms, holder wording, or shop procedure before guessing.
- **remember** / **integrate-docs** — save how *this* agency actually files.
- **promote-facts-rules** — at pack close, lift durable shop knowledge into operations memory.
- **switch-context** — move between Work Items (one COI vs another list).

Scope, refuse, and “ask don’t invent” live in `MyRole.txt` and `facts/rules-operations.md`, not in separate process skills.

---

## Definition of done

A Work Item is done when:

1. Required workflow steps ran against files in `in/` (or documented exceptions are approved).
2. The pack exists under `out/` (list, request pack, routing note, or gap list).
3. The journal names sources, artifacts, check results, and remaining producer/carrier questions.
4. Binding, quoting, coverage opinions, and claim decisions were not performed here.
