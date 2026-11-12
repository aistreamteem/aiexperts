# Production Incident Workflow

**When to use:** Production incidents, urgent bugs, hotfixes, escalations. Existing architecture is known, so there is no HLD or DD phase.

**Status:** defined but not enabled. It is not in `workflow-registry.json`; `define-role` adds it only when the user gives an explicit yes.

## Phase Sequence

assess-incident → analyze-root-cause → apply-mitigation → monitor-impact → resolve-and-document → done

## Approval Gates

- **Fix approach approval** (after analyze-root-cause, before apply-mitigation): next action waits for "I approve the fix approach" or "Skip fix approach approval"
- **Deployment approval** (before any change reaches production): next action waits for "I approve the deployment" or "Skip deployment approval"

"continue" is never an approval. See `CLAUDE.md` rule 6.

## Artifact Organization

- Assessment: `work-items/<id>/docs/incident/assessment.md`
- Root cause analysis: `work-items/<id>/docs/incident/root-cause-analysis.md`
- Mitigation log: `work-items/<id>/docs/incident/mitigation-log.md`
- Resolution: `work-items/<id>/docs/incident/resolution.md`
- Journal: `journals/work-items/<id>/` (item-wide fields in `progress.md`, step notes and next action in `nodes/`)

## Phase Behaviors

#### assess-incident

- Run through `spec-parser` with the incident artifact path
- Write to `docs/incident/assessment.md`
- Ask: what is affected, who has escalated, where the evidence is (logs, alerts, tickets)
- Set next action: "run analyze-root-cause"

#### analyze-root-cause

- Write to `docs/incident/root-cause-analysis.md`
- Reproduce the issue where possible; record evidence and hypotheses
- Propose a fix or mitigation approach
- Set next action: "wait for fix approach approval"

#### apply-mitigation

- Write to `docs/incident/mitigation-log.md`
- Record every change made, with time and who approved it
- Run the tests relevant to the fix
- Set next action: "wait for deployment approval", then "run monitor-impact"

#### monitor-impact

- Append observations to `docs/incident/mitigation-log.md`
- Confirm the mitigation is working, or return to analyze-root-cause
- Set next action: "run resolve-and-document"

#### resolve-and-document

- Write to `docs/incident/resolution.md`
- Record the cause, the fix, the follow-up work, and lessons learned
- Offer to capture reusable lessons through `remember`
- Set next action: "done"

## Rules to Load

- `facts/rules-shared.md` and `facts/facts-shared.md`
- `facts/rules-incident-response.md` and `facts/facts-incident-response.md`, when they exist
- `work-items/<id>/facts/rules.md` (Work Item rules)

Rules MUST be followed; log violations to the journal.
