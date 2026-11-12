# Work Item Facts

Facts are observations, data points, and contextual information specific to this Work Item. They inform design and implementation decisions but are not prescriptive.

**Format:**

```markdown
### YYYY-MM-DD: Label or Title
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [Optional: user name, URL, chat thread, etc.]
**Status:** [active | promoted-to-expert | archived]

[Content with full formatting preserved]
```

**Note:** Work Item-level facts do NOT need a `**Workflows:**` field. They inherit the Work Item's workflow context.

Expert Role-level facts live in `facts/facts-shared.md` and `facts/facts-<workflow>.md` at the repository root. Their format adds workflow applicability:

```markdown
### YYYY-MM-DD: Label or Title
**Scope:** expert-role
**Workflows:** all | developer | production-incident | [comma-separated list]
**Captured:** YYYY-MM-DD
**Source:** [Optional]

[Content]
```

---

Facts will be added here as they are captured during Work Item execution.
