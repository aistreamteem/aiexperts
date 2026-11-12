---
name: integrate-docs
description: "Use when the user provides documentation, notes, exports, or runbooks to integrate into shared facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Fold operator notes into this mortgage-processor Expert (facts, rules, role).

**When to use:** They drop a conditions-export legend, stacking order, LOS status words, or similar.

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional pointer in `facts/MEMORY-INDEX.md`
- `MyRole.txt` update only if a new repeating job appears
- Summary of what was integrated

## Behavior

1. Ask for document paths and whether they are facts (how this shop works) or rules (must / never).
2. Extract processor content: conditions codes, PTD/PTF labels, document-type names, date-stamp sources, what must never be invented (rate, lock, DTI, CTC).
3. Classify and confirm with the operator. Default **Workflows:** `all`, or a registered job (`conditions-checklist`, `missing-docs`, …). For rules, also ask **Triggers:** `write:csv` | `write:pack` | `write:doc` | `none`.
4. Format entries like existing shared memory:

```markdown
### YYYY-MM-DD: Short label
**Scope:** expert-role
**Workflows:** all | conditions-checklist | …
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** <document path>
**Status:** active

**Rule:** …
```

5. Route **only** to shared memory files. For a large reference (~50+ lines), add `facts/<topic>.md` and a MEMORY-INDEX pointer.
6. Detect duplicates and conflicts; ask which is right before overwriting. After adding or retagging a rule whose trigger is not `none`, regenerate the trigger index: `python scripts/memory/build_trigger_index.py`.
7. Summarize paths added. If a new repeating job appeared, propose a workflow file + registry entry.

Forward actions after a verified note: **remember** (already stored here), or start a Work Item and **continue** the matching job. Not software design.
