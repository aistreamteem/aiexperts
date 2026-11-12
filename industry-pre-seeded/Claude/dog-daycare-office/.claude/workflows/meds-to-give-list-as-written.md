# Meds To Give List As Written

**When to use:** From boarding cards and the feeding or meds sheet, list meds-to-give exactly as written and whether today’s medication log page is present. Never prescribe, convert a dose, or fill staff initials. Flag unreadable lines and blank log boxes. This is not a veterinary refill list. Late-med codes copy as theirs and route. Starter / guess until they teach who gives meds and which clipboard is official.

**How to run:** If no Work Item exists, run workflow-selector. Follow the steps below. After each step, journal-keeper.

**Human gates:** Unreadable dose lines → ask. Blank log boxes stay blank. You do not give the medication.

**Initial phase:** care-lists

## Steps

Paths are relative to `work-items/<id>/`.

1. **Occupancy / cards**
   - Tool: `docs/tools/boarding-csv.md`
   - Produce: `work/boarding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/boarding.csv patient stay`

2. **Meds / feeding sheet**
   - Needs: `work/boarding.csv`
   - Tool: `docs/tools/feeding-sheet.md`
   - Produce: `work/feeding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/feeding.csv patient food`

3. **Write meds-to-give pack**
   - Needs: `work/boarding.csv`, `work/feeding.csv`
   - Produce: `out/meds-to-give.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/meds-to-give.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach who gives meds and which clipboard is official.
