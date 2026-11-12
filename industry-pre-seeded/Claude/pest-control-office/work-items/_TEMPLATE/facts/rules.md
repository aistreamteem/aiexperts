# Work Item Rules

Rules are constraints and procedures that MUST be followed during this Work Item. Log violations in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** [Optional: operator, log sheet, label file]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]
```

Work Item-level rules do NOT need a `**Workflows:**` field — they inherit this pest-office job.

For Expert Role-level rules use `facts/rules-operations.md`:

```
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** all
**Triggers:** write:doc | write:csv | write:pack | none
**Captured:** YYYY-MM-DD
**Source:** [Optional]

**Rule:** [statement]
```

---

[Rules will be added here as they are captured during this route day or pack]
