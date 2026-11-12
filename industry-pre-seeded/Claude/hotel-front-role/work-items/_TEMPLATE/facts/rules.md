# Work Item Rules

Rules are constraints and procedures that MUST be followed during this Work Item. Log violations in the journal.

**Format:**

```markdown
### YYYY-MM-DD: Label/Title

**Scope:** work-item

**Captured:** YYYY-MM-DD

**Source:** operator name, export filename, or chat

**Status:** active | promoted-to-expert | archived

**Rule:** statement

**Why:** reason
```

Work Item-level rules do not need `**Workflows:**` — they inherit the Work Item’s workflow.

For Expert Role rules use `facts/rules-operations.md` with:

```markdown
**Workflows:** all | [registered job id]
**Triggers:** write:doc | write:csv | none
```

---

[Rules will be added here as they are captured during Work Item execution]
