# Work Item Facts

Facts are observations specific to this bake date, wholesale day, cake board, or receiving ticket. They are informative, not prescriptive.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [operator, bake sheet path, invoice PDF, etc.]
**Status:** [active | promoted-to-expert | archived]

[Content]
```

Work Item-level facts do not need a `**Workflows:**` field — they inherit this Work Item’s job.

For Expert Role facts, append to `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md` (job-tagged). See `facts/MEMORY-INDEX.md`.

---

[Facts will be added here as they are captured during this job]
