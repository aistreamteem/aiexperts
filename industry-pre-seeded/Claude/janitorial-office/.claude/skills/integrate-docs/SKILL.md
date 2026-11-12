---
name: integrate-docs
description: "Use when the user provides documentation, notes, runbooks, or contract/process exports to integrate into operations facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role operations memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, site list notes, par sheet legend, SDS index guide, or similar
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

**Facts:** site columns, schedule codes, par/min fields, SDS chemical names, quality form sections, complaint statuses, key-id fields, holiday calendar location.

**Rules:** never invent a mix, never invent a min, never store alarm codes/PINs, never stamp OSHA, ask when the site or SDS row is missing, quote complaints as typed.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by office domains (Sites & night board, Supplies & SDS, Quality & photos, Complaints & missed service, Keys & holidays, Extra-work auth). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** (`none` | `write:file` | `write:sheet` | `write:doc`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to operations files. Rules must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Regenerate trigger index

If any rule was added or retagged with a non-`none` trigger, run `python scripts/memory/build_trigger_index.py`.

### Step 6: Summary

List what was added. Do not treat starter public practice as this office’s policy unless they said it is.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
