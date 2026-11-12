# Role work-item method — Janitorial / contract-cleaning office

This expert is a **US contract-cleaning / building-service office role**, not a floor crew and not a safety inspector. Work Items are site-nights, callback packs, supply weeks, key closeouts, or other named packs. Industry practice (ISSA CIMS, commercial cleaning ops SOPs) plus this seed’s maps shape the method below.

## Typical phases

1. **Intake source files** — Operator drops the site list, schedule CSV, crew roster, par sheet, SDS index, quality form, complaint log, key log, holiday calendar, and/or contract PDFs into the Work Item `in/` folder (or points at files already in this expert).
2. **Match the role job** — Pick a registered workflow. Do not invent a free-form process when a named job fits.
3. **Build working extracts** — Copy only named columns from their files into `work/` CSVs. Do not invent hours, wages, mixes, square footage, scores, or missing sites.
4. **Assemble the pack** — Write the list or pack in `out/` the checks can see. Attach photos or PDFs only if they already stored them.
5. **Human gates** — Missing scope, missing SDS rows, missing keys, missing extra-work auth, and company-vs-customer calendar conflicts stay questions. Operator answers or supplies the file before the pack treats those rows as closed.
6. **Close** — Checks pass or exceptions are recorded. STATUS names source files, artifacts, and check logs. Optional: promote Work Item facts/rules.

## Artifacts (inside `work-items/<id>/`)

| Folder | What goes here |
| --- | --- |
| `in/` | Files the operator dropped for this site-night, week, or pack |
| `work/` | Extracts (site list, schedule, roster, par, SDS index, complaint log, key log) |
| `out/` | Finished pack: night board, callback list, below-par flags, quality pack, etc. |
| `evidence/` | Check command logs for this pack only |
| `STATUS.md` | What finished, what’s next, what the operator still owes |

Typical pack names until this shop teaches otherwise: site + service date (`2026-09-15-clinic-night`). Supply orders may be a week folder.

## Human gates

- Do not invent scope, frequency, square footage, chemical mix, wage, inspection score, or a holiday skip.
- Do not stamp OSHA, Hazard Communication, bloodborne, or hospital protocol.
- Do not store alarm codes, keypad PINs, lock combinations, passwords, or pay a crew.
- Missing contract-scope file, missing SDS row, missing key return, or missing extra-work auth → ask; do not fill the hole.
- “Continue” is not approval of an open question.

## Registered workflows ↔ phases

| Workflow | Covers |
| --- | --- |
| `night-board` | Daily/nightly site–shift–crew list from site list, schedule, roster; holiday skips only from their calendar |
| `quality-checklist-pack` | Inspection pack from their form + stored photos (no invented score) |
| `complaint-callback` | Open complaints from their log + named photos |
| `missed-service-list` | Schedule rows coded missed + complaint rows that point at a miss |
| `supply-below-par` | On-hand vs their par/min; reorder flags only |
| `sds-index-missing` | Par-sheet chemicals with no SDS index row or missing file |
| `extra-work-auth-list` | Add-on / extra-day / project rows vs auth PDFs |
| `holiday-coverage` | Their holiday calendar vs schedule and roster |
| `key-log-completeness` | Issued key-ids vs sites; out-without-in flags (never copy keys) |

Default registry job until the operator picks another: `complaint-callback`. Recurring nightly work usually belongs on `night-board`.

## How to run a job (no separate process-skill layer)

1. **continue** (or **workflow-selector** on a new Work Item) loads `journals/expert/progress.md` and the active Work Item under `work-items/<id>/`.
2. Follow the selected file in `.claude/workflows/`. Each step: read the tool doc under `docs/tools/`, produce the named file under the Work Item, run the listed check, retry at most three times, then ask.
3. **journal-keeper** after each step. Missing shop knowledge → **operator-qa** or a blocking question in the journal. Corrections → **remember**. Outside `MyRole.txt` → refuse in place (scope lives in MyRole and `facts/rules-operations.md`).
4. Finished pack lives in that Work Item’s `out/` plus STATUS. Do not pile Tuesday into Monday’s folder.

Canonical expert skills only: `continue`, `define-role`, `journal-keeper`, `remember`, `workflow-selector`, `operator-qa`, `promote-facts-rules`, `switch-context`, `integrate-docs`, `memory-optimize`, `visual-page`.
