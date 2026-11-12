# Facility requests missing COI

**When to use:** Index facility requests they stored, then mark which still-scheduled outside uses lack a COI on their checklist. Do not approve the request. Do not decide coverage or invent a limit. Expired certificates on live dates stay flagged. Member-only exemptions come only from their policy sentence. Write-up is a missing-COI list plus form-versus-calendar holes. They chase the group. You do not waive a certificate.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: facility-coi-missing
steps:
  - id: requests
    needs: []
    produces: requests
    produce_path: work/facility-requests.csv
    tool: docs/tools/facility-request-folder.md
    check: python docs/tools/checks/file-exists.py work/facility-requests.csv
    on_fail: retry
    next: [coi]
  - id: coi
    needs: [requests]
    produces: coi
    produce_path: work/coi-index.csv
    tool: docs/tools/coi-folder.md
    check: python docs/tools/checks/file-exists.py work/coi-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [requests, coi]
    produces: coi-pack
    produce_path: out/facility-coi-missing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/facility-coi-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
