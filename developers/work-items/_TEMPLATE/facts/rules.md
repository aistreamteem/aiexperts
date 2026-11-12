# Work Item Rules

Rules are constraints, procedures, and patterns that MUST be followed during this Work Item. They are prescriptive and violations should be logged in the journal.

## Format

```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [Optional: user name, URL, chat thread, etc.]
**Status:** [active | promoted-to-expert | archived]

[Content with full formatting preserved]

---
```

**Note:** Work Item-level rules do NOT need a `**Workflows:**` field. They inherit the Work Item's workflow context.

Expert Role-level rules live in `facts/rules-<workflow>.md` (and `facts/rules-shared.md` for `Workflows: all`). Their entries add workflow applicability and an action trigger:

```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** all | developer | production-incident | [comma-separated list]
**Triggers:** [write:sql | write:doc | pr:open | git:push | git:commit | sql:generate | none]
**Captured:** YYYY-MM-DD
**Source:** [Optional]

**Rule:** [statement]

**Why:** [reason]

**How to apply:** [steps]

**Violation:** [consequence]

---
```

## Entries

[Rules will be added here as they are captured during Work Item execution]
