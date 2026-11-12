---
name: integrate-docs
description: "Use when the user provides documentation, notes, handbooks, policy PDFs, or office-admin files to integrate into facts, rules, and MyRole.txt."
disable-model-invocation: false
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, filing tree, supply min list, license tracker, or similar
- Operator wants this Expert to absorb how *this* office already works

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

**Facts:** calendar export location, week start, supply mins, filing tree, license tracker, visitor sheet, mail log, vendor list, retention schedule.

**Rules:** never invent a vendor, never move money, never assign an owner, calendar from their file, handbook PDF wins.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by office-operations domains (Calendar & week, Mail, Supplies, Meetings, Licenses, Keys, Visitors, Vendors, Retention). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each rule, ask **Triggers:** (`none`, `write:doc`, or `write:csv`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to operations files. Rules must include a `**Triggers:**` line. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate the trigger index

After adding or retagging any rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

- Single correction → **remember**
- Elevate a Work Item note → **promote-facts-rules**
