# Waitlist

**When to use:** From their waitlist sheet and calendar, list order, requested dates, and stay type. Do not jump a row. Do not confirm a stay unless they asked you to draft from their process. Do not invent a peak deposit. Vaccine-file and waiver gates stay present or missing, never a medical due-date. You do not message the list as a blast. Starter / guess until they teach the sort key and who calls the next name.

**How to run:** If no Work Item exists, run workflow-selector. Follow the steps below. After each step, journal-keeper.

**Human gates:** Do not jump the order. Do not confirm a stay or invent a deposit. Who calls the next name is theirs.

**Initial phase:** waitlist

## Steps

Paths are relative to `work-items/<id>/`.

1. **Waitlist sheet**
   - Tool: `docs/tools/spreadsheet.md`
   - Produce: `work/waitlist.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/waitlist.csv client date`

2. **Calendar**
   - Needs: `work/waitlist.csv`
   - Tool: `docs/tools/calendar.md`
   - Produce: `work/calendar.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/calendar.csv date status`

3. **Write waitlist pack**
   - Needs: `work/waitlist.csv`, `work/calendar.csv`
   - Produce: `out/waitlist.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/waitlist.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach the sort key and who calls the next name.
