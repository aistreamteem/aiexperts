# Work Item Rules

Rules are constraints that MUST be followed on this RO / pack. Log violations in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** [Optional]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]
```

**Note:** Work Item-level rules do NOT need a `**Workflows:**` field — they inherit this Work Item's role job. Keep `**Triggers:**` so promoted rules stay hook-ready.

For Expert Role-level rules use `### YYYY-MM-DD: Title`. `Workflows: all` → `facts/rules-shared.md`; shop job detail → `facts/rules-operations.md`. Trigger vocabulary for this role: `none` or `write:doc`.

[Rules will be added here as they are captured during this Work Item]
