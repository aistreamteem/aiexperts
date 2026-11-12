# Work Item Rules

Rules are constraints and procedures that MUST be followed during this move or pack. Log violations in the journal.

**Format:**

```
### YYYY-MM-DD: [Label]
**Scope:** work-item
**Triggers:** write:csv | write:doc | write:estimate | none
**Captured:** YYYY-MM-DD
**Source:** [operator, file, chat]
**Status:** active | promoted-to-expert | archived

**Rule:** [statement]
```

Work Item rules do not need a `**Workflows:**` field; they inherit this job’s workflow. Include `**Triggers:**` so promoted rules stay hook-visible.

Expert Role rules: `Workflows: all` → `facts/rules-shared.md`; job-scoped → `facts/rules-operations.md`.

---

[Rules will be added here as they are captured during this Work Item]
