# Guarantee vs Setup

**When to use:** Compare the guarantee or labeled expected count on each BEO to chair and table counts on the dated diagram. Flag disagreements and any count above posted occupancy on their inventory or placard file if that number is in the BEO pack notes. Do not invent a guarantee. Do not stamp fire capacity. They revise the diagram or the count. You deliver the comparison list plus write-up.

**How to run:** workflow-selector if no Work Item is active → follow this file one ready step (or whole named job if requested) → write artifacts under `work-items/<id>/` → journal-keeper

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

Starter work map. Replace tools and checks when the operator teaches this shop (use remember).
