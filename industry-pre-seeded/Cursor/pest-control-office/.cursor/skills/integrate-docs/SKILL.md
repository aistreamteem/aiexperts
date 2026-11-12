---
name: integrate-docs
description: "Use when the user provides documentation, notes, route SOPs, chemical-log field lists, or export guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, route SOP, required-log-field list, WDO form checklist, or similar
- Operator wants this Expert to absorb how *this* shop already works

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

**Facts:** route-file location, required chemical-log fields, skip labels, callback vs warranty coding, bait-map numbering, WDO graph requirement, price-file columns.

**Rules:** never invent a mix or EPA number, never diagnose a structure, never store gate codes, skip list wins, ask when a ticket is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by pest-office domains (Routes & skips, Tickets & callbacks, Chemical logs & inventory, Bait maps & devices, WDO/termite packs, Estimates, Safety flags). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** `none` | `write:doc` | `write:csv`.

### Step 4: Format and route

Append dated entries to operations files using `### YYYY-MM-DD: Title`. Rule entries must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate the trigger index

If any rule with a non-`none` trigger was added or retagged, run:

```text
python scripts/memory/build_trigger_index.py
```

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
