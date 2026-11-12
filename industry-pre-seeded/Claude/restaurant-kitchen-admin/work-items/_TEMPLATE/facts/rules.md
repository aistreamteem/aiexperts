# Work Item Rules

Rules are constraints that MUST be followed during this job. Violations go in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Triggers:** none | write:sheet | write:pack | file:intake
**Captured:** YYYY-MM-DD
**Source:** [operator, shop sheet, etc.]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]
```

Work Item-level rules do not need a `**Workflows:**` field — they inherit this Work Item’s job.

For Expert Role rules, append to `facts/rules-operations.md` (see `facts/MEMORY-INDEX.md`).

---

[Rules will be added here as they are captured during this job]
