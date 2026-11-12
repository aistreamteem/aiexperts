# Preauth Fields

**When to use:** Check that predetermination requests have the fields and attachments they require. No approval promise. No CDT choice. Copy a preauth number only from their payer letter or portal print; do not invent one. The dentist chooses what is proposed. Name attachment files or say missing; do not write the narrative or read films. A predetermination is not a scheduled visit and not a paid claim. Least PHI on the check sheet.

**How to run:** Open or reuse `work-items/<id>/`. Put the source export in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: preauth-fields
steps:
  - id: pull
    needs: []
    produces: preauth-raw
    produce_path: work/preauth.csv
    tool: docs/tools/claim-form-pdf.md
    check: python docs/tools/checks/file-exists.py work/preauth.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [preauth-raw]
    produces: preauth-writeup
    produce_path: out/preauth-check.md
    tool: docs/tools/claim-form-pdf.md
    check: python docs/tools/checks/file-exists.py out/preauth-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this office works.
