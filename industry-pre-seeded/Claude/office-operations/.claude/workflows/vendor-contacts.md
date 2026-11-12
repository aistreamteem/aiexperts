# Vendor Contacts

**When to use:** Contacts and renewal months from their file. Do not invent phones, account numbers, or a website listing as their account. List company, service, and dates they stored. W-9 may be a present flag without a full TIN in the pack. You do not pay, cancel, or pick a winner. Notice windows are copied dates, not legal readings. Two vendors for one service: list both. Starter facilities list until they teach this shop's contacts.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: vendor-contacts
steps:
  - id: list
    needs: []
    produces: vendors
    produce_path: work/office-vendors.csv
    tool: docs/tools/vendor-list.md
    check: python docs/tools/checks/csv-has-columns.py work/office-vendors.csv company service
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [vendors]
    produces: vend-pack
    produce_path: out/office-vendors.md
    tool: docs/tools/vendor-list.md
    check: python docs/tools/checks/file-exists.py out/office-vendors.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
