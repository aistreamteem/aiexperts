---
name: integrate-docs
description: "Use when the user provides documentation, notes, handbook excerpts, checklists, or HR file guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, new-hire checklist, I-9 index notes, PTO policy excerpt, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared pair only. Do not create developer or incident-response memory files. `Workflows: all` routes to the shared pair.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** checklist row names, live handbook PDF location, I-9 index columns, PTO sheet banks, poster index, offboard remaining-task labels.

**Rules:** never invent a start date, never fire, never copy SSNs, their checklist wins, ask when an I-9 section date is blank.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by HR-admin domains (Applicant files, New-hire packets, I-9 completeness, Handbook/posters, PTO/training, Offboard process, Legal/privacy limits). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask **Triggers:** `none` | `write:doc` | `write:csv`.

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to the shared files. Rule format must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Trigger index

If any new or retagged rule has Triggers other than `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
