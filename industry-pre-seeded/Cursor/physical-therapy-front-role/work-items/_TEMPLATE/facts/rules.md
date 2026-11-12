# Work Item Rules

Rules are constraints and procedures that MUST be followed during this Work Item. Log violations in the journal.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [Optional]
**Status:** [active | promoted-to-expert | archived]
**Triggers:** none

**Rule:** [statement]
```

Work Item-level rules do NOT need a `**Workflows:**` field — they inherit this job.

For Expert Role-level rules use `facts/rules-operations.md`:

```
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** [Optional]

**Rule:** [statement]
```

---

[Rules will be added here as they are captured during this Work Item]
