# Work Item Rules

Rules are constraints that MUST be followed during this dispatch pack. Violations should be logged in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Triggers:** write:doc | write:csv | none
**Captured:** YYYY-MM-DD
**Source:** [Optional]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]

---
```

**Note:** Work Item-level rules do NOT need a `**Workflows:**` field — they inherit this pack’s registered workflow.

For Expert Role-level rules: `Workflows: all` → `facts/rules-shared.md`; a registered role job → `facts/rules-operations.md`. Triggers: `write:doc | write:csv | none`.

##

[Rules will be added here as they are captured during this pack]
