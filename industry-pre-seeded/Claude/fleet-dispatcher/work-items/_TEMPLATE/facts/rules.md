# Work Item Rules

Rules are constraints that MUST be followed during this dispatch pack. Violations should be logged in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Triggers:** write:doc | write:csv | write:pack | none
**Captured:** YYYY-MM-DD
**Source:** [Optional]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]

---
```

**Note:** Work Item-level rules do NOT need a `**Workflows:**` field — they inherit this pack’s registered workflow.

For Expert Role-level rules with `**Workflows:** all`, append to `facts/rules-shared.md`. Job-scoped Expert Role notes go to `facts/rules-operations.md`. Include a `**Triggers:**` line.

##

[Rules will be added here as they are captured during this pack]
