# Capacity Vs Booked

**When to use:** Compare their capacity file to the boarding export for the date they asked. Use their max, not a number from another kennel. Do not raise a cap on paper. Do not staff the floor. Split daycare and overnight if their columns split. Quote both numbers in the pack when booked meets or exceeds max. Starter / guess until they teach weekday versus peak caps.

**How to run:** If no Work Item exists, run workflow-selector. Follow the steps below. After each step, journal-keeper.

**Human gates:** Do not change their max. If booked meets or exceeds max, quote both and ask who decides holds or waitlist moves.

**Initial phase:** capacity

## Steps

Paths are relative to `work-items/<id>/`.

1. **Capacity file**
   - Tool: `docs/tools/capacity-file.md`
   - Produce: `work/capacity.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/capacity.csv room max`

2. **Booked stays**
   - Needs: `work/capacity.csv`
   - Tool: `docs/tools/boarding-csv.md`
   - Produce: `work/boarding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/boarding.csv patient stay`

3. **Write comparison pack**
   - Needs: `work/capacity.csv`, `work/boarding.csv`
   - Produce: `out/capacity-vs-booked.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/capacity-vs-booked.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach weekday versus peak caps.
