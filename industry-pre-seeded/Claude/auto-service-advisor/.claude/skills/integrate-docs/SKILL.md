---
name: integrate-docs
description: "Use when the user provides shop documentation, notes, MPI forms, labor-guide exports, or RO policy sheets to integrate into facts, rules, and MyRole.txt."
disable-model-invocation: false
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role memory and, when needed, `MyRole.txt`.

**When to use:**
- Operator provides shop notes, DMS exports, MPI form instructions, labor-guide policy, or similar
- Operator wants this role to match *this* shop, not only starter notes

**Outputs:**
- New facts in `facts/facts-shared.md` or `facts/facts-operations.md`
- New rules in `facts/rules-shared.md` or `facts/rules-operations.md`
- Optional tool stubs under `docs/tools/`
- Optional pointer in `facts/MEMORY-INDEX.md`
- Optional `MyRole.txt` / workflow updates if they named a new repeating job
- Summary of what was integrated

> **Memory model:** Shared pair for `Workflows: all`; operations pair for RO-job detail. Do not route shop knowledge into developer or incident-response files.

## Behavior

### Step 1: Gather Documents

Ask for file path(s) and whether the material is primarily facts (how this shop works) or rules (must/never).

### Step 2: Analyze Content

**Facts:** labor guide they use, MPI form name, auth capture method, parts PO process, board status words, pay types.

**Rules:** never invent diagnosis, auth before sold, MPI only from their form, invoice matches last auth, no card numbers.

**Role/workflow updates:** a new repeating job that should be registered under `.claude/workflows/`.

### Step 3: Classify

Present the proposed facts/rules in shop language. Ask which apply to every RO (`all` → shared) vs this document only (then use **remember** at Work Item scope instead). For each rule, ask whether it needs a tool-action trigger (`write:doc`) or `none`.

### Step 4: Integrate

1. Read existing shared and operations files; flag duplicates and conflicts (**operator-qa**).
2. Append new entries with `### YYYY-MM-DD: Title`, source attribution, and `**Workflows:** all` (shared) or operations as classified. Rules must include `**Triggers:**`.
3. Update MEMORY-INDEX if a new browse topic appears.
4. Propose MyRole/registry changes if they described a new role job.
5. Regenerate the trigger index: `python scripts/memory/build_trigger_index.py`.

### Step 5: Summary

List paths, counts, conflicts, and next step (often: run a real RO pack with **continue**).

## Complements

- **remember**: one fact/rule during chat
- **promote-facts-rules**: Work Item → Expert Role
- **operator-qa**: verify wording before persisting
