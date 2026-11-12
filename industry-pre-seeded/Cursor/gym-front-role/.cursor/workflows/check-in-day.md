# Day check-in list

**When to use:** Build today’s check-in list from their scan export. Join access flags so denied or frozen rows stay visible. Do not invent a visit and do not clear a deny. Guests without a pass row stay exceptions. Kid-area scans stay on their file unless they taught a merge. Hours file still does not create a check-in. Produce the list plus a pack note. They greet and they override. Starter until they teach this club’s scan columns.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Follow this file's YAML via **continue**. Read the cited `docs/tools/` doc, write artifacts under the Work Item, run the step `check`, store logs in `evidence/`, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: check-in-day
steps:
  - id: pull
    needs: []
    produces: checkins
    produce_path: work/check-in.csv
    tool: docs/tools/check-in-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/check-in.csv member_id status
    on_fail: retry
    next: [flags]
  - id: flags
    needs: [checkins]
    produces: flags
    produce_path: work/access-flags.csv
    tool: docs/tools/access-flag-export.md
    check: python docs/tools/checks/file-exists.py work/access-flags.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [checkins, flags]
    produces: checkin-pack
    produce_path: out/check-in-day.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/check-in-day.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
