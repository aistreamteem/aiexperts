# Work Item Rules

Rules are constraints, procedures, and patterns that MUST be followed during this office-operations Work Item. They are prescriptive and violations should be logged in the journal.

**Format:** see `facts/MEMORY-INDEX.md` (use `### YYYY-MM-DD: Title`).

```markdown
### YYYY-MM-DD: Label/Title
**Scope:** work-item
**Captured:** YYYY-MM-DD
**Source:** operator, file name, or chat
**Status:** active

**Rule:** statement
```

Work Item-level rules do not need a `**Workflows:**` field — they inherit the Work Item's workflow context.

Expert Role-level rules go in `facts/rules-operations.md` and must include:

```markdown
### YYYY-MM-DD: Label/Title
**Scope:** expert-role
**Workflows:** all | weekly-pack | meeting-pack | registry-id
**Triggers:** none | write:doc | write:csv
**Captured:** YYYY-MM-DD
**Source:** optional
**Status:** active

**Rule:** statement
```

---

[Rules will be added here as they are captured during Work Item execution]
