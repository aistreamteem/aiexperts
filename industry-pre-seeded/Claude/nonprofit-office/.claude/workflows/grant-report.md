# Grant Report

**When to use:** Map the funder template questions to program files and the grant financial export they coded to that award. Flag missing attachments, missing census months, and template-versus-agreement mismatches. Fill narrative only from cited files. Do not invent outcomes or headcount. They submit. You do not click the portal. Budget-versus-actual variances stay questions, not silent rebudgets. Period and fund code come from the award PDF. Output is the template in work/, the program extract, and a report map that shows what is present and what still needs staff.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. Place the funder template (docs/tools/grant-pdf.md) → `work/funder-template.pdf`.
2. Extract program files (docs/tools/program-report-folder.md) → `work/program.csv`.
3. Map questions to cited files; flag holes → `out/grant-report.md`. Do not invent outcomes. They submit.

## Work map

```yaml
id: grant-report
steps:
  - id: tmpl
    needs: []
    produces: template
    produce_path: work/funder-template.pdf
    tool: docs/tools/grant-pdf.md
    check: python docs/tools/checks/file-exists.py work/funder-template.pdf
    on_fail: retry
    next: [program]
  - id: program
    needs: [template]
    produces: program
    produce_path: work/program.csv
    tool: docs/tools/program-report-folder.md
    check: python docs/tools/checks/file-exists.py work/program.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [template, program]
    produces: report-out
    produce_path: out/grant-report.md
    tool: docs/tools/grant-pdf.md
    check: python docs/tools/checks/file-exists.py out/grant-report.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when this shop corrects them.
