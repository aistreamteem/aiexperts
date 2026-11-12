---
name: integrate-docs
description: "Use when the user provides documentation, notes, client rule files, rate cards, or staffing playbooks to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a client rule file, rate card notes, orientation checklist, holiday calendar, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared Expert Role memory only. Do not create developer or incident-response memory files.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** assignment status words, tracked credential types, fill-rate formula, holiday calendar location, timesheet period, orientation ack list, DNS/DNR scope labels.

**Rules:** never invent a rate or markup, never fire, never copy SSNs, ask when a timesheet or credential date is missing, DNS flags from their file only.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by staffing-office domains (Assignments & orders, Credentials & orientation, Timesheets & rates, DNS/DNR, Holidays, Incidents, Legal/privacy limits). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** (`none` | `write:doc` | `write:csv`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to `facts/facts-shared.md` / `facts/rules-shared.md`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate trigger index

If any new or retagged rule has Triggers other than `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

**remember** for one correction. **promote-facts-rules** to elevate a Work Item note. **operator-qa** to verify wording first.
