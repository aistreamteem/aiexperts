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

## Management Initiative

**When to use:** Use when an outcome needs owners, a cadence, decisions, and stakeholder communication.

- [facts-management-initiative.md](facts-management-initiative.md)
- [rules-management-initiative.md](rules-management-initiative.md)

## Management Escalation

**When to use:** Use when a decision is stuck, a commitment is at risk, or stakeholders conflict.

- [facts-management-escalation.md](facts-management-escalation.md)
- [rules-management-escalation.md](rules-management-escalation.md)

Default workflow when a session is ambiguous: `management-initiative`.

Starter triggers: `decision:log`, `status:update`, `stakeholder:update`, `escalation:open`, `cadence:review`, `write:doc`.

## Fact entry

```markdown
### year-month-day: Descriptive Title

**Scope:** expert-role

**Workflows:** management-initiative | management-escalation | all

**Captured:** year-month-day

**Source:** where this came from

What is true, and why it matters for this role.
```

## Rule entry

```markdown
### year-month-day: Prescriptive Title

**Scope:** expert-role

**Workflows:** management-initiative | management-escalation | all

**Triggers:** decision:log | status:update | stakeholder:update | escalation:open | cadence:review | write:doc | none

**Captured:** year-month-day

**Source:** where this came from

**Rule:** What must be done

**Why:** Why it matters

**How to apply:** What to do when it applies
```
