# Memory System Index

Quick navigation for this **Veterinary front role** Expert. Load only what the current pack needs.

---

## Two axes

1. **Workflow axis** (this file) — which memory files to load for a clinic role job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

---

## This role’s memory

**Role title:** Veterinary front role (not the vet)  
**Seed id:** `veterinary-front-role`

Always load the **shared** pair, then the **operations** pair:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) — `Workflows: all` entries
- [facts-operations.md](facts-operations.md) — appointments, patient vs client, records routing, reminders, estimates, boarding, starter clinic notes
- [rules-operations.md](rules-operations.md) — never diagnose, never invent prices, never triage as a vet, flag emergency words, one Work Item one folder, label guesses

**When to load:** every Work Item for this role.

**Registered role jobs:** `board-dropoff`, `checkout-list`, `day-appointments`, `emergency-flag`, `estimate-from-prices`, `new-client-forms`, `records-in`, `records-out`, `reminder-list`.

This expert does **not** load developer or production-incident memory files. Those are not this role.

### Work Item memory

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Job-specific notes (this day’s PIMS export quirks, this packet layout). Promote into shared or operations when the operator agrees.

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | day-appointments | records-out | …
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | day-appointments | …
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-shared.md` + `rules-shared.md`, then `facts-operations.md` + `rules-operations.md`.
3. Load the active Work Item facts/rules if present.
4. Follow the selected workflow file under `.claude/workflows/`.

**Maintenance:** when adding a new topic, add a pointer here if operators would not find it from the headings alone. Run the memory-optimize analyze script when files grow quickly.
