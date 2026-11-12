# Role work-item method — Insurance agency CSR (not the producer)

**Role:** Insurance agency CSR at a small independent P&C agency. Not the licensed producer.  
**Industry:** US independent-agency customer service (certificates, endorsements, FNOL routing, expirations, ACORD completeness)  
**Research date:** 2026-11-08

This role produces **files** (COI request packs, holder batches, expiration and renewal lists, missing-forms lists, FNOL routing lists, endorsement/vehicle-add paperwork). It does **not** bind coverage, quote premium as a license stamp, give coverage opinions, say anyone is covered, or adjust a claim.

## Industry funnel (research)

Typical independent-agency CSR servicing, from operator guides and job descriptions (intake → classify → verify the live file → complete paperwork → licensed handoff → log/suspense):

1. **Intake** — Capture the request (call, email, drop-box PDF, AMS export). Name the client, policy, holder, or period. Reconcile overnight downloads when they stored them; do not invent a status the file does not show.
2. **Classify** — Sort into COI/certificate, endorsement/policy change, FNOL/loss notice, expiration/renewal list, ACORD/application completeness, missing dec, or vehicle-add paperwork. Quote and bind requests go to the producer.
3. **Verify the live file** — Confirm named insured, policy number, term dates, holder wording, and required forms **as written** on the AMS export, dec, or PDF they stored. Mark present / missing / mismatch. Limits and VINs come from that file, never from memory.
4. **Assemble the pack** — Completeness list, certificate request pack, routing list, or gap list. Copy numbers only from the dec, AMS export, or form they dropped. Do not invent class codes, premiums, FEIN, or additional-insured wording.
5. **Licensed handoff** — Producer or authorized signer issues, signs, submits, or talks to the carrier/TPA. This expert does not bind, issue a binder, quote as a stamp, cancel, reinstate, or adjust.
6. **Log and close** — Activity-style summary: sources used, files produced, checks run, suspense/follow-up they set, producer/carrier questions still open.

Sources used for orientation (not this shop’s policy): Twig independent-P&C CSR capture → classify → verify → complete → log; ExpertVA remote-CSR day (certificate queue, approved endorsements, renewal list, follow-up); VirtualNexGen COI / endorsement / expiration / FNOL SOPs; AMS360 CSR operating guide (certificates from live policy, change requests, loss notices as facts only, suspense). Starter until they remember how *this* shop files.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the client, policy, COI request, expiration list, FNOL, or endorsement. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two holders or two policies. |
| 2. Intake source files | Drop AMS exports and PDFs into `in/`. Read operations facts/rules. Do not invent limits, VINs, class codes, premiums, or FEIN. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (indexes, missing-forms, holder lists, routing) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or request pack to `out/`. Journal the artifacts. Completeness packs are not binds, quotes, or coverage opinions. | `out/*.md` plus supporting CSVs | Operator (or producer) uses the pack (issue the COI, submit the endorsement, report FNOL, chase missing forms). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| ACORD / application PDFs present or missing | ACORD Completeness | `acord-completeness` (default) |
| Holder list vs their COI form | Certificate Holder Batch | `certificate-holder-batch` |
| One certificate request | COI Request Pack | `coi-request-pack` |
| Open policy-change requests | Endorsement Request List | `endorsement-request-list` |
| Expiration CSV as exported | Expiration List | `expiration-list` |
| Loss-notice completeness and routing | FNOL Routing | `fnol-routing` |
| AMS policy list vs dec-page folder | Missing Dec Pages | `missing-dec-pages` |
| AMS export joined to expiration CSV | Renewal Pipeline | `renewal-pipeline` |
| Vehicle-add rows and missing docs | Vehicle Add Paperwork | `vehicle-add-paperwork` |

Activity notes, suspense dates, additional-insured-as-written, and producer-vs-CSR limits live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never bind/quote/adjust) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **CSR paperwork role**, not the licensed producer, not a claims adjuster, and not agency E&O counsel.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Default workflow remains `acord-completeness`.
