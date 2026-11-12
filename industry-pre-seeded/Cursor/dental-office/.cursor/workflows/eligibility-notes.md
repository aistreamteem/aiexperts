# Eligibility Notes

**When to use:** Quote in-network, deductible, and remaining maximum only as the dated screenshot shows. Ask if the image is missing or stale. Do not call the payer. Do not invent a remaining maximum from chat or a similar employer. Frequency sentences are quoted text, not a clinical due date and not a CDT choice. Do not promise benefits will pay. Quote the dental block they pointed to. Least PHI: the figures they asked for, not extra member identifiers.

**How to run:** Open or reuse `work-items/<id>/`. Put the source export in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: eligibility-notes
steps:
  - id: index
    needs: []
    produces: elig-index
    produce_path: work/eligibility-index.csv
    tool: docs/tools/eligibility-screenshot.md
    check: python docs/tools/checks/file-exists.py work/eligibility-index.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [elig-index]
    produces: elig-writeup
    produce_path: out/eligibility-notes.md
    tool: docs/tools/eligibility-screenshot.md
    check: python docs/tools/checks/file-exists.py out/eligibility-notes.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this office works.
