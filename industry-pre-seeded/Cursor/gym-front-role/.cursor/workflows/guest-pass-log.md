# Guest-pass log

**When to use:** Build the guest-pass log from check-ins plus the membership export for host rows if their file requires a host. Waiver present stays a join to the waiver folder when they asked. Do not invent a free pass or write a guest onto the member roster. Produce the log plus a pack note. They sell the day pass. Starter until they teach this club’s guest rules.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Follow this file's YAML via **continue**. Read the cited `docs/tools/` doc, write artifacts under the Work Item, run the step `check`, store logs in `evidence/`, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: guest-pass-log
steps:
  - id: checkins
    needs: []
    produces: checkins
    produce_path: work/check-in.csv
    tool: docs/tools/check-in-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/check-in.csv member_id status
    on_fail: retry
    next: [members]
  - id: members
    needs: [checkins]
    produces: members
    produce_path: work/membership.csv
    tool: docs/tools/membership-export.md
    check: python docs/tools/checks/file-exists.py work/membership.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [checkins, members]
    produces: guest-pack
    produce_path: out/guest-pass-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/guest-pass-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
