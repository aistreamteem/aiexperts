# Minutes Index

**When to use:** Index meeting dates and draft versus adopted from their minutes folder. Do not edit adopted minutes in place. Do not promote a draft to adopted. Do not invent attendance or votes. Committee files stay labeled committee. Least PII in the index. Missing adopted minutes for a calendar date are holes. Output is the index CSV and a pack note the next board pack can use. They adopt minutes. You label and list. A corrections process, if they have one, comes from their policy file—not from a silent overwrite.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. Index the minutes folder (docs/tools/minutes-folder.md) → `work/minutes-index.csv`.
2. Pack draft versus adopted labels and holes → `out/minutes-index.md`. They adopt minutes. You label.

## Work map

```yaml
id: minutes-index
steps:
  - id: list
    needs: []
    produces: minutes
    produce_path: work/minutes-index.csv
    tool: docs/tools/minutes-folder.md
    check: python docs/tools/checks/file-exists.py work/minutes-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [minutes]
    produces: min-out
    produce_path: out/minutes-index.md
    tool: docs/tools/minutes-folder.md
    check: python docs/tools/checks/file-exists.py out/minutes-index.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when this shop corrects them.
