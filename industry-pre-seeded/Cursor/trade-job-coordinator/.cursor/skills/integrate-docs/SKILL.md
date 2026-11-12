---
name: integrate-docs
description: "Use when the user provides documentation, notes, dispatch SOPs, packing-list templates, or CRM export guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, dispatch SOP, packing-list template, permit log notes, or similar
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

**Facts:** job-id field, packing-list columns, permit-number location, photo types by job type, emergency words, truck-stock vs special-order labels.

**Rules:** never invent SKUs, never claim inspection pass, never store gate codes, packing list before roll, sold before schedule install, ask when a permit number is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by coordinator domains (Board & windows, Parts & packing lists, Permits & locates, Callbacks & warranty, Closeout photos, Safety flags). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** `none` | `write:doc` | `write:csv`.

### Step 4: Format and route

Append dated entries to operations files using `### YYYY-MM-DD: Title` headers (see MEMORY-INDEX). Include `**Triggers:**` on every rule. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate trigger index

If any promoted or imported rule has Triggers other than `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
