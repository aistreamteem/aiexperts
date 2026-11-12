---
name: integrate-docs
description: "Use when the user provides documentation, notes, facility manuals, auction checklists, or PMS export guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, fee schedule, auction checklist, hours memo, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared only. Route `Workflows: all` to the shared pair. Do not create developer or incident-response memory files.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** hours file location, required move-in forms, auction checklist items, rate-sheet columns, waitlist order field, occupancy status codes, late-export columns.

**Rules:** never invent a fee, never lien/auction legal, never store gate codes or PAN, occupancy from export, waitlist order theirs, ask when an agreement is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by storage-office domains (Unit mix & rates, Occupancy, Move-in packets, Late lists, Auction files, Waitlists, Photos, Transfers). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** `none` | `write:doc` | `write:csv`.

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to shared files. Rule format must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate trigger index

If any rule was added or retagged with a non-`none` trigger, run `python scripts/memory/build_trigger_index.py`.

## Complements

**remember** for one-off captures. **promote-facts-rules** to elevate Work Item notes. **memory-optimize** for health checks.
