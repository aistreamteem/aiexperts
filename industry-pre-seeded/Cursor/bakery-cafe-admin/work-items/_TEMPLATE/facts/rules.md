# Work Item Rules

Rules are constraints for this bake date, wholesale day, cake board, or receiving ticket.

**Format:**

```
### YYYY-MM-DD: [Label/Title]
**Scope:** work-item
**Triggers:** none | write:sheet | write:pack | file:intake
**Captured:** YYYY-MM-DD
**Source:** [operator, bake sheet path, invoice PDF, etc.]
**Status:** [active | promoted-to-expert | archived]

**Rule:** [What must / must not happen]
```

Work Item-level rules do not need a `**Workflows:**` field — they inherit this Work Item’s job.

For Expert Role rules, append to `facts/rules-shared.md` (`Workflows: all`) or `facts/rules-operations.md` (job-tagged). See `facts/MEMORY-INDEX.md`.

---

[Rules will be added here as they are captured during this job]
