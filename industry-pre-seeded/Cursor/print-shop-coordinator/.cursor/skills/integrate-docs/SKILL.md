---
name: integrate-docs
description: "Use when the user provides documentation, notes, shop handbooks, ticket-sheet guides, or MIS export notes to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, house preflight checklist, ticket-column guide, mill-order sheet notes, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Operations only. Do not create developer or incident-response memory files.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** ticket-sheet columns, house bleed, proof-type words, stock SKU field, mill-order promise column, bindery-step order, delivery-log fields, reprint-reason codes.

**Rules:** never invent a due, never hide a shortage, never invent Pantone, proof before press unless their rule, ask if the ticket is missing, no mill payment.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by print-shop domains (Tickets & job board, Preflight & proofs, Stock & mill paper, Calendar & dues, Bindery, Delivery, Reprints). Confirm with the operator. Ask workflow applicability (`all` or registry ids).

### Step 4: Format and route

Append dated entries to shared memory files (`facts/facts-shared.md`, `facts/rules-shared.md`). Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
