# New Client Forms

**When to use:** From registration PDFs, list missing pages and signatures. Do not take a clinical history. Check name, contacts, patient identity, dates, and photo-policy acknowledgment if they use one. Authorized-agent pages are a signature check, not a consent decision you make. Do not store extra ID images here. Incomplete packets are a yes-or-no completeness list for staff. Starter / guess until they teach the current packet and e-sign rules.

**How to run:** Open/reuse a Work Item under `work-items/<id>/`. Follow this map one ready step (or the whole named job if requested). Read the named `docs/tools/` file. Write produce_path inside this Work Item. Run the step check. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: new-client-forms
steps:
  - id: list
    needs: []
    produces: nc-raw
    produce_path: work/new-client-forms.csv
    tool: docs/tools/new-client-pdf.md
    check: python docs/tools/checks/file-exists.py work/new-client-forms.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [nc-raw]
    produces: nc-writeup
    produce_path: out/new-client-forms.md
    tool: docs/tools/new-client-pdf.md
    check: python docs/tools/checks/file-exists.py out/new-client-forms.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this clinic works.
