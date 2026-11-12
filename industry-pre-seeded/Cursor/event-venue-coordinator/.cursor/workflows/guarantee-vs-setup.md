# Guarantee versus setup

**When to use:** Compare the guarantee or labeled expected count on each BEO to chair and table counts on the dated diagram. Flag disagreements and any count above posted occupancy on their inventory or placard file if that number is in the BEO pack notes. Do not invent a guarantee. Do not stamp fire capacity. They revise the diagram or the count. You deliver the comparison pack.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put BEO PDFs and dated diagrams in `in/`. Read this file and `docs/tools/beo-pdf.md` / `docs/tools/diagram-pdf.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: guarantee-vs-setup
steps:
  - id: beos
    needs: []
    produces: beos
    produce_path: work/beos.csv
    tool: docs/tools/beo-pdf.md
    check: python docs/tools/checks/file-exists.py work/beos.csv
    on_fail: retry
    next: [diags]
  - id: diags
    needs: [beos]
    produces: diagrams
    produce_path: work/diagrams.csv
    tool: docs/tools/diagram-pdf.md
    check: python docs/tools/checks/file-exists.py work/diagrams.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [beos, diagrams]
    produces: setup-pack
    produce_path: out/guarantee-vs-setup.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/guarantee-vs-setup.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
