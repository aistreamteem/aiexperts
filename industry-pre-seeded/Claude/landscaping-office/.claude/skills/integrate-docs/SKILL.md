---
name: integrate-docs
description: "Use when the user provides documentation, notes, exports, or shop packets to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Fold dropped shop documents into this landscaping-office Expert (shared facts/rules and, if needed, MyRole / workflow stubs).

**When to use:** Operator provides a packet, policy PDF, price-file legend, HOA spec notes, or similar — not a one-line "remember this" (use **remember** for that).

## Memory model

Write Expert Role entries to:

- `facts/facts-shared.md`
- `facts/rules-shared.md`

`**Workflows:**` = `all` or registry ids. Large reference material may be `facts/<topic>.md` plus a MEMORY-INDEX pointer. Write only shared memory for this role.

## Behavior

1. Ask for path(s) and whether the packet is mostly facts or rules.
2. Read the documents. Extract:
   - **Facts:** how this shop files routes, which columns they use, equipment names they listed
   - **Rules:** never invent a wage, skip list wins, weather they call
   - **Role/workflow:** a new repeating job that is not in the registry
3. Show classification. Ask workflow applicability (default `all`; examples: price-file legend → `estimate-from-price`, skip policy → `crew-day, route-pack`). For each rule, ask **Triggers** (`write:doc`, `write:sheet`, or `none`).
4. Format dated entries with `### YYYY-MM-DD: Title`. Preserve wording. Source = document path. Rules include a `**Triggers:**` line.
5. Check shared memory files for duplicates/conflicts; ask if they clash.
6. Append. Update MEMORY-INDEX if a new topic. For rules with a non-`none` trigger, run `python scripts/memory/build_trigger_index.py`. Propose MyRole / workflow updates only if a new role job appeared.
7. Summarize what was added.

## Guidelines

Prefer facts when ambiguous. Flag conflicts. Never copy gate codes, passwords, or card numbers into memory. Starter vs *this* shop: label guesses.

**Complements:** **remember** (one item during chat), **promote-facts-rules** (Work Item → Expert Role).
