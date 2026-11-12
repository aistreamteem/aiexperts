# Work Item Rules

Rules are constraints that MUST be followed during this inventory job. Log violations in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [operator]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]
```

Work Item rules do not need `**Workflows:**` — they inherit this Work Item’s registry job.

For Expert Role rules use `facts/rules-shared.md` (`Workflows: all`) or `facts/rules-operations.md` with a registered job id.

---

[Rules will be added here as they are captured]
