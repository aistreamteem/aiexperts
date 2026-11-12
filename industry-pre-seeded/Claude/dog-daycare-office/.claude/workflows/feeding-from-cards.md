# Feeding From Cards

**When to use:** Transcribe feeding as the client wrote it onto the feeding sheet for the stay date. Do not substitute a bag or invent cups. Unreadable lines are questions. Allergy words stay theirs, not a diagnosis. Confirm the occupancy list so you do not feed a dog who is not here. House food is only a named backup on their sheet. Starter / guess until they teach who initials the clipboard.

**How to run:** If no Work Item exists, run workflow-selector. Follow the steps below. After each step, journal-keeper.

**Human gates:** Unreadable feeding lines → ask. Do not diagnose an allergy. Do not invent house food.

**Initial phase:** care-lists

## Steps

Paths are relative to `work-items/<id>/`.

1. **Occupancy / cards**
   - Tool: `docs/tools/boarding-csv.md`
   - Produce: `work/boarding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/boarding.csv patient stay`

2. **Feeding sheet**
   - Needs: `work/boarding.csv`
   - Tool: `docs/tools/feeding-sheet.md`
   - Produce: `work/feeding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/feeding.csv patient food`

3. **Write feeding pack**
   - Needs: `work/boarding.csv`, `work/feeding.csv`
   - Produce: `out/feeding-from-cards.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/feeding-from-cards.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach who initials the clipboard.
