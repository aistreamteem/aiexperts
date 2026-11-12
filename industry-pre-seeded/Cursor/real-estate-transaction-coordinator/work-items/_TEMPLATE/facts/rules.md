# Work Item Rules

Rules that MUST be followed for this transaction file only. Violations go in the journal.

**Format:**

```
### YYYY-MM-DD: [Label]
**Scope:** work-item
**Triggers:** write:csv | write:checklist | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** [operator]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]
```

Work Item rules do not need a `**Workflows:**` field unless promoting later.

For Expert Role rules use `facts/rules-operations.md`.

---

[Rules will be added here as this pack runs]
