# Work Item Rules

Rules are constraints and procedures that MUST be followed during this Work Item. Violations should be logged in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [Optional]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]
```

Work Item-level rules do NOT need a `**Workflows:**` field — they inherit this Work Item.

For Expert Role-level rules: `Workflows: all` → `facts/rules-shared.md`; job-scoped → `facts/rules-operations.md`. Include `**Triggers:** write:csv | write:pack | write:doc | none`.

---

[Rules will be added here as they are captured during this pack]
