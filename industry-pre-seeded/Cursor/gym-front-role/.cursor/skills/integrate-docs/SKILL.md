---
name: integrate-docs
description: "Use when the user provides documentation, notes, club policy files, membership-system export guides, or role playbooks to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, freeze/cancel policy PDF notes, waiver checklist, price sheet guide, or similar
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

**Facts:** scan-export columns, waiver form names, freeze policy location, PT package menu, class-capacity source, retail SKU sheet.

**Rules:** never invent dues, never run EFT, never interpret PAR-Q, waiver required, hours file beats leftover class, ask when a contract PDF is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by gym-role domains (Check-in & access, Waivers & guests, Freeze & cancel, Failed drafts, Classes & PT, Retail close, Scope limits). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** (`write:doc`, `write:csv`, or `none`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to operations files. Rules include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate the trigger index

If any rule was added or retagged with a non-`none` trigger, run `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
