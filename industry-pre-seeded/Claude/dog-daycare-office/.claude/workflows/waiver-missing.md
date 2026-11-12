# Waiver Missing

**When to use:** From the waiver folder and the stay list, list dogs whose waiver is unsigned, undated, wrong version, or missing pages. Do not give a legal opinion. Do not skip a trial day unless they wrote an exception. Photo-release pages are separate if their packet splits them. A complete waiver is not a medical clearance. Starter / guess until they teach the current version and e-sign rules.

**How to run:** If no Work Item exists, run workflow-selector. Follow the steps below. After each step, journal-keeper.

**Human gates:** Do not treat an unsigned waiver as complete. Do not explain what a court would do. Trial-day exceptions must be their written exception, not yours.

**Initial phase:** intake-completeness

## Steps

Paths are relative to `work-items/<id>/`.

1. **Waiver folder index**
   - Tool: `docs/tools/waiver-folder.md`
   - Produce: `work/waivers.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/waivers.csv patient file`

2. **Stay list**
   - Needs: `work/waivers.csv`
   - Tool: `docs/tools/boarding-csv.md`
   - Produce: `work/boarding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/boarding.csv patient stay`

3. **Write missing-waiver pack**
   - Needs: `work/waivers.csv`, `work/boarding.csv`
   - Produce: `out/waiver-missing.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/waiver-missing.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach the current version and e-sign rules.
