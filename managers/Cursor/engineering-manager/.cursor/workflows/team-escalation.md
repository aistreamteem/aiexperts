# Team Escalation

**When to use:** Use when delivery slips, a people decision is urgent, or a production issue lands on the team.

## Phase Sequence

assess-situation → analyze-impact → respond → monitor-situation → resolve-and-document → done

## Approval Gates

- **Response approval** after impact analysis: "I approve the response" or "Skip response approval"

## Artifact Organization

- `work-items/<id>/docs/escalations/assessment.md`
- `work-items/<id>/docs/escalations/impact.md`
- `work-items/<id>/docs/escalations/response.md`
- `work-items/<id>/docs/escalations/monitor.md`
- `work-items/<id>/docs/escalations/resolution.md`

## Phase Behaviors

### assess-situation

- Write `docs/escalations/assessment.md`
- Cover: Who is affected, what decision is needed today, what is communicated, and what is watched next.
- Set next action: "run analyze-impact"

### analyze-impact

- Write `docs/escalations/impact.md` with options and who decides
- Set next action: "wait for response approval"

### respond

- Write `docs/escalations/response.md` and carry out only the approved response
- Set next action: "run monitor-situation"

### monitor-situation

- Write what is being watched and the next check into `docs/escalations/monitor.md`
- Set next action: "run resolve-and-document"

### resolve-and-document

- Write `docs/escalations/resolution.md` as a management record of what was decided, what was communicated, and what remains open
- Set next action: "done"
