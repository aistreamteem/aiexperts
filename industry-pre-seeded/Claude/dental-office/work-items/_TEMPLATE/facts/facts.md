# Work Item Facts

Facts are observations, data points, and context specific to this Work Item (this clinic day, claim pack, or export). They inform the role job but are not office-wide rules.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [operator, filename, chat]
**Status:** [active | promoted-to-expert | archived]

[Content]
```

Work Item-level facts do NOT need a `**Workflows:**` field — they inherit this job.

For Expert Role-level facts use `facts/facts-operations.md`:

```
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** all
**Captured:** YYYY-MM-DD
**Source:** [Optional]

[Content]
```

---

[Facts will be added here as they are captured during this Work Item]
