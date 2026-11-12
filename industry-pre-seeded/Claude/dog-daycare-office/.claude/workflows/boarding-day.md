# Boarding Day

**When to use:** From their boarding export, list the stay date by patient-dog, client label they allow, stay type, and crate or playgroup as stored. Confirm the file date before you treat it as today. Do not invent a missing card. Do not diagnose from a floor note. Do not decide a vaccine is due. Never release a dog from this list. If capacity and booked disagree, quote both in the pack. Starter / guess until they teach which report is today’s board.

**How to run:** If no Work Item exists, run workflow-selector. Put operator files in `work-items/<id>/in/`. Follow the steps below (one ready step per continue, or the whole job if requested). After each step, journal-keeper.

**Human gates:** Missing boarding card → ask. Occupancy vs capacity disagreement → quote both; do not raise a cap. Clinical or release decisions stay with the named person.

**Initial phase:** occupancy-roster

## Steps

Paths are relative to `work-items/<id>/`.

1. **Pull boarding export**
   - Tool: `docs/tools/boarding-csv.md`
   - Produce: `work/boarding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/boarding.csv patient stay`
   - On fail: retry up to 3, then ask. Do not invent rows.

2. **Pull capacity file**
   - Needs: `work/boarding.csv`
   - Tool: `docs/tools/capacity-file.md`
   - Produce: `work/capacity.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/capacity.csv room max`
   - On fail: retry up to 3, then ask.

3. **Write occupancy pack**
   - Needs: `work/boarding.csv`, `work/capacity.csv`
   - Produce: `out/boarding-day.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/boarding-day.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach how *this* shop files today’s board.
