---
name: integrate-docs
description: "Use when the user provides documentation, notes, receiving SOPs, count procedures, or WMS export guides to integrate into shared or operations facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Fold operator notes into this wholesale / inventory Expert (facts, rules, role).

**When to use:** They drop a receiving SOP, count procedure, item-master field list, bin map notes, or similar.

**Outputs:**
- New facts in `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md` (named job)
- New rules in `facts/rules-shared.md` or `facts/rules-operations.md`
- Optional pointer in `facts/MEMORY-INDEX.md`
- `MyRole.txt` update only if a new repeating job appears
- Summary of what was integrated

## Behavior

1. Ask for document paths and whether they are facts (how this shop works) or rules (must / never).
2. Extract inventory content: on-hand export columns, min/max, recount threshold, freeze window, bin map, lot/expiry columns, RMA condition codes, what must never be invented.
3. Classify and confirm with the operator. Default **Workflows:** `all`, or a registered job (`receiving-match`, `cycle-count`, …). For rules, also ask **Triggers:** `write:csv` | `write:pack` | `write:doc` | `none`.
4. Format entries with `### YYYY-MM-DD: Title`, Scope, Workflows, Triggers (rules), Captured, Source, Status.
5. Route `Workflows: all` to the shared pair; named jobs to the operations pair. For a large reference (~50+ lines), add `facts/<topic>.md` and a MEMORY-INDEX pointer.
6. Detect duplicates and conflicts; ask which is right before overwriting. After adding a rule whose trigger is not `none`, regenerate with `py -3 scripts/memory/build_trigger_index.py`.
7. Summarize paths added. If a new repeating job appeared, propose a workflow file + registry entry.

Forward actions after a verified note: **remember** (already stored here), or start a Work Item and **continue** the matching job. Not software design.
