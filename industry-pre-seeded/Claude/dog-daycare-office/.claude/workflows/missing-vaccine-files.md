# Missing Vaccine Files

**When to use:** From their vaccine index and today’s stay list, list patient-dogs whose required pages are missing, unreadable, or the wrong dog. Present or missing only. Never decide a vaccine is due medically. Never interpret a titer. Do not paste certificate tables. Rabies pages they require are the same rule. Starter / guess until they teach which named pages this shop requires for daycare versus board.

**How to run:** If no Work Item exists, run workflow-selector. Follow the steps below. After each step, journal-keeper.

**Human gates:** Do not publish a group occupancy list that treats a dog as complete when a required rabies page is missing — ask first. Titer pages are present or missing; you do not read the number.

**Initial phase:** intake-completeness

## Steps

Paths are relative to `work-items/<id>/`.

1. **Vaccine index**
   - Tool: `docs/tools/vaccine-file-index.md`
   - Produce: `work/vaccine-index.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/vaccine-index.csv patient file`

2. **Today’s stays**
   - Needs: `work/vaccine-index.csv`
   - Tool: `docs/tools/boarding-csv.md`
   - Produce: `work/boarding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/boarding.csv patient stay`

3. **Write missing-file pack**
   - Needs: `work/vaccine-index.csv`, `work/boarding.csv`
   - Produce: `out/missing-vaccine-files.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/missing-vaccine-files.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach which named pages this shop requires.
