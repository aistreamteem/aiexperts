# Memory System Index

Quick navigation for this dental front-role expert. Load only the operations files unless a Work Item has its own facts/rules.

---

## Two axes: browsing and triggers

1. **Workflow axis** (this file) — which memory files to load for the current dental-role job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing via `.claude/hooks/inject_rules_on_action.py` and generated `trigger-index.json`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `py -3 scripts/memory/build_trigger_index.py` — never hand-edit them; regenerate after adding or retagging a rule.

Day-to-day role memory is the operations pair only.

---

## Pre-seeded role

**Role title:** Dental office (not the dentist)

**Seed id:** `dental-office`

**Work-item method:** `docs/role/work-item-method.md`

### Operations (this role)

**When to use:** Normal work for this dental front role (day list, forms, eligibility notes, claims fields, preauth, EOB index, recall, broken list, day close).

**Load these files:**

- [facts-operations.md](facts-operations.md) — scheduling, insurance paperwork, recall, intake forms, PHI minimums, filing
- [rules-operations.md](rules-operations.md) — no diagnosis, no CDT choice, quote the screenshot, one item one folder, label guesses

**Typical jobs and what to skim first:**

| Job | Fact topics to skim |
| --- | --- |
| day-list | Day sheet, chair, provider, confirmation, blocks/huddle, emergency slot, privacy |
| forms-check | Intake forms, medical history, consents, NPP ack, signatures |
| eligibility-notes | Eligibility, benefit year, frequency limits, member/group, subscriber vs patient |
| claims-fields | Claim form fields, attachments present, tooth/surface labels, date of service |
| preauth-fields | Predetermination, attachments named, no invented preauth number |
| eob-index | EOB file, patient portion, adjustments, claim status |
| recall-list | Recall, preferred contact, office hours |
| broken-list | Broken appointments, wait list (as their file), their broken policy |
| day-close | Production vs collection, day-close tender, fee schedule file |

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all
**Triggers:** write:doc | write:csv | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

Work Item facts/rules live under `work-items/<id>/facts/` and do not need a `Workflows:` field.

---

## Usage

1. Always load this index first.
2. Load `facts-operations.md` + `rules-operations.md`.
3. If a Work Item is active, also load its `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md`.
4. Follow rules. Facts inform the work.

**Maintenance:** When adding facts/rules, append to the operations files. For health metrics see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
