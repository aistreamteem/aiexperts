---
name: integrate-docs
description: "Use when the user provides documentation, notes, receiving SOPs, count procedures, or WMS export guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared/operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a receiving SOP, count procedure, item-master field list, bin map notes, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md` (job-scoped)
- New rules in `facts/rules-shared.md` (`Workflows: all`) or `facts/rules-operations.md` (job-scoped)
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared + operations. Do not create developer or incident-response memory files. Route `Workflows: all` to shared; named registry ids to operations.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** on-hand export columns, min/max fields, recount threshold, freeze window, bin-map location, lot/expiry column names, RMA condition codes.

**Rules:** never invent qty, never silent-adjust, blind means hide book, one warehouse unless asked, UOM check before add, RMA before restock.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by inventory domains (Receiving & putaway, Counts & ABC, Locations & bins, Lots & expiry, Reorder, Pick/pack, Transfers, RMA, Owner/consignment). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask `**Triggers:**` (`write:csv`, `write:pack`, `write:doc`, or `none`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to shared (`all`) or operations (named job). Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Trigger index

If any promoted or imported rule has Triggers other than `none`, regenerate with `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
