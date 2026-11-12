# Memory System Index

Load this index first, then the shared pair, then only the workflow pair you need.

## Two axes

1. **Workflow axis** (this file). Always load `facts-shared.md` and `rules-shared.md`. Then load `facts-<workflow>.md` and `rules-<workflow>.md` for the session.
2. **Trigger axis** (`TRIGGER-INDEX.md`, generated). Rules carry `**Triggers:**`. The hook `.claude/hooks/inject_rules_on_action.py` injects a matching rule when that action happens.

Regenerate the trigger index with `python scripts/memory/build_trigger_index.py` after retagging a rule. Do not hand-edit `TRIGGER-INDEX.md` or `trigger-index.json`.

## Shared (always)

- [facts-shared.md](facts-shared.md)
- [rules-shared.md](rules-shared.md)

Entries marked `Workflows: all` live here.

## Program Delivery

**When to use:** Use when a cross-team effort needs a schedule, a RAID log, and a steering forum.

- [facts-program-delivery.md](facts-program-delivery.md)
- [rules-program-delivery.md](rules-program-delivery.md)

## Program Escalation

**When to use:** Use when a milestone is blocked, a dependency fails, or scope is disputed.

- [facts-program-escalation.md](facts-program-escalation.md)
- [rules-program-escalation.md](rules-program-escalation.md)

Default workflow when a session is ambiguous: `program-delivery`.

Starter triggers: `status:report`, `raid:update`, `milestone:review`, `scope:change`, `steering:pack`, `write:doc`.

## Fact entry

```markdown
### year-month-day: Descriptive Title

**Scope:** expert-role

**Workflows:** program-delivery | program-escalation | all

**Captured:** year-month-day

**Source:** where this came from

What is true, and why it matters for this role.
```

## Rule entry

```markdown
### year-month-day: Prescriptive Title

**Scope:** expert-role

**Workflows:** program-delivery | program-escalation | all

**Triggers:** status:report | raid:update | milestone:review | scope:change | steering:pack | write:doc | none

**Captured:** year-month-day

**Source:** where this came from

**Rule:** What must be done.

**Why:** Why the rule exists.

**How to apply:** How to follow it in this role.
```
