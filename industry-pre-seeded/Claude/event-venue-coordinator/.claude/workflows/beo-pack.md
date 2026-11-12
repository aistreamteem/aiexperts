# BEO Pack

**When to use:** Assemble BEO pages for definite functions and attach menu prices only as printed on their menu file. Name any function that has no BEO page. Draft versus issued stays labeled. Do not invent a guarantee, a minimum, or a bar license. Diagrams and AV lists attach if those files exist; missing stays missing. They issue the packet to the floor. You deliver the completeness pack and write-up.

**How to run:** workflow-selector if no Work Item is active → follow this file one ready step (or whole named job if requested) → write artifacts under `work-items/<id>/` → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: beo-pack
steps:
  - id: beos
    needs: []
    produces: beos
    produce_path: work/beos.csv
    tool: docs/tools/beo-pdf.md
    check: python docs/tools/checks/file-exists.py work/beos.csv
    on_fail: retry
    next: [menu]
  - id: menu
    needs: [beos]
    produces: menu
    produce_path: work/menu.csv
    tool: docs/tools/menu-file.md
    check: python docs/tools/checks/file-exists.py work/menu.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [beos, menu]
    produces: beo-pack
    produce_path: out/beo-pack.md
    tool: docs/tools/beo-pdf.md
    check: python docs/tools/checks/file-exists.py out/beo-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator teaches this shop (use remember).
