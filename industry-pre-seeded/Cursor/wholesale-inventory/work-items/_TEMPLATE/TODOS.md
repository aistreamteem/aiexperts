TODO List

Work Item: [WID-XXXXXXXX]
Workflow: [receiving-match | putaway-list | pick-pack | transfer | cycle-count | abc-class | dead-stock | lot-expiry | reorder | rma-returns]

## Intake
- [ ] Source files in `in/` (stock CSV, count sheet, PO PDF, packing slip named by the selected job)

## Work-map steps
- [ ] Walk each YAML step in `.cursor/workflows/<workflow>.md` (needs → produces → check)

## Pack
- [ ] Finished list or match sheet in `out/`
- [ ] Check logs in `evidence/`

## Close
- [ ] Journal updated; operator has the pack
- [ ] Optional: remember / promote shop corrections

---

Status: [Not started | In progress (step) | Complete]
