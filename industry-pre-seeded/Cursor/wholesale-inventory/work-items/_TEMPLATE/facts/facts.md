# Work Item Facts

Facts are observations specific to this inventory job (this receipt, count date, pick, transfer, RMA, or reorder pull). They inform the list or match. They are not Expert Role rules.

**Format:**

```
### YYYY-MM-DD: [Label]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [operator, export, PDF]
**Status:** [active | promoted-to-expert | archived]

[Content]
```

Work Item facts do not need a `**Workflows:**` field.

For Expert Role facts use `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md` with a registered job id.

---

[Facts will be added here as this job runs]
