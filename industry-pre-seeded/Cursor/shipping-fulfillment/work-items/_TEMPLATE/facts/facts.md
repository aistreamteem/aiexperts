# Work Item Facts

Facts are observations and context specific to this shipping job (this wave, order, truck, day, or RMA batch). They are not shop-wide until promoted.

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

Expert Role facts: `facts/facts-shared.md` for `Workflows: all`, or `facts/facts-operations.md` for a job id.

---

[Facts will be added here as they are captured]
