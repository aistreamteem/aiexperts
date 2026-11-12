# Memory System Index

Quick navigation for this **Fleet / delivery dispatcher** Expert. Load only what the current pack needs.

---

## Two axes

1. **Workflow axis** (this file) — which memory files to load for a dispatch job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

---

## This role’s memory

**Role title:** Fleet / delivery dispatcher  
**Seed id:** `fleet-dispatcher`

Always load the **shared** pair, then the **operations** pair:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) — `Workflows: all` entries
- [facts-operations.md](facts-operations.md) — roster, routes, DVIR, POD, ELD/GPS, fuel, exceptions, how we file packs
- [rules-operations.md](rules-operations.md) — do not invent GPS/ETA/POD/DVIR; ask when missing; one day / one unit / one folder; flag don’t accuse; secrets stay out

**When to load:** every Work Item for this role.

**Typical jobs:** see `.claude/workflows/` and `docs/role/work-item-method.md` (intake → assignment → routes → DVIR → exceptions → POD → file questions → accepted pack).

There is no software-developer or incident-response memory on this Expert.

### Work Item memory

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Job-specific (this service date’s board, this unit’s exception codes). Promote into shared or operations when the operator agrees.

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | assignment-pack | todays-routes | dvir-gap | exceptions | breakdown | detention | pod-check | hos-questions | fuel-outliers
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | assignment-pack | …
**Triggers:** write:doc | write:csv | write:pack | none
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
