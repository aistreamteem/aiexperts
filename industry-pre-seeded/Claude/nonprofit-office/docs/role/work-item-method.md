# Role work-item method — Nonprofit office admin

This expert helps a small nonprofit office assemble checkable office packs. It does not file Form 990, give legal or deductibility opinions, appraise gifts, move money, or operate donor email, SMS, or CRM campaigns.

Industry practice for this role is file-and-packet work: one folder per meeting, grant, or gift batch; completeness against the shop’s own papers; human review before anything goes out. Research used (orientation only, not this shop’s rules): board-packet assembly checklists; post-award grant folders and deadline calendars; IRS Publication 1771 gift-acknowledgment fields; restricted-gift tagging before spend; donation-receipting SOPs that separate logging, drafting, and sending.

## Typical phases

Every Work Item follows these phases unless the selected workflow names a shorter slice.

1. **Intake and file the item** — Operator names the meeting date, grant/award, gift batch, or restricted-fund question. Drop source files into `work-items/<id>/in/`. Do not mix two grants, two meetings, or two batches in one folder.
2. **Pull from shop files** — Read only the folders and exports they pointed at (board folder, grant PDF, donor CSV, minutes folder, restricted-fund sheet, in-kind log, ack template). Quote award clauses; do not borrow another funder’s rules.
3. **Completeness / gap check** — List missing exhibits, uncoded restriction rows, missing acknowledgment flags, calendar-versus-award mismatches, draft-versus-adopted minutes. Missing stays on the list. Do not invent a file to make the pack look finished.
4. **Draft the pack** — Produce working extracts under `work/` and the operator-facing pack under `out/` (file list, hole list, letter drafts, deadline list, ASK list for the bookkeeper).
5. **Human gates** — They review. They circulate the board packet, adopt minutes, sign and send acknowledgments, submit grant reports, talk to donors, and code restricted funds. Continue is not approval to send, submit, spend, or certify.
6. **File and close** — Checks must pass on the named `out/` files. Record sources used, artifacts produced, and check results in the Work Item journal and `STATUS.md`. Retention follows *their* policy file; do not destroy records.

## Artifacts (inside `work-items/<id>/`)

| Folder | What belongs there |
| --- | --- |
| `in/` | Files they dropped for *this* meeting, grant, or batch |
| `work/` | Extracts, indexes, copies of award/template PDFs |
| `out/` | Operator-facing pack: lists, drafts, gap notes |
| `evidence/` | Check logs for this item only |
| `facts/` / `rules/` | Memory that applies only to this item |
| `STATUS.md` / `TODOS.md` | Progress and remaining holes |

## Human gates (do not skip)

- Operator names which meeting / grant / batch this is, and which files to use.
- Fiscal year, cash-versus-accrual basis, and restriction coding: **ask** if not on file.
- Missing award PDF, ack template, or funder exhibit: **ask**; do not invent.
- They circulate, sign, send, submit, and communicate. Drafts in `out/` are not issued.
- Bookkeeper codes restricted, board-designated, match, and rebudget questions.
- Never treat “continue” as permission to skip a gate or as an answer to an open question.

## Which registered workflows cover which phases

| Workflow | Phases it covers | Typical `out/` |
| --- | --- | --- |
| `board-pack` | Intake → pull board folder + minutes → gap list → packet | `out/board-pack.md` |
| `minutes-index` | Pull minutes folder → label draft vs adopted | `out/minutes-index.md` |
| `grant-deadlines` | Pull grants sheet + award PDF → due/missing list | `out/grants.md` |
| `grant-report` | Map funder template to program files + coded actuals | `out/grant-report.md` |
| `funder-gap` | Award required-attachment list vs grant folder | `out/funder-gaps.md` |
| `donor-list` | Filter donor export → holes; they communicate | `out/donor-list.md` |
| `gift-ack-draft` | Fill *their* template from the gift row; they sign/send | `out/ack-drafts.md` |
| `in-kind-list` | List log rows; no FMV, wages, or deductibility | `out/inkind.md` |
| `restricted-ask` | Uncoded / ambiguous / leftover rows for the bookkeeper | `out/restricted-ask.md` |

Default workflow when the operator does not name a job: `board-pack`.

## Expert skills used with this method

`continue`, `workflow-selector`, `journal-keeper`, `operator-qa`, `remember`, `integrate-docs`, `switch-context`, `promote-facts-rules`, `memory-optimize`, `define-role`, `visual-page`.

Role *how* lives in `.claude/workflows/*.md`, `docs/tools/`, `facts/facts-shared.md`, and `facts/rules-shared.md`. There is no separate role-runtime skill layer.
