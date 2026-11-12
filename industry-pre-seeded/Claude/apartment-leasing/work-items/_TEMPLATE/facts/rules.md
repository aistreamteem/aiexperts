# Work Item Rules

Rules are constraints that MUST be followed during this leasing job. Log violations in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Triggers:** none | write:doc | write:csv
**Captured:** YYYY-MM-DD
**Source:** [operator]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]
```

Work Item rules do not need `**Workflows:**` — they inherit this Work Item’s registry job.

Expert Role rules live in `facts/rules-shared.md`.

---

[Rules will be added here as they are captured]
