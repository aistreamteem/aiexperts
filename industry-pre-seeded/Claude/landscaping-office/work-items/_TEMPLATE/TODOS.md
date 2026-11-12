# Work Item steps

Work Item: [id]
Workflow: [registry id — e.g. crew-day]
Method: see `docs/role/work-item-method.md` and `.claude/workflows/<id>.md`

## Intake / files in

- [ ] Operator dropped route, roster, tickets, price file, or photos into `in/`
- [ ] Missing ticket / access / dog flag questions listed

## Workflow steps

Copy the step ids from the selected workflow file (needs → produces → check). Example for crew-day:

- [ ] roster → `work/crew-roster.csv`
- [ ] tickets → `work/tickets.csv`
- [ ] pack → `out/crew-day.md`

## Human gates

- [ ] Missing prices, dump fees, hours, or wages asked (not invented)
- [ ] Weather postpone only if they called it
- [ ] Extra work auth / commercial PO present or listed as missing
- [ ] Estimate draft labeled draft until they accept

## Closeout

- [ ] Checks ran against this Work Item’s `work/` and `out/`
- [ ] Journal / STATUS names sources, artifacts, checks
- [ ] Offer promote-facts-rules if this job taught durable shop practice

---

Status: [Not started | In progress | Complete]
