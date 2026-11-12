# Incident Routing

**When to use:** From the incident log and completed forms, list time, patient-dog, form present or missing, and who was notified as their process. Do not diagnose. Do not write a legal opinion on a bite. Do not bury interrupt rows. Minimum data: IDs and filenames. Escapes stay on the same pack if they logged them. Starter / guess until they teach who is interrupted and the current form version.

**How to run:** If no Work Item exists, run workflow-selector. Follow the steps below. After each step, journal-keeper.

**Human gates:** You route; you do not adjudicate. Named person decides client call, agency call, and clinical follow-up.

**Initial phase:** incident-routing

## Steps

Paths are relative to `work-items/<id>/`.

1. **Incident log**
   - Tool: `docs/tools/incident-log.md`
   - Produce: `work/incidents.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/incidents.csv time patient`

2. **Forms present or missing**
   - Needs: `work/incidents.csv`
   - Tool: `docs/tools/incident-form.md`
   - Produce: `work/incident-forms.csv`
   - Check: `python docs/tools/checks/csv-has-columns.py work-items/<id>/work/incident-forms.csv file patient`

3. **Write routing pack**
   - Needs: `work/incidents.csv`, `work/incident-forms.csv`
   - Produce: `out/incident-routing.md`
   - Check: `python docs/tools/checks/file-exists.py work-items/<id>/out/incident-routing.md`
   - Copy check logs to `evidence/`. Update STATUS.md.

Starter map. Replace tools and checks when they teach who is interrupted and the current form version.
