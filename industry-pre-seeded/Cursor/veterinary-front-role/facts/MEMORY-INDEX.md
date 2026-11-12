# Memory System Index

Quick navigation for this **Veterinary front role** expert. Load shared memory for role work. Do not load developer or incident-response files for this role — they are not the live memory.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which shared entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most clinic-role rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Shared (this role)

**When to use:** Any veterinary front-role Work Item (day appointments, emergency flag, new-client forms, records in/out, reminders, estimates, checkout, boarding drop-off).

**Load these files:**

- [facts-shared.md](facts-shared.md) — appointments, patient vs client, records routing, reminders, price file, boarding notes, privacy
- [rules-shared.md](rules-shared.md) — no diagnosis, no triage as vet, prices from file, one item one folder, label guesses, emergency words first

**Typical jobs and what to skim first:**

| Job | Fact topics to skim |
| --- | --- |
| day-appointments | Appointments, appointment type, hours, emergency, species, one-day book |
| emergency-flag | Emergency wording, after-hours list, route urgent, no triage |
| new-client-forms | New client forms, patient vs client, photo policy, authorized agent |
| records-in | Records route, lab file, image file, no lab read |
| records-out | Records route, authorization, no withhold, least client data |
| reminder-list | Reminders, vaccine due, client comm pref, deceased flag |
| estimate-from-prices | Price file, estimate, estimate auth, no add line |
| checkout-list | Invoice from export, payment at role, no pay, open invoices |
| board-dropoff | Boarding notes, boarding meds, boarding as written, pickup window |

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | day-appointments | emergency-flag | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | day-appointments | emergency-flag | ...
**Triggers:** none | write:doc | write:csv
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

Work Item facts/rules live under `work-items/<id>/facts/` and do not need a `Workflows:` field.

---

## Usage

1. Always load this index first.
2. Load `facts-shared.md` + `rules-shared.md`.
3. If a Work Item is active, also load its `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md`.
4. Filter Expert Role entries to `all` or the current registry id.

**Maintenance:** New shop knowledge goes in the shared pair. If a new high-value scenario appears (5+ similar questions), add a line here.

---

## Pre-seeded role

**Role title:** Veterinary front role (not the vet)

**Seed id:** `veterinary-front-role`

Day-to-day role memory is the **shared** pair above. Starter entries are typical US veterinary front-role practice until the operator corrects them.
