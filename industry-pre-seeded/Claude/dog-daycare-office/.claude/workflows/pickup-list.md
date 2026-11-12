# Pickup List

**When to use:** Build or check today’s pickup list against the occupancy file. Names as spelled. Flag people not on the list. Emergency contacts are not pickup unless the card says so. You never release a dog. If card and software disagree, quote both. Do not add a same-day name from a phone vibe. A complete CSV is still not a release you perform. Starter / guess until they teach ID-at-door rules and same-day adds.

**How to run:** If no Work Item exists, run workflow-selector. Follow the steps below. After each step, journal-keeper.

**Human gates:** You never release a dog. Same-day add to the list is their process, not a chat guess. Quote both files when they disagree.

**Initial phase:** pickup-list

## Steps

Paths are relative to `work-items/<id>/`.

1. **Authorized names**
   - Tool: `docs/tools/pickup-list.md`
   - Produce: `work/pickup-auth.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/pickup-auth.csv patient name`

2. **Occupancy**
   - Needs: `work/pickup-auth.csv`
   - Tool: `docs/tools/boarding-csv.md`
   - Produce: `work/boarding.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/boarding.csv patient stay`

3. **Write pickup pack**
   - Needs: `work/pickup-auth.csv`, `work/boarding.csv`
   - Produce: `out/pickup-list.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/pickup-list.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach ID-at-door rules and same-day adds.
