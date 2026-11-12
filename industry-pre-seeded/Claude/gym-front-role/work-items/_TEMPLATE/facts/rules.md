# Work Item Rules

Rules are constraints that MUST be followed during this gym role job. Violations go in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [Optional]
**Status:** [active | promoted-to-expert | archived]
**Triggers:** write:doc | write:csv | write:pack | none

**Rule:** [statement]
**Why:** [reason]

---
```

**Note:** Work Item-level rules do NOT need a `**Workflows:**` field — they inherit this Work Item's role job.

For Expert Role rules use `facts/rules-shared.md` (`Workflows: all`) or `facts/rules-operations.md` with a registered job id.

---

[Rules will be added here as they are captured during this Work Item]
