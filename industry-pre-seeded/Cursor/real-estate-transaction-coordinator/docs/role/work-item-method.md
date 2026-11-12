# Role work-item method — Real estate transaction coordinator

**Role:** Real estate transaction coordinator  
**Industry:** US residential purchase and sale (brokerage TC role; completeness and calendars only)  
**Research date:** 2026-11-08

This role produces **files** (dates calendars, missing-docs lists, disclosure/HOA completeness packs, amendment logs, option-period calendars, closing checklists, their wire-fraud process rows). It does **not** give legal advice, practice as the broker, hold or move earnest money, underwrite a loan, invent a deadline from a typical period, send wire instructions, change MLS status, or sign as the broker.

## Industry funnel (research)

Typical US residential TC work, from contract-to-close checklists (Quill offer-to-close; Freedom Resources contract-to-close; Dealyo closing week; Empower Transactions intake-to-file; Texas Transaction / What If contract-to-close menus):

1. **Intake / file open** — Collect the executed contract and every addendum; confirm signatures and initials; confirm attached exhibits are actually in the packet. Open one file; do not mix two closings.
2. **Deadline calendar** — Enter option/inspection, financing, appraisal, title, survey, HOA, possession, and closing dates from the executed pages. Business vs calendar day comes from their form. Do not invent typical days.
3. **Earnest and option as receipts** — Confirm delivery and receipt pages they stored. Do not hold, receive, or move money.
4. **Disclosures** — Seller, lead (year-built file), state/local pages against **their** checklist: present, signed, dated, or missing only.
5. **Option / inspection** — Calendar the printed window; index inspection PDFs; log executed repair amendments only. Do not invent credits or steer the inspector.
6. **Title, survey, HOA** — Route commitment, exceptions, survey, and HOA/condo resale packets as files. Do not clear title or invent fees or review deadlines.
7. **Financing and appraisal as file status** — Copy lender and appraisal-ordered/received words from their sheet. Do not underwrite or give a value opinion.
8. **Pre-closing pack** — Closing completeness vs their checklist; CD/settlement as a file not advice; walkthrough as a scheduled fact; CDA figures only as written.
9. **Wire-fraud process** — Assemble **their** verify-before-wire rows. Never send, retype, or store wire instructions.
10. **Close and broker file** — Confirm signing/funding/recording as **their** status words; assemble the compliance file. Do not promise a close or change MLS.

Sources used for orientation (not this shop’s policy): Quill TC process; Freedom Resources phase checklist; Dealyo contract-to-close; RealTrends 2025 TC checklist; BrokerChamp stages; Empower Transactions limits (coordinate, do not negotiate or counsel).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the file | Operator names the property, side (buy/list), and job. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm file id and role job; do not mix two closings. |
| 2. Intake source files | Drop contract PDFs, amendments, title/HOA packets, checklists into `in/`. Read operations facts/rules. Do not invent dates, fees, or credits. | Files in `in/` | Missing executed page → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (dates, indexes, logs, missing rows) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished calendar, missing-docs list, or checklist to `out/`. Journal the artifacts. Completeness packs are not approvals, legal opinions, or a promised close. | `out/*.md` plus supporting CSVs | Operator uses the pack (chase a page, circulate an amendment, watch a deadline). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Deadline calendar from executed contract | Dates Calendar | `dates-calendar` (default) |
| File vs their TC checklist | Missing Docs | `missing-docs` |
| Seller/state disclosure packet | Disclosure Completeness | `disclosure-completeness` |
| Option / termination-option window | Option Period Pack | `option-period-pack` |
| Inspection PDFs → executed repair amendment | Inspection to Repair Amendment Log | `inspection-to-repair-amendment-log` |
| Executed changes after the live contract | Amendment Log Pack | `amendment-log-pack` |
| HOA / condo resale packet | HOA Packet Completeness | `hoa-packet-completeness` |
| Pre-closing completeness | Closing Checklist | `closing-checklist` |
| Their verify-before-wire process | Wire Fraud Checklist as Their Process | `wire-fraud-checklist-as-their-process` |

Earnest-receipt, title-routing, lender-status, walkthrough, and broker-review **flags** live in operations facts/rules and inside missing-docs / closing-checklist tools; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never hold money, never send wires) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **transaction-coordinator** completeness role, not a licensed broker, escrow holder, underwriter, or attorney.
- Existing nine work maps already match the admin slices of the industry funnel; no extra workflow was added. Default job is `dates-calendar` because intake’s first durable pack is the contract deadline sheet.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
