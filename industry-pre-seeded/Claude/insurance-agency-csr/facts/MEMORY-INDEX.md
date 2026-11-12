# Memory System Index

Quick navigation for this **Insurance agency CSR (not the producer)** expert. Load operations memory for role work. Do not load developer or incident-response files for this role — they are not the live memory.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which operations entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most CSR rules use `Triggers: none` (judgment / ask). Vocabulary: `write:doc`, `write:csv` (no `config:change`). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Operations (this role)

**When to use:** Any insurance-agency CSR Work Item (certificates, ACORD completeness, endorsements, expirations, FNOL routing, missing decs, vehicle-add paperwork, and the other registered jobs).

**Load these files:**

- [facts-operations.md](facts-operations.md) — named insured, dec pages, COI requests, holders, ACORD completeness, FNOL routing, expirations, endorsements, starter shop notes
- [rules-operations.md](rules-operations.md) — never bind, never quote as a stamp, never invent limits/VINs/class codes/premiums, never say covered, one Work Item one folder, label guesses

**Typical jobs:** see `.claude/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | acord-completeness | coi-request-pack | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | acord-completeness | coi-request-pack | ...
**Triggers:** none | write:doc | write:csv
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-operations.md` + `rules-operations.md`.
3. Load the active Work Item `facts/` and `rules/` if present.
4. Filter Expert Role entries to `all` or the current registry id.

**Maintenance:** New shop knowledge goes in the operations pair. If a new high-value scenario appears (5+ similar questions), add a line here.

---

## Pre-seeded role

**Role title:** Insurance agency CSR (not the producer)

**Seed id:** `insurance-agency-csr`

Day-to-day role memory is the **operations** pair above. Starter entries are typical US independent-agency CSR practice until the operator corrects them.
