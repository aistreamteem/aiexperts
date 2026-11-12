# Role work-item method — Mortgage processor (file completeness)

This expert runs **loan-file completeness** for a small US broker or correspondent processor role. It does not underwrite, approve or deny, lock a rate, calculate DTI/LTV/income, give TRID or fair-lending legal opinions, certify value, or send wires.

Industry processor work (NAMP, MGIC processing fundamentals, OriginPoint loan steps, typical LOS checklists) moves a file from **intake → document collection → third-party orders → conditions → clear-to-close support**. This role only does the **present / missing / dated** slice of that cycle. Clear-to-close and lock status stay **their flags**.

## Typical Work Item phases

1. **Open the loan file.** Isolate one loan under `work-items/<id>/`. Drop the LOS export, conditions sheet, and PDFs they stored into `in/`.
2. **Index what is on file.** Build or refresh a document-folder index (application, ID minimum-necessary, income/assets, VOE, contract, and whatever else they imaged).
3. **Select the role job.** Use `workflow-selector` if the journal has no workflow type. Default: **conditions-checklist**.
4. **Load shop memory.** Read `facts/MEMORY-INDEX.md`, then `facts/facts-shared.md` and `facts/rules-shared.md`, plus this Work Item’s facts/rules.
5. **Run the registered workflow steps.** Follow the YAML in `.claude/workflows/<id>.md`. Read the listed `docs/tools/` file. Write `work/` then `out/`. Run each step’s check from the Work Item root.
6. **Human gates.** Ask before inventing a missing conditions sheet, shop code, or date. Label starter names as guesses. Never declare CTC from a green checklist. Operator confirms guessed labels and whether to chase a named missing item.
7. **Pack and journal.** Finished lists live in `out/`. Check logs live in `evidence/`. `journal-keeper` records the step, artifacts, blockers, and next action.

## Artifacts (per Work Item)

| Phase | Typical artifacts |
| --- | --- |
| Intake / index | `work/document-index.csv`, `out/loan-file-index.md` |
| Conditions | `work/conditions.csv`, `out/conditions-checklist.md` |
| Missing docs | `out/missing-docs.md` |
| Dates | `work/processor-calendar.csv`, `out/date-stamps.md` |
| Third-party files | `out/appraisal-in-file.md`, `out/title-routing.md`, `out/insurance-binder-present.md` |
| Disclosures | `work/le-cd-index.csv`, `out/cd-le-present.md` |
| Suspense | `out/suspense-list.md` |
| Wire-fraud process | `out/wire-fraud-checklist.md` (their rows only; do not send a wire) |

## Human gates

- Missing conditions sheet or LOS export when a checklist is requested → ask (`operator-qa`); do not invent UW items.
- Two files disagree on a date or rate → quote both; do not pick.
- Guessed document type or LOS code → label the guess; do not present it as this shop’s rule.
- CTC / lock / docs-out / approved → copy their flag or say it is not on file.
- “Continue” is not approval of a gate and not an answer to a blocking question.

## Which registered workflows cover which phases

| Industry phase (completeness slice) | Registered workflow |
| --- | --- |
| File intake / what is imaged | `loan-file-index` |
| Conditions / PTD / PTF | `conditions-checklist` |
| Chase incomplete file | `missing-docs` |
| Critical dates (application, VOE, LE/CD, lock, close as stored) | `date-stamps` |
| Appraisal PDF present (not a value) | `appraisal-in-file-not-value` |
| Title commitment routing (not an opinion) | `title-routing` |
| HOI / flood binder present | `insurance-binder-present` |
| LE / CD versions present | `cd-le-present` |
| Suspense / rereq as their codes | `suspense-list-as-their-codes` |
| Their wire-fraud / callback checklist rows | `wire-fraud-checklist-their-process` |

Canonical expert skills that drive the loop: `continue`, `workflow-selector`, `journal-keeper`, `operator-qa`, `remember`, `integrate-docs`, `switch-context`. Role *how* lives in the workflow files and `docs/tools/`, not in a second process-skill layer.

## What this method does not include

Software design-and-build pipelines, income calculation, credit decisioning, rate lock, TRID legal timing opinions, sending or republishing wire instructions.
