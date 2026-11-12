---
name: integrate-docs
description: "Use when the user provides documentation, notes, CMMS export guides, crib procedures, or plant playbooks to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, PM calendar notes, crib min-max sheet, LOTO index, or similar
- Operator wants this Expert to absorb how *this* plant already works

**Outputs:**
- New facts in `facts/facts-operations.md`
- New rules in `facts/rules-operations.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Operations only. Do not create developer or incident-response memory files.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** WO CSV columns, PM interval file location, crib min-qty columns, downtime codes, craft list, LOTO PDF folder, warranty-end field.

**Rules:** never invent an interval, never invent a min, never OSHA-stamp, never hide downtime, ask when the asset is missing, quote the completion note as typed.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by maintenance domains (Work orders & dispatch, PM calendar, Parts crib, Downtime, Safety forms, Contractors & warranty). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** (`none` | `write:doc` | `write:csv`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to operations files. Rules must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Regenerate trigger index

If any rule was added or retagged with a non-`none` trigger, run `python scripts/memory/build_trigger_index.py`.

### Step 6: Summary

List what was added. Do not treat starter public practice as this plant’s policy unless they said it is.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
