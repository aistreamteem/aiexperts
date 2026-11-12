# Missing Waivers

**When to use:** Compare the membership export to the waiver folder. List members and guests whose required form is absent. PAR-Q is present-or-missing only — do not score answers. Minors need the guardian form their packet names. Do not invent a signature. Produce the missing-forms CSV plus a pack note in `out/`. They chase signatures. Do not score a PAR-Q or copy medical answers into docs/. Starter until the operator corrects this club’s current form versions.

**How to run:** Open or reuse `work-items/<id>/` (workflow-selector if unset) → continue one ready YAML step (or the whole named job if requested) → journal-keeper. Paths `work/` and `out/` are inside that Work Item.

**Initial phase:** `intake`

## Work map

```yaml
id: missing-waivers
steps:
  - id: members
    needs: []
    produces: members
    produce_path: work/membership.csv
    tool: docs/tools/membership-export.md
    check: python docs/tools/checks/csv-has-columns.py work/membership.csv member_id status
    on_fail: retry
    next: [waivers]
  - id: waivers
    needs: [members]
    produces: waivers
    produce_path: work/waiver-index.csv
    tool: docs/tools/waiver-folder.md
    check: python docs/tools/checks/file-exists.py work/waiver-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [members, waivers]
    produces: waiver-pack
    produce_path: out/missing-waivers.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/missing-waivers.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this club.
