# Memory System Index

Quick navigation for this **Real estate transaction coordinator** Expert. Load only what the current pack needs.

---

## Two axes

1. **Workflow axis** (this file) — which memory files to load for a TC job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

---

## This role’s memory

**Role title:** Real estate transaction coordinator  
**Seed id:** `real-estate-transaction-coordinator`

Day-to-day memory is the **operations** pair:

- [facts-operations.md](facts-operations.md) — contract dates, disclosures, HOA, inspection/repair, title as routing, closing completeness, wire-fraud process, starter shop notes
- [rules-operations.md](rules-operations.md) — must-nevers, labeled guesses, no legal advice, no wire instructions, one transaction per folder

**When to load:** every Work Item for this role.

**Typical jobs:** see `.cursor/workflows/` and `docs/role/work-item-method.md` (intake → index → dates / missing docs / checklists → pack).

There is no software-developer or incident-response memory on this Expert. Use the operations pair only.

### Work Item memory

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Job-specific (this transaction’s HOA packet checklist, this file’s guessed disclosure label). Promote into operations when the operator agrees.

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | dates-calendar | missing-docs | …
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | dates-calendar | …
**Triggers:** write:csv | write:checklist | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-operations.md` + `rules-operations.md`.
3. Load the active Work Item facts/rules if present.
4. Follow the selected workflow file under `.cursor/workflows/`.

**Maintenance:** when adding a new topic, add a pointer here if operators would not find it from the operations headings alone. Run `/memory-optimize --metrics` when files grow quickly.
