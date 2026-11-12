# Failed-draft list

**When to use:** List failed drafts from the membership or billing export they dropped: amount as printed, fail date, and reason code if present. Do not invent NSF versus expired card. Do not retry the draft and do not store PAN. They contact the member. Produce the list plus a pack note. Access after a fail stays their flag, not a hold you invent. Starter until they teach this club’s fail and retry codes.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Follow this file's YAML via **continue**. Read the cited `docs/tools/` doc, write artifacts under the Work Item, run the step `check`, store logs in `evidence/`, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: failed-draft-list
steps:
  - id: members
    needs: []
    produces: members
    produce_path: work/membership.csv
    tool: docs/tools/membership-export.md
    check: python docs/tools/checks/csv-has-columns.py work/membership.csv member_id status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [members]
    produces: draft-pack
    produce_path: out/failed-drafts.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/failed-drafts.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
