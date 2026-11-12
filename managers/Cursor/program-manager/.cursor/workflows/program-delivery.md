# Program Delivery

**When to use:** Use when a cross-team effort needs a schedule, a RAID log, and a steering forum.

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
- Ask: What outcome is due, and by when?; What is in scope and out of scope?; Who governs this and who accepts a milestone?; Which dependencies are already known?
- Set next action: "run charter-writer"

### charter-writer

- Ask charter depth: Standard, Part 1, or Extended
- Write `docs/charter/charter.md` titled **Charter** with sections: Outcomes, In scope, Out of scope, Governance, Success measures, Stakeholders
- Draft the diagrams listed below
- Set next action: "wait for charter approval"

### plan-writer

- Write `docs/plan/operating-plan.md` titled **Operating Plan** with sections: Milestones, Dependencies, RAID, RACI, Communications cadence, Decision rights
- Update diagrams
- Set next action: "wait for plan approval"

### diagram-generator

- Write one Mermaid file per diagram: Milestone and dependency map, RACI, Governance path
- Refresh `docs/diagrams/index.html`
- Set next action: "run action-breakdown"

### action-breakdown

- Write `TODOS.md` with sections: Setup, Dependencies and asks, Kickoff, Execution, Verification, Communication and close-out
- Order setup and kickoff before execution
- Set next action: "run kickoff"

### kickoff

- Create: Integrated tracker, RAID log, Steering cadence, Stakeholder list
- Set next action: "execute-action (task 1/N)"

### execute-action

- Complete one TODO. Outputs include: Status report, RAID update, Dependency chase, Steering pack, Decision record
- Do not accept a milestone yourself when a named approver is recorded.
- Set next action to the next task, or "run verify" when the list is finished

### verify

- Write `docs/verification/verification.md` covering: Milestone acceptance by the named approver, Steering sign-off, Open-risk review
- Set next action: "run close-out"

### close-out

- Write the close-out: A narrative split into done, next, and blocked, plus a RAID snapshot and a handoff.
- Record the status narrative, the decision-log path, and the handoff note in the journal
- Set next action: "done"
