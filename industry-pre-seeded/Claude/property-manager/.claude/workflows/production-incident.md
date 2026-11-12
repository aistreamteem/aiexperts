# Production incident (optional scaffold)

Not registered for this property-manager role. Present so leftover developer skills that name the workflow have a real instruction file. Do **not** add it to `workflow-registry.json` until define-role enables it.

## When to use

A live production outage or degradation that this expert is asked to help triage. Property-manager Work Items do not use this map.

## Phases

1. **Assess** — what is affected, who escalated, where evidence lives (`docs/incident/assessment.md`)
2. **Stabilize** — contain impact; record actions and blockers
3. **Analyze root cause** — evidence-backed hypothesis; no invented shop procedure
4. **Remediate** — approved fix or handoff; record result
5. **Close** — summary, follow-ups, promote durable facts/rules if asked

## Gates

- Do not mark a phase complete while blocking questions remain
- Do not invent monitoring dashboards or on-call process for this shop
- Journal via journal-keeper under `journals/work-items/<id>/`

## Artifacts

- `docs/incident/assessment.md`
- Work Item `out/` summary and `evidence/` logs when used