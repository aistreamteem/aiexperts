# Gift Ack Draft

**When to use:** Draft letters from their approved template and the gift file. Fill blanks only. They send and they sign. Do not mark the CSV sent. Do not invent a deductibility sentence, a tax paragraph, or a plate-cost net. Use the matching template for DAF, stock, or event if they named one. Quid pro quo estimates come from their event file. A draft in out/ is not an issued acknowledgment. If no template is present, ask; do not write Publication 1771 wording from memory as if it were letterhead.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. Pull gift rows (docs/tools/spreadsheet.md) → `work/gifts.csv`.
2. Load *their* ack template (docs/tools/ack-template.md) → `work/ack-template.md`. If none, ask.
3. Fill blanks only → `out/ack-drafts.md`. They sign and send. Do not mark the CSV sent.

## Work map

```yaml
id: gift-ack-draft
steps:
  - id: gifts
    needs: []
    produces: gifts
    produce_path: work/gifts.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/gifts.csv
    on_fail: retry
    next: [tmpl]
  - id: tmpl
    needs: [gifts]
    produces: template
    produce_path: work/ack-template.md
    tool: docs/tools/ack-template.md
    check: python docs/tools/checks/file-exists.py work/ack-template.md
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [gifts, template]
    produces: ack-out
    produce_path: out/ack-drafts.md
    tool: docs/tools/ack-template.md
    check: python docs/tools/checks/file-exists.py out/ack-drafts.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when this shop corrects them.
