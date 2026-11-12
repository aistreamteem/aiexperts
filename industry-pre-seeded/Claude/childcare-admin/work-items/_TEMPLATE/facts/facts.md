# Work Item Facts

Facts are observations specific to this job (this date, room, child, or period). They inform the pack but are not Expert Role rules.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [export name, operator, …]
**Status:** [active | promoted-to-expert | archived]

[Content]
```

Work Item facts do not need a `**Workflows:**` field — they inherit this Work Item’s registered job.

Expert Role facts live in `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md` (job-specific).

---

[Facts will be added here as they are captured during this job]
