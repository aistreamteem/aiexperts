TODO List

Work Item: [WID-XXXXXXXX or dated-slug]
Workflow: [describe-csv | group-compare-bars | histogram-pack | missing-and-outliers | refresh-from-new-export | scatter-and-corr | small-multiples | time-series-line]
Question: [one sentence]

## Question
- [ ] Named question, audience, measure, columns, date range, filters

## Intake
- [ ] Source file in `in/`; source name and version recorded
- [ ] Missing package? install ask — do not fake a chart

## Profile
- [ ] Types, n, missing, date range, units; parse failures listed
- [ ] Header / date format / separator guesses labeled and asked

## Prepare
- [ ] Filter / join / aggregate only as named
- [ ] Plotted-values CSV in `work/`

## Chart
- [ ] PNG/PDF in `out/` with units, honest scale, colorblind palette
- [ ] No extra PII on the picture

## Pack
- [ ] Write-up in `out/`: question, source, columns, filters, n, what was not claimed
- [ ] Checks in `evidence/` exit 0 (or documented exception)

## Review
- [ ] Operator read the pack
- [ ] Corrections stored with remember if durable

---

Status: [Not started | In progress (phase) | Complete]
