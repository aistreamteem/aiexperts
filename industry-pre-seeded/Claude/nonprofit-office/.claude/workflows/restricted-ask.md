# Restricted Ask

**When to use:** From the gifts or bank-coding sheet and the bookkeeper’s fund or class export, list rows with no fund code, ambiguous restriction language (“for the kids”), grant leftovers, or board-designated labels that someone called restricted. Ask the bookkeeper. Do not spend them in a narrative, invoice, or liquidity note. Quote the gift words or award clause next to each question. If the restricted-fund sheet is missing, the whole pack is an ASK list, not a spend plan. Their codes win after they teach. You do not post a release or a reclass.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. Pull the restricted-fund sheet (docs/tools/restricted-fund-sheet.md) → `work/funds.csv`.
2. Pull gift/bank rows (docs/tools/spreadsheet.md) → `work/gifts.csv`.
3. List uncoded, ambiguous, leftover, or mislabeled rows for the bookkeeper → `out/restricted-ask.md`. Do not spend them in a narrative.

## Work map

```yaml
id: restricted-ask
steps:
  - id: pull
    needs: []
    produces: funds
    produce_path: work/funds.csv
    tool: docs/tools/restricted-fund-sheet.md
    check: python docs/tools/checks/file-exists.py work/funds.csv
    on_fail: retry
    next: [gifts]
  - id: gifts
    needs: [funds]
    produces: gifts
    produce_path: work/gifts.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/gifts.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [funds, gifts]
    produces: ask-pack
    produce_path: out/restricted-ask.md
    tool: docs/tools/restricted-fund-sheet.md
    check: python docs/tools/checks/file-exists.py out/restricted-ask.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when this shop corrects them.
