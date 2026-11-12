# Pack checklist

Work Item: [WID-XXXXXXXX or YYYY-MM-DD-site]
Workflow: [night-board | complaint-callback | quality-checklist-pack | missed-service-list | supply-below-par | sds-index-missing | extra-work-auth-list | holiday-coverage | key-log-completeness]

Copy steps from the selected file in `.claude/workflows/`. Check them off as each named check passes.

## Intake
- [ ] Source files in `in/` (site list, schedule, roster, par, SDS, quality form, logs, contracts — as the job needs)
- [ ] Missing files listed as questions, not invented

## Working extracts (`work/`)
- [ ] Step 1 extract produced and check passed
- [ ] Later extracts produced and checks passed

## Pack (`out/`)
- [ ] Finished list/pack exists
- [ ] Check command exited 0 (or exception recorded)
- [ ] STATUS names sources, artifacts, and check logs

## Human gates
- [ ] Missing scope / SDS / keys / extra-work auth asked
- [ ] Operator answers recorded in the journal

Status: [Not started | In progress | Complete]
