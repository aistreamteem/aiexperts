---
name: integrate-docs
description: "Use when the user provides documentation, notes, handbooks, policy PDFs, or grant/donor file guides to integrate into facts, rules, and MyRole.txt."
disable-model-invocation: false
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, gift-acceptance policy, grant calendar, ack template, or similar
- Operator wants this Expert to absorb how *this* office already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared pair only. Do not invent developer or incident-response memory files. Route `Workflows: all` to shared.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** board-packet page list, grant calendar location, ack template path, donor CSV columns, restricted-fund sheet, minutes folder layout.

**Rules:** never invent a restriction code, never give a deductibility opinion, never move money, never submit in a funder portal, calendar from their file, handbook PDF wins.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by nonprofit-office domains (Board & minutes, Grants & awards, Donors & acknowledgments, Restricted funds & in-kind). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** `none` | `write:doc` | `write:csv`.

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to the shared pair. Rule entries must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Trigger index

After adding or retagging any rule whose Triggers is not `none`, regenerate with `python scripts/memory/build_trigger_index.py`.

## Complements

- Single correction → **remember**
- Elevate a Work Item note → **promote-facts-rules**
