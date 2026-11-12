# Funder Gap

**When to use:** From the award PDF’s required-attachment list or the funder template exhibit, mark each file present or missing in the grant folder. Missing means ask, not omit so the pack looks finished. Do not substitute a file from another award. If the template and the agreement disagree, quote both. Portal-only items need an export in the folder before you mark them present. They submit. You produce the gap list. Closeout attachments follow the same rule when the PDF names them. Completeness is the job; a pretty incomplete pack is a failure.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. Copy/quote the award letter (docs/tools/award-letter-pdf.md) → `work/award.pdf`.
2. List files present in the grant folder (docs/tools/grant-pdf.md) → `work/grant-files.csv`.
3. Mark required attachments present or missing → `out/funder-gaps.md`. They submit.

## Work map

```yaml
id: funder-gap
steps:
  - id: award
    needs: []
    produces: award
    produce_path: work/award.pdf
    tool: docs/tools/award-letter-pdf.md
    check: python docs/tools/checks/file-exists.py work/award.pdf
    on_fail: retry
    next: [files]
  - id: files
    needs: [award]
    produces: files
    produce_path: work/grant-files.csv
    tool: docs/tools/grant-pdf.md
    check: python docs/tools/checks/file-exists.py work/grant-files.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [award, files]
    produces: gap-out
    produce_path: out/funder-gaps.md
    tool: docs/tools/grant-pdf.md
    check: python docs/tools/checks/file-exists.py out/funder-gaps.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when this shop corrects them.
