# Work Item Facts

Facts are observations and context specific to this inventory job (this receipt, count date, pick, transfer, RMA, or reorder pull). They are not shop-wide until promoted.

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

For Expert Role facts use `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md` with a registered job id.

---

[Facts will be added here as they are captured]
