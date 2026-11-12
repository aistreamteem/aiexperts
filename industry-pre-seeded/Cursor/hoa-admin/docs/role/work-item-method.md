# Role work-item method — HOA / association admin

This expert files one association job as one Work Item. It does **not** use a software HLD → DD → implement pipeline. It does **not** send money, stamp architectural decisions, certify elections, or act as counsel.

**Research date:** 2026-11-08. Industry sources for the phase shape: Community Associations Institute manager-duty lists (inspect/log, ACC completeness for board/committee action, board-packet prep, vendor contract files, assessment collections liaison); typical CAM loops for violation intake → notice-step tracking, architectural request completeness before committee routing, vendor COI presence before dispatch, dues aging from the ledger, and reserve-study liaison. A community association manager intakes a file, checks it against the board-adopted form or policy, produces a pack the board or committee can act on, and stops at human gates the manager does not own.

Starter notes in operations memory are typical US practice until the operator says how *this* association files.

## Typical phases (every Work Item)

1. **Identify the job and the association** — Name the community, the lot or meeting or project, and the registered workflow. One association per pack unless the operator asked for a labeled portfolio.
2. **Intake source files** — Put their export, PDF, form, roster, or photo set in the Work Item `in/` folder. Confirm the association name on the header before listing rows.
3. **Completeness / field check** — Against *their* form, adopted notice steps, ledger columns, certificate checklist, or meeting-file list. Missing pages, blank lots, unsigned fields, expired dates, and broken photo links are questions, not findings you invent.
4. **Produce the pack** — CSV the checks can see under `work/`, then the write-up under `out/`. Copy check logs to `evidence/`.
5. **Human gate** — Board, committee, treasurer, or counsel owns approve/deny, award, certification, demand letters, liens, and fund movement. The expert does not pass those gates.
6. **File and close** — Journal the artifacts, blockers, and next action. Promote durable shop knowledge only when the operator selects it.

`continue` walks **one ready step** inside the selected workflow unless the operator asked for the whole named job. The word continue is not approval of a gate and is not an answer to an open question.

## Artifacts

| Phase | Where | Typical files |
| --- | --- | --- |
| Intake | `work-items/<id>/in/` | Ledger export, ACC form, bid PDFs, COIs, roster, photos, reserve-study PDF, meeting folder |
| Working lists | `work-items/<id>/work/` | CSVs named by the workflow (`violations.csv`, `dues-aging.csv`, …) |
| Finished pack | `work-items/<id>/out/` | Write-up markdown the operator can skim |
| Checks | `work-items/<id>/evidence/` | `file-exists.py` / `csv-has-columns.py` logs |
| Memory | `facts/facts-operations.md`, `facts/rules-operations.md`, optional WI `facts/` | Shop facts and must-never rules |
| Journal | `journals/work-items/<id>/` | Progress, decisions, blockers, next action |

## Human gates (do not infer from “continue”)

- Confirm community name and as-of date before dues aging.
- Confirm which meeting date, which ACC application, which bid project, or which vendor file when more than one is in `in/`.
- Architectural approve / deny / defer — committee or board only (`acc-completeness` is completeness, not a stamp).
- Pick a winning bid or award a contract — board only.
- Certify an election or rule on proxy validity — named human inspector / board only.
- Demand letters, liens, foreclosure, eviction, fair-housing opinions, engineering stamps, coverage opinions, paying vendors, moving operating/reserve funds — out of scope; ask or refuse with `MyRole.txt`.
- Missing required exhibits, photos, or clauses — **operator-qa** (or a blocking journal question), do not invent.

## Registered workflows (what covers which phase)

| Workflow | Registry id | Phases it covers | Typical pack |
| --- | --- | --- | --- |
| ACC Completeness | `acc-completeness` | Intake + completeness of an architectural application | Missing-pages CSV + `out/acc-check.md` |
| Violations | `violations` | Intake + notice-step status from their log | Open-item CSV + `out/violations.md` |
| Dues Aging | `dues-aging` | Intake + aging buckets from their ledger | Aging CSV + `out/dues-aging.md` |
| Board Files | `board-files` | Meeting-packet present/missing list | File index CSV + `out/board-files.md` |
| Election Tally | `election-tally` | Count from roster and ballot/proxy files | Tally CSV labeled as a tally, not a certification |
| Bid Compare | `bid-compare` | Compare numbers from bid PDFs for one project | Comparison CSV + `out/bid-compare.md` |
| Vendor Certs | `vendor-certs` | Certificate presence: dates, named insured, additional insured as printed | COI index + `out/vendor-certs.md` |
| Work Orders | `work-orders` | Common-area job list from their export | WO CSV + `out/work-orders.md` |
| Reserve Index | `reserve-index` | Reserve-study PDF presence and printed cover numbers | Index CSV + `out/reserve-index.md` |

Default registry workflow: `acc-completeness`. Related CAM work that is common in the industry (hearing calendars, payment-plan logs, records requests, amenity reservations, parking/tow logs, vendor W-9 presence) uses the closest registered job plus operations facts/rules. Add a new registered workflow only when the operator names a repeating shop job.

## How to run a job (no deleted process skills)

1. **workflow-selector** (or an already-selected Workflow type on the Work Item journal).
2. Copy `work-items/_TEMPLATE/` to `work-items/<id>/` if the folder does not exist. Put operator files in `in/`.
3. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`, plus this Work Item’s `facts/` when present.
4. Walk the YAML steps in `.cursor/workflows/<id>.md`: read the cited `docs/tools/` file, write `produce_path` under the Work Item, run the listed check, store logs in `evidence/`.
5. **journal-keeper** after each ready step, operator answer, blocker, or close.
6. Missing shop knowledge → ask (blocking question or **operator-qa**). Durable corrections → **remember**. End-of-pack promotion → **promote-facts-rules**.

Do not look for a leftover top-level job pile or a parallel role-skill loop. Work Item folders plus the registered workflow file *are* the map.

## Assumptions

- This is a small association or management-company role, not counsel, not an engineer, not a collections agency, not the architectural committee.
- Checks are presence/column checks on files the operator provided, not a legal finding that a lot is in violation or that a meeting was valid.
- Starter handbook language is labeled until they teach this community.
