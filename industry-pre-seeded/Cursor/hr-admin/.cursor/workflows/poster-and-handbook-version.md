# Poster index and handbook version

**When to use:** Read their poster index and the live handbook PDF. List poster files or wall-check dates as they logged them, plus the handbook version string. Do not invent a legally required poster set. Do not rewrite the handbook. If two handbook PDFs look current, ask which wins. Missing poster on their index is an ask. Write the version-and-poster pack. They hang posters and they publish the book. DOL poster pages are orientation for names they may already use, not a citation list you create.

## How to run

1. Open or switch to one Work Item under `work-items/<id>/` (`workflow-selector` if the job is not selected yet). Put source files in that item's `in/`.
2. Follow this file's YAML: one ready step per **continue**, or the whole named job if the operator requested it. Read the named `docs/tools/` doc. Write `produce_path` under this Work Item. Run the step `check`. Retry at most three times, then ask.
3. Run **journal-keeper** after the step (or job) completes.

**Initial phase:** `role-job`

## Work map

```yaml
id: poster-and-handbook-version
steps:
  - id: posters
    needs: []
    produces: posters
    produce_path: work/poster-index.csv
    tool: docs/tools/poster-index.md
    check: python docs/tools/checks/file-exists.py work/poster-index.csv
    on_fail: retry
    next: [book]
  - id: book
    needs: [posters]
    produces: handbook
    produce_path: work/handbook-version.txt
    tool: docs/tools/handbook-pdf.md
    check: python docs/tools/checks/file-exists.py work/handbook-version.txt
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [posters, handbook]
    produces: ver-pack
    produce_path: out/poster-handbook-version.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/poster-handbook-version.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
