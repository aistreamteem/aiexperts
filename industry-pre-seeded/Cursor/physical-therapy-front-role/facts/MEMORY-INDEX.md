# Memory System Index

Quick navigation for this physical-therapy front-role expert. Load only the operations files unless a Work Item has its own facts/rules.

---

## Two axes: browsing and triggers

1. **Workflow axis** (this file) — which memory files to load for the current PT front-role job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing via `.cursor/hooks/inject_rules_on_action.py` and generated `trigger-index.json`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` — never hand-edit them; regenerate after adding or retagging a rule.

Day-to-day role memory is the operations pair only.

---

## Pre-seeded role

**Role title:** Physical therapy front role (not the therapist)

**Seed id:** `physical-therapy-front-role`

**Work-item method:** `docs/role/work-item-method.md`

### Operations (this role)

**When to use:** Normal work for this PT front role (day list, remaining visits from file, visit-count check, referral/POC, recert, HEP print, no-show, wait list, day close).

**Load these files:**

- [facts-operations.md](facts-operations.md) — day list, remaining visits, referral/POC, recert, HEP, no-show, wait list, day close, PHI minimums, filing
- [rules-operations.md](rules-operations.md) — no treat, no diagnosis, remaining from file, quote the screenshot, one item one folder, label guesses

**Typical jobs and what to skim first:**

| Job | Fact topics to skim |
| --- | --- |
| day-list | Day list, therapist column, duration, eval vs follow, double-book, HIPAA min |
| auth-remaining-from-file | Remaining from file, visits used, visits authorized, auth number, eligibility |
| visit-count-export-check | Unit count as their export, remaining from file, visits used |
| referral-poc-completeness | Referral in, plan of care as present, physician signature, POC expire |
| recert-dates | Recert date as file, POC expire, referral expire |
| hep-print-index | HEP PDF as their library, home-program print |
| no-show-list | No-show as their codes, cancel as their status, cancel policy |
| wait-list | Wait list, cancel wait-fill |
| day-close | Day-close tender, copay posted |

There is no developer or production-incident memory on this Expert. Do not look for those split files.

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
3. If a Work Item is active, also load `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md`.
4. Follow rules. Facts inform the work.

**Maintenance:** When adding facts/rules, append to the operations files. For health metrics see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
