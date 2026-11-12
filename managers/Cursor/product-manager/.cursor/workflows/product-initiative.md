# Product Initiative

**When to use:** Use when a user problem needs an outcome, a now-versus-later cut, and stakeholder alignment.

## Phase Sequence

intake → charter-writer → plan-writer → diagram-generator → action-breakdown → kickoff → execute-action (loop) → verify → close-out → done

## Approval Gates

- **Charter approval** after the opportunity brief and diagrams: "I approve the charter" or "Skip charter approval"
- **Plan approval** after the product plan and diagrams: "I approve the plan" or "Skip plan approval"
- **Change approval** for change-request: "I approve the change" or "Skip change approval"

## Artifact Organization

- Brief: `work-items/<id>/docs/charter/brief.md`
- Opportunity Brief: `work-items/<id>/docs/charter/charter.md`
- Product Plan: `work-items/<id>/docs/plan/operating-plan.md`
- Diagrams: `work-items/<id>/docs/diagrams/*.mmd` and `index.html`
- Decision log: `work-items/<id>/docs/decisions/decision-log.md`
- Actions: `work-items/<id>/TODOS.md`
- Changes: `work-items/<id>/docs/changes/<change-id>/`
- Verification: `work-items/<id>/docs/verification/verification.md`

## Phase Behaviors

### intake

- Write `docs/charter/brief.md`
- Ask: What problem is this, and for whom?; What outcome would show it is solved?; What is explicitly out of scope?; Who must agree before this plan is current?
- Set next action: "run charter-writer"

### charter-writer

- Ask charter depth: Standard, Part 1, or Extended
- Write `docs/charter/charter.md` titled **Opportunity Brief** with sections: Problem, Users, Outcome, Non-goals, Assumptions
- Draft the diagrams listed below
- Set next action: "wait for charter approval"

### plan-writer

- Write `docs/plan/operating-plan.md` titled **Product Plan** with sections: Scope now, Scope later, Success metrics, Risks, Rollout narrative, Open decisions
- Update diagrams
- Set next action: "wait for plan approval"

### diagram-generator

- Write one Mermaid file per diagram: Journey, Prioritization, Stakeholder map, Decision flow
- Refresh `docs/diagrams/index.html`
- Set next action: "run action-breakdown"

### action-breakdown

- Write `TODOS.md` with sections: Setup, Dependencies and asks, Kickoff, Execution, Verification, Communication and close-out
- Order setup and kickoff before execution
- Set next action: "run kickoff"

### kickoff

- Create: Discovery log, Decision log, Roadmap slice, Stakeholder list
- Set next action: "execute-action (task 1/N)"

### execute-action

- Complete one TODO. Outputs include: Discovery note, Prioritization decision, Roadmap update, Stakeholder readout, Metric check
- Do not turn an execute action into a build task.
- Set next action to the next task, or "run verify" when the list is finished

### verify

- Write `docs/verification/verification.md` covering: Outcome criteria checked, Stakeholder sign-off, Unresolved-assumption review
- Set next action: "run close-out"

### close-out

- Write the close-out: Outcome versus plan, the decisions made, and what moved to later.
- Record the status narrative, the decision-log path, and the handoff note in the journal
- Set next action: "done"
