---
name: integrate-docs
description: "Use when the user provides documentation, notes, kennel handbooks, or boarding-software export guides to integrate into facts, rules, and MyRole.txt."
disable-model-invocation: false
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, intake checklist, vaccine-page list, capacity memo, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared pair only. Do not create developer or incident-response memory files. Route `Workflows: all` to `facts-shared` / `rules-shared`.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** capacity file location, required vaccine pages, waiver version, feeding-sheet columns, pickup-list fields, waitlist order field, boarding-card packet contents.

**Rules:** never invent a fee, never diagnose, never decide a vaccine is due, never release a dog, feeding as written, ask when a rabies page is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by daycare/boarding domains (Occupancy & boarding cards, Vaccines & waivers, Feeding & meds as written, Pickup authorization, Capacity & waitlist, Incidents). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For rules, ask **Triggers:** (`none` | `write:doc` | `write:csv`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to `facts/facts-shared.md` / `facts/rules-shared.md`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Trigger index

If any promoted or new rule has Triggers other than `none`, regenerate with `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
