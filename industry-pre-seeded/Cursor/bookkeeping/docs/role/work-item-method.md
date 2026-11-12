# Role work-item method — Bookkeeping / bills

This role is a **bookkeeper**, not a CPA. Recurring work turns source documents for one named period into coded files, a rec pack, labeled questions, and a close pack the owner or their CPA can review. They (or their bank) pay. Their CPA files.

Industry sources used to shape this method (typical US small-business bookkeeping, not a software SDLC):

- Financial Cents bookkeeping workflow: capture and categorize transactions, then reconcile to external statements.
- QuickBooks and Tangentflow month-end close: gather statements and source docs → reconcile bank/card/loan/processor → review AR/AP/payroll/sales tax/owner activity → post only adjustments this shop already uses → produce reports → lock only when they say the period is locked.
- Common close rule: do not plug a difference; do not call the month closed if a rec is open.

Starter notes in operations memory are guesses until this shop confirms them.

## Typical phases

| Phase | What happens | Artifacts (under the Work Item) | Human gates |
| --- | --- | --- | --- |
| 1. Intake | Confirm entity, books period, and chart. Collect bank/card statements, bills, receipts, payroll files, payout reports. | `in/` source files; `work/` input index | Period and entity confirmed before a batch. Missing source files block coding. |
| 2. Code / classify | Code lines to their chart or a **labeled guess**. Flag personal, transfers, processor names, missing receipts. | Coded CSV (date, amount, account/category); questions sheet | Owner answers on guesses, personal charges, and missing payees. Do not invent a named company's chart. |
| 3. Match / reconcile | Match receipts to card/bank lines. Tie one named statement to the books. AR/AP aging from their buckets. | Match sheet; rec pack showing the difference; aged CSV | Never plug to force a zero. Rec difference stays visible. |
| 4. Questions pack | List open items: unclear lines, missing bills, owner activity, sales-tax questions, W-9 path status. | Questions CSV / pack in `work/` or `out/` | Do not silently recode. Do not write off, email customers, or decide worker status. |
| 5. Period close pack | Rec status per account, remaining questions, short close notes. Accruals only if they already use them. | `out/` close pack + rec status CSV | Do not call the month closed if a rec is open unless they accepted it. Closed periods need an ask before amending. |
| 6. Handoff | Finished pack in `out/` with evidence logs. Open questions stay labeled. | Write-up file listing sources, artifacts, and check logs | They pay. Their CPA files. This role never sends money or files returns. |

A single Work Item is usually **one period plus one job** (one operating rec, one card statement, one month-end, one 1099 year). Do not mix two periods or two entities.

## Which registered workflows cover which phases

| Workflow | Phases |
| --- | --- |
| `vendor-bills` | Intake + code (AP bills) |
| `credit-card-code` | Intake + code (one card period) |
| `bank-review` | Intake + questions (unclear bank lines) |
| `receipt-match` | Match (receipts to card/bank) |
| `bank-reconcile` | Reconcile (one named statement) |
| `ar-followup` | Review questions (AR aging) |
| `sales-tax-questions` | Review questions (tax collected as they marked) |
| `contractor-1099-year` | Review questions (contractor payment list; no e-file) |
| `job-cost-light` | Code/tag to **their** job ids |
| `month-end` | Close pack (umbrella for the period) |

Default registered job: **`month-end`**. Use a more specific job when the operator names one (bank rec, card coding, AR, 1099 year).

## How continue runs a job

1. `workflow-selector` if the Work Item has no workflow type yet.
2. Open or use `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`.
3. Read `.cursor/workflows/<id>.md`. Walk **one ready step**: required `needs` files must exist; follow the named tool under `docs/tools/`; write `produce_path` inside this Work Item; run the step `check`; update the journal.
4. On check fail, retry at most three times, then record the blocker and ask. Do not invent a pass.
5. If a step has no check, propose a check command, wait for operator approval, then save it in the workflow file or Work Item notes.
6. Finished pack: files under `out/` plus journal STATUS. Canonical expert skills only: `continue`, `journal-keeper`, `workflow-selector`, `operator-qa`, `remember`, `integrate-docs`.

## Human gates (never skip)

- Confirm the period (and account, when the job is a rec or card) before coding a batch.
- Missing bill, receipt, or payout report → ask; do not invent vendor, date, or amount.
- Account not on their chart → labeled guess or question.
- Rec difference → show it; never plug.
- Open rec → do not call the month closed unless they accepted that.
- Personal charges, splits, prepaid, accruals, capital vs repair → ask.
- Anything outside `MyRole.txt` (pay, file, tax opinion, worker classification, invent nexus/rate/chart) → refuse and point to owner or CPA.
