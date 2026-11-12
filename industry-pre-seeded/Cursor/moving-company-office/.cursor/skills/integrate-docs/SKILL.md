---
name: integrate-docs
description: "Use when the user provides documentation, notes, rate-book memos, dispatch playbooks, or claims-file guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, rate-file memo, materials sheet legend, claims-log naming rule, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared only. Route `Workflows: all` to the shared pair. Do not create developer or incident-response memory files.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** live rate-file location, cube-chart revision, high-value-list rule, claims-log owner, truck-calendar columns, scale-ticket naming.

**Rules:** never invent weight or cube, never pay a crew, never tariff/DOT legal, ask when rate file is missing, scale ticket wins.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by moving-office domains (Estimates & rates, Inventory & cube, Dispatch & crew, Trucks & calendars, Materials, Weigh tickets, Claims routing, Valuation as their form). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** `none` | `write:doc` | `write:csv`.

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to shared files. Rule format must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate trigger index

If any rule was added or retagged with a non-`none` trigger, run `python scripts/memory/build_trigger_index.py`.

## Complements

**remember** for one-off captures. **promote-facts-rules** to elevate Work Item notes. **memory-optimize** for health checks.
