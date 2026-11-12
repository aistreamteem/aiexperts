# Funder file-gap list

**When to use:** From the award PDF’s required-attachment list or the funder template exhibit, mark each file present or missing in the grant folder. Missing means ask, not omit so the pack looks finished. Do not substitute a file from another award. If the template and the agreement disagree, quote both. Portal-only items need an export in the folder before you mark them present. They submit. You produce the gap list. Closeout attachments follow the same rule when the PDF names them. Completeness is the job; a pretty incomplete pack is a failure.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

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

Starter work map. Replace tools and checks when they correct how this shop works (**remember**).
