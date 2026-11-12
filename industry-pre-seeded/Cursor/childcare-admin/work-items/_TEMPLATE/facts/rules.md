# Work Item Rules

Rules that MUST be followed during this job. Violations go in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [Optional]
**Status:** [active | promoted-to-expert | archived]
**Triggers:** write:doc | write:csv | none
**Rule:** [statement]
```

Work Item rules do not need `**Workflows:**` — they inherit this Work Item’s registered job.

Expert Role rules live in `facts/rules-shared.md` (`Workflows: all`) or `facts/rules-operations.md` (job-specific).

---

[Rules will be added here as they are captured during this job]
