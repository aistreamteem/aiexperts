---
name: integrate-docs
description: "Use when the user provides documentation, notes, facility manuals, auction checklists, or PMS export guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, fee schedule, auction checklist, hours memo, or similar
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

**Facts:** hours file location, required move-in forms, auction checklist items, rate-sheet columns, waitlist order field, occupancy status codes, late-export columns.

**Rules:** never invent a fee, never lien/auction legal, never store gate codes or PAN, occupancy from export, waitlist order theirs, ask when an agreement is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by storage-office domains (Unit mix & rates, Occupancy, Move-in packets, Late lists, Auction files, Waitlists, Photos, Transfers). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each rule, ask **Triggers:** (`none`, `write:doc`, or `write:csv`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to operations files. Rules must include a `**Triggers:**` line. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate the trigger index

After adding or retagging any rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
