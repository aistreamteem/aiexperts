# Memory System Index

Quick navigation for this **Mortgage processor (file completeness)** Expert. Load only what the current pack needs.

---

## Two axes

1. **Workflow axis** (this file) — which memory files to load for a processor job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

---

## This role’s memory

**Role title:** Mortgage processor (file completeness)  
**Seed id:** `mortgage-processor`

Day-to-day memory is the **shared** pair:

- [facts-shared.md](facts-shared.md) — conditions, present-versus-missing docs, date stamps, third-party files, starter shop notes
- [rules-shared.md](rules-shared.md) — must-nevers, labeled guesses, no underwrite, no CTC, one loan per folder

**When to load:** every Work Item for this role.

**Typical jobs:** see `.claude/workflows/` and `docs/role/work-item-method.md` (intake → index → conditions / missing docs / dates → pack).

There is no software-developer or incident-response memory on this Expert. Use the shared pair only.

### Work Item memory

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Job-specific (this loan’s split gift trail, this file’s guessed document type). Promote into shared when the operator agrees.

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | conditions-checklist | missing-docs | …
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | conditions-checklist | …
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-shared.md` + `rules-shared.md`.
3. Load the active Work Item facts/rules if present.
4. Follow the selected workflow file under `.claude/workflows/`.

**Maintenance:** when adding a new topic, add a pointer here if operators would not find it from the shared headings alone. Run `/memory-optimize --metrics` when files grow quickly.
