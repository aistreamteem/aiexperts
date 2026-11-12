# Production Incident Response Workflow

**When to use:** Production incidents, urgent bugs, hotfixes. Architecture is assumed known; no HLD/DD.

**Status:** Defined for skills that reference it. Not listed in `workflow-registry.json` until define-role (or a later promotion) enables it.

## Phase Sequence

assess-incident → analyze-root-cause → apply-mitigation → monitor-impact → resolve-and-document → done

## Approval Gates

- **Fix approach approval** (before applying mitigation): Next action waits for explicit approval or waiver
- **Deployment approval** (before pushing to production): Next action waits for explicit approval or waiver

## Artifact Organization

- Assessment: `work-items/<id>/docs/incident/assessment.md`
- Root cause: `work-items/<id>/docs/incident/root-cause-analysis.md`
- Mitigation log: `work-items/<id>/docs/incident/mitigation-log.md`
- Resolution: `work-items/<id>/docs/incident/resolution.md`
- Tests: focused regression for the fix under `work-items/<id>/tests/` or root `tests/`

## Phase Behaviors

#### assess-incident

- Capture what is affected, who escalated, and where the evidence is
- Write `docs/incident/assessment.md`
- Set next action: "run analyze-root-cause"

#### analyze-root-cause

- Reproduce or narrow the failure from evidence
- Write `docs/incident/root-cause-analysis.md`
- Set next action: "wait for fix approach approval" (or "run apply-mitigation" if waived)

#### apply-mitigation

- Implement the approved fix
- Append steps and results to `docs/incident/mitigation-log.md`
- Set next action: "run monitor-impact"

#### monitor-impact

- Observe post-change behaviour; update `docs/incident/mitigation-log.md`
- Set next action: "wait for deployment approval" when a production push is required, else "run resolve-and-document"

#### resolve-and-document

- Write `docs/incident/resolution.md` (cause, fix, follow-ups)
- Set next action: "done"

## Characteristics

- No HLD/DD phase
- Fast iteration focused on immediate resolution
- Minimal documentation during the incident; post-incident write-up after resolution
- Streamlined testing focused on the specific fix
