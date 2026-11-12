# Work Item Facts

Facts are observations specific to this loan pack (this loan number, this export, this guessed document type). They inform the checklist. They are not Expert Role rules.

**Format:**

```
### YYYY-MM-DD: [Label]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [operator, LOS export, PDF folder]
**Status:** [active | promoted-to-expert | archived]

[Content]
```

Work Item facts do not need a `**Workflows:**` field.

For Expert Role facts use `facts/facts-operations.md` with `**Workflows:** all` or a registered job id.

---

[Facts will be added here as this pack runs]
