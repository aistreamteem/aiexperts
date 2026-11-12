# Work Item Rules

Rules are constraints, procedures, and patterns that MUST be followed during this Work Item. They are prescriptive, and violations should be logged in the journal.

**Format:**

```markdown
### YYYY-MM-DD: Label or Title
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** [Optional: user name, URL, chat thread, etc.]
**Status:** [active | promoted-to-expert | archived]

[Content with full formatting preserved]
```

**Note:** Work Item-level rules do NOT need a `**Workflows:**` field. They inherit the Work Item's workflow context.

Expert Role-level rules live in `facts/rules-shared.md` and `facts/rules-<workflow>.md` at the repository root. Their format adds workflow applicability and action triggers:

```markdown
### YYYY-MM-DD: Label or Title
**Scope:** expert-role
**Workflows:** all | developer | [comma-separated list]
**Triggers:** [action token(s) or `none`]
**Captured:** YYYY-MM-DD
**Source:** [Optional]

**Rule:** [statement]

**Why:** [reason]

**How to apply:** [steps]

**Violation:** [consequence]
```

---

Rules will be added here as they are captured during Work Item execution.
