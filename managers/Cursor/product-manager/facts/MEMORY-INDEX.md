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

## Product Initiative

**When to use:** Use when a user problem needs an outcome, a now-versus-later cut, and stakeholder alignment.

- [facts-product-initiative.md](facts-product-initiative.md)
- [rules-product-initiative.md](rules-product-initiative.md)

## Product Escalation

**When to use:** Use for a launch problem, a priority conflict, or a user issue that changes the outcome.

- [facts-product-escalation.md](facts-product-escalation.md)
- [rules-product-escalation.md](rules-product-escalation.md)

Default workflow when a session is ambiguous: `product-initiative`.

Starter triggers: `discovery:note`, `roadmap:update`, `prioritization:decide`, `stakeholder:update`, `metric:review`, `write:doc`.

## Fact entry

```markdown
### year-month-day: Descriptive Title

**Scope:** expert-role

**Workflows:** product-initiative | product-escalation | all

**Captured:** year-month-day

**Source:** where this came from

What is true, and why it matters for this role.
```

## Rule entry

```markdown
### year-month-day: Prescriptive Title

**Scope:** expert-role

**Workflows:** product-initiative | product-escalation | all

**Triggers:** discovery:note | roadmap:update | prioritization:decide | stakeholder:update | metric:review | write:doc | none

**Captured:** year-month-day

**Source:** where this came from

**Rule:** What must be done

**Why:** Why it matters

**How to apply:** What to do when it applies
```
