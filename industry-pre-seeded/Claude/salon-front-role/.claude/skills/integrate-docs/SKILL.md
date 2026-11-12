---
name: integrate-docs
description: "Use when the user provides documentation, notes, salon SOPs, booking/POS export guides, or policy files to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, hours memo, menu PDF notes, no-show policy, booth roster legend, or similar
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

**Facts:** hours file location, menu columns, POS close report name, gift-card ID style, retail par sheet, booth vs employee roster labels.

**Rules:** never invent a fee or price, never blast clients, never mix booth and employee closes, never store card numbers, hours file wins, ask when a provider role is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by salon-role domains (Book & hours, Reminders & waitlist, Menu vs ticket, No-shows, Closeout & tenders, Gift cards, Retail vs backbar, Booth vs employee). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** (`write:doc`, `write:csv`, or `none`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to operations files. Rules must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate trigger index

After adding or retagging any rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

**remember** for one correction. **promote-facts-rules** to elevate a Work Item note. **operator-qa** before persisting uncertain notes.
