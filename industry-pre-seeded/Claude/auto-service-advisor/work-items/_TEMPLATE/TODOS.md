TODO List

Work Item: [WID-XXXXXXXX or YYYY-MM-DD-ro-#####]
Workflow: [one-ro | open-ros | mpi-pack | estimate-pack | auth-gap | additional-findings | parts-status | comeback | pickup-invoice]

## Intake
[ ] Operator named the RO / pack; folder `work-items/<id>/` exists
[ ] Source files in `in/` (RO export, MPI, parts, invoice as needed)

## Workflow steps
[ ] Follow `.claude/workflows/<workflow>.md` in order
[ ] Each `produces` file exists under this Work Item (`work/` then `out/`)
[ ] Each step check passed (or exception recorded)

## Human gates (as applicable)
[ ] Authorization on file before treating lines as sold
[ ] Additional findings have new auth (who, when, amount) or listed pending
[ ] Invoice matches last auth; extras flagged as questions

## Close
[ ] Pack in `out/`; check logs in `evidence/`
[ ] Journal next action and completion status updated

---

Status: [Not started | In progress (step X) | Complete]
