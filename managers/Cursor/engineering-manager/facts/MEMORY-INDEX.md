# Memory System Index

Load this index first, then the shared pair, then only the workflow pair you need.

## Two axes

1. **Workflow axis** (this file). Always load `facts-shared.md` and `rules-shared.md`. Then load `facts-<workflow>.md` and `rules-<workflow>.md` for the session.
2. **Trigger axis** (`TRIGGER-INDEX.md`, generated). Rules carry `**Triggers:**`. The hook `.cursor/hooks/inject_rules_on_action.py` injects a matching rule when that action happens.

Regenerate the trigger index with `python scripts/memory/build_trigger_index.py` after retagging a rule. Do not hand-edit `TRIGGER-INDEX.md` or `trigger-index.json`.

## Shared (always)

- [facts-shared.md](facts-shared.md)
- [rules-shared.md](rules-shared.md)

Entries marked `Workflows: all` live here.

## Team Delivery

**When to use:** Use when a team objective needs an outcome, owners, and a cadence, such as a delivery commitment, a staffing plan, or a delegation change.

- [facts-team-delivery.md](facts-team-delivery.md)
- [rules-team-delivery.md](rules-team-delivery.md)

## Team Escalation

**When to use:** Use when delivery slips, a people decision is urgent, or a production issue lands on the team.

- [facts-team-escalation.md](facts-team-escalation.md)
- [rules-team-escalation.md](rules-team-escalation.md)

Default workflow when a session is ambiguous: `team-delivery`.

Starter triggers: `meeting:1on1`, `hiring:loop`, `status:update`, `escalation:open`, `decision:log`, `write:doc`.

## Fact entry

```markdown
### year-month-day: Descriptive Title

**Scope:** expert-role

**Workflows:** team-delivery | team-escalation | all

**Captured:** year-month-day

**Source:** where this came from

What is true, and why it matters for this role.
```

## Rule entry

```markdown
### year-month-day: Prescriptive Title

**Scope:** expert-role

**Workflows:** team-delivery | team-escalation | all

**Triggers:** meeting:1on1 | hiring:loop | status:update | escalation:open | decision:log | write:doc | none

**Captured:** year-month-day

**Source:** where this came from

**Rule:** What must be done

**Why:** Why it matters

**How to apply:** What to do when it applies
```
