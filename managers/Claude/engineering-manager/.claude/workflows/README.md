# Workflow Framework

Workflows are registered in `workflow-registry.json`. Each work item stores `Workflow type` in its journal. continue loads the matching instruction file.

## Available Workflows

1. **Team Delivery** (`team-delivery`)
   - Use when a team objective needs an outcome, owners, and a cadence, such as a delivery commitment, a staffing plan, or a delegation change.
   - Gates: charter approval, plan approval
   - Artifacts: `docs/charter/`, `docs/plan/`, `docs/diagrams/`, `TODOS.md`, `docs/verification/`

2. **Team Escalation** (`team-escalation`)
   - Use when delivery slips, a people decision is urgent, or a production issue lands on the team.
   - Gate: response approval
   - Artifacts: `docs/escalations/`

define-role may disable one of these or approve a third pipeline. workflow-selector offers only workflows still listed in the registry.

## How a work item runs

1. continue reads `Workflow type` from the journal. If it is missing, workflow-selector asks the operator to choose.
2. The instruction file supplies the phase order, the gates, and the artifact paths.
3. journal-keeper records the phase, the artifacts, and the next action.

## Adding a workflow

Do this only from define-role, after the operator approves the role:

1. Add the workflow to `workflow-registry.json` with `name`, `description`, `instruction_file`, and `initial_phase`.
2. Create `.claude/workflows/<key>.md` with the phase sequence, gates, artifacts, and phase behaviors.
3. Point the new phases at skills that already exist, or describe the new skill in `.claude/role-skills.md` and add the skill folder in the same turn the operator approved it.
