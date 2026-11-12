---
name: integrate-docs
description: "Use when the user provides documentation, notes, banquet playbooks, BEO samples, or house checklists to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, BEO sample notes, COI checklist, labor sheet, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared pair only. Do not create developer or incident-response memory files. Route `Workflows: all` to the shared pair.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** BEO numbering, hold vs definite codes, COI additional-insured wording, guarantee due-date field, diagram revision labels, load-in dock hours, banquet-check signer.

**Rules:** never invent a rate or F&B minimum, never serve as the liquor license, never stamp fire occupancy, never store PAN, ask on missing COI, counts from guarantee.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by venue domains (Holds & definite, BEO & menu, Guarantee & setup, COI & insurance, Diagrams, Load-in, Banquet check, Group rooms). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each rule, ask **Triggers:** `none` | `write:doc` | `write:csv`.

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to the shared files. Rules must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Trigger index

If any rule was added with a non-`none` trigger, regenerate with `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
