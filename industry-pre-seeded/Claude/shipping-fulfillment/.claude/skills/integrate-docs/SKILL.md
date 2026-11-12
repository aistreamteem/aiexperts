---
name: integrate-docs
description: "Use when the user provides documentation, notes, packing SOPs, carrier routing guides, or WMS export guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared/operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a packing SOP, carton catalog, routing guide, RMA policy, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md` (job ids)
- New rules in `facts/rules-shared.md` or `facts/rules-operations.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared + operations only. Do not create developer or incident-response memory files.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** scale-export columns, carton catalog codes, BOL form name, hold codes, RMA reason codes, carrier roster as their file labels them.

**Rules:** never invent weight/class/DIM, never pay freight, never stamp hazmat, shorts stay visible, ask before void or hold release.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by shipping domains (Pick & wave, Pack & carton, Weights & DIM, BOL & freight docs, Holds & will-call, Exceptions & shorts, Manifest & tracking, RMA & restock). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** (`none` | `write:doc` | `write:csv`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to shared (`Workflows: all`) or operations (job ids). Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Index and triggers

If any rule Triggers is not `none`, regenerate with `python scripts/memory/build_trigger_index.py`.

### Step 6: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

## Complements

**remember** for one-off captures. **promote-facts-rules** to elevate Work Item notes. **memory-optimize** when files grow large.
