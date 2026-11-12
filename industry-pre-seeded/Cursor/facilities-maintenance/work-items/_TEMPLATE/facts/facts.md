# Work Item Facts

Facts are observations and context specific to this maintenance job (this work order, dispatch day, PM week, crib pull, or downtime period). They are not shop-wide until promoted.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [operator, export name, chat]
**Status:** [active | promoted-to-expert | archived]

[Content]
```

Work Item facts do not need `**Workflows:**` — they inherit this Work Item’s registry job.

Expert Role facts live in `facts/facts-operations.md`.

---

[Facts will be added here as they are captured]
