# Management Initiative

**When to use:** Use when an outcome needs owners, a cadence, decisions, and stakeholder communication.

## Phase Sequence

intake → charter-writer → plan-writer → diagram-generator → action-breakdown → kickoff → execute-action (loop) → verify → close-out → done

## Approval Gates

- **Charter approval** after the charter and diagrams: "I approve the charter" or "Skip charter approval"
- **Plan approval** after the operating plan and diagrams: "I approve the plan" or "Skip plan approval"
- **Change approval** for change-request: "I approve the change" or "Skip change approval"

## Artifact Organization

- Brief: `work-items/<id>/docs/charter/brief.md`
- Charter: `work-items/<id>/docs/charter/charter.md`
- Operating Plan: `work-items/<id>/docs/plan/operating-plan.md`
- Diagrams: `work-items/<id>/docs/diagrams/*.mmd` and `index.html`
- Decision log: `work-items/<id>/docs/decisions/decision-log.md`
- Actions: `work-items/<id>/TODOS.md`
- Changes: `work-items/<id>/docs/changes/<change-id>/`
- Verification: `work-items/<id>/docs/verification/verification.md`

## Phase Behaviors

### intake

- Write `docs/charter/brief.md`
- Ask: What outcome is needed?; Who is affected and who decides?; What does success look like?; What cadence already exists?
- Set next action: "run charter-writer"

### charter-writer

- Ask charter depth: Standard, Part 1, or Extended
- Write `docs/charter/charter.md` titled **Charter** with sections: Outcome, Scope, Stakeholders, Success, Constraints
- Draft the diagrams listed below
- Set next action: "wait for charter approval"

### plan-writer

- Write `docs/plan/operating-plan.md` titled **Operating Plan** with sections: Owners, Cadence, Decisions needed, Risks, Communications
- Update diagrams
- Set next action: "wait for plan approval"

### diagram-generator

- Write one Mermaid file per diagram: Stakeholder map, Operating cadence, RACI, Decision flow
- Refresh `docs/diagrams/index.html`
- Set next action: "run action-breakdown"

### action-breakdown

- Write `TODOS.md` with sections: Setup, Dependencies and asks, Kickoff, Execution, Verification, Communication and close-out
- Order setup and kickoff before execution
- Set next action: "run kickoff"

### kickoff

- Create: Operating cadence, Decision log, Status tracker, Stakeholder list
- Set next action: "execute-action (task 1/N)"

### execute-action

- Complete one TODO. Outputs include: Decision note, Status update, Stakeholder note, Cadence review, Delegation note
- Do not skip the charter gate or the plan gate.
- Set next action to the next task, or "run verify" when the list is finished

### verify

- Write `docs/verification/verification.md` covering: Success criteria checked, Stakeholder sign-off, Risk review
- Set next action: "run close-out"

### close-out

- Write the close-out: Outcome status, the decisions made, and a handoff.
- Record the status narrative, the decision-log path, and the handoff note in the journal
- Set next action: "done"
