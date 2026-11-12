---
name: integrate-docs
description: "Use when the user provides documentation, notes, runbooks, or contract/process exports to integrate into operations facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate documentation into this janitorial-office expert (facts, rules, role definition).

**When to use:** Operator provides shop notes, contract exhibits, par-sheet legends, quality-form instructions, or similar.

**Outputs:**
- `Workflows: all` facts/rules → `facts/facts-shared.md` / `facts/rules-shared.md`
- Job-scoped facts/rules → `facts/facts-operations.md` / `facts/rules-operations.md`
- Large reference material as `facts/<topic>.md` plus a MEMORY-INDEX pointer
- `MyRole.txt` / `docs/role/work-item-method.md` updates if a new repeating role job appears
- Summary of what was integrated

> **Memory model:** Shared + operations. Do not route into software-build or incident-response memory files.

## Behavior

### 1. Gather documents

Ask for path(s) and whether the material is mainly facts or rules.

### 2. Analyze

**Facts:** how this shop names sites, wings, SKUs, callback codes, holiday calendars, where SDS PDFs live.

**Rules:** never invent mix/wage/score; complaints from their log; extra work needs auth; keys logged not copied.

**Role/workflow:** new repeating pack that should become a registered job.

### 3. Classify and confirm

Group by role topic (night board, quality, supplies, SDS, keys, complaints). Ask which role jobs each entry applies to (default `all`). For each **rule**, ask for **Triggers** (`write:file` | `write:sheet` | `write:csv` | `write:doc` | `none`). Confirm before writing.

### 4. Format and integrate

Use the `### YYYY-MM-DD: Title` entry shape (see MEMORY-INDEX), including **Triggers:** on rules. Check duplicates/conflicts; quote conflicts and ask. Append to shared or operations per Workflows; update MEMORY-INDEX for new topics. After new triggered rules, regenerate the trigger index with `python scripts/memory/build_trigger_index.py`.

### 5. Summary

List files touched, duplicates merged, conflicts. Next step is review — not a developer commit pipeline unless they already use git for this folder.

## Edge cases

Ambiguous fact vs rule: ask. Conflicting rule: show both, ask which wins. Large docs: chunk. Do not store alarm codes, passwords, or SSNs found in the source — flag and strip.

## Complements

- **remember**: one-off during chat
- **promote-facts-rules**: Work Item → Expert Role
- **integrate-docs**: batch from files
