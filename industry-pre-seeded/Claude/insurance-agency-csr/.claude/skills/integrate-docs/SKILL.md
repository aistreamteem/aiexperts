---
name: integrate-docs
description: "Use when the user provides documentation, notes, agency procedures, AMS export guides, or form checklists to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, AMS procedure, required-forms list, holder-library note, or similar
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

**Facts:** AMS export location, required ACORD set, COI form they use, holder-list columns, expiration CSV fields, FNOL routing contact file.

**Rules:** never invent a limit, never bind, never say covered, never copy full FEIN, their export wins, ask when a form is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by CSR domains (Certificates & holders, ACORD & applications, Endorsements & vehicle adds, Expirations & renewals, FNOL routing, Dec pages, Producer vs CSR limits). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** (`none` | `write:doc` | `write:csv`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to operations files. Rules must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate trigger index

If any new or retagged rule has Triggers other than `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
