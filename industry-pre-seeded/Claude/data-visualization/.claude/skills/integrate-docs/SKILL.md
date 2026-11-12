---
name: integrate-docs
description: "Use when the user provides documentation, notes, export specs, chart style guides, or comments to integrate into the expert system (facts, rules, and MyRole.txt role definition)."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into shared/operations memory and the role definition.

**When to use:**
- User provides new documentation (export specs, style guides, column dictionaries, notes files)
- User wants to capture how *this* shop names columns, weeks, or colors

**Outputs:**
- New facts in `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md` (job-specific)
- New rules in `facts/rules-shared.md` or `facts/rules-operations.md`
- Optional reference doc in `facts/` with a pointer in `facts/MEMORY-INDEX.md`
- Updated `MyRole.txt` if new chart-pack patterns are detected
- Summary report of what was integrated
- Regenerated `facts/TRIGGER-INDEX.md` when rules gained non-`none` triggers

> **Memory model:** Always load shared + operations. Route `Workflows: all` to the shared pair. Do not invent developer or incident-response memory files.

---

## Behavior

### Step 1: Gather Documents

Ask for file path(s), a brief description, and whether the content is primarily facts or rules. Read all provided documents.

### Step 2: Analyze Content

**Facts:** column dictionaries, export encodings, how they roll days into weeks, palette names, where event dates live, typical source filenames.

**Rules:** never-impute, units required, question-first, refuse forecast-as-product, colorblind default, join-keys-theirs.

**Role/Workflow updates:** a repeating pack that should become a registered workflow.

### Step 3: Classify and Organize

Group by role topics (sources, tidy tables, chart forms, honesty/scales, refresh). Present classification and ask which items apply to `all` vs one registered job (`describe-csv`, `time-series-line`, …). Default `all`. Do not offer software-build or incident-response jobs.

For each **rule**, also ask for `**Triggers:**` (`write:python`, `write:csv`, `write:chart`, `write:doc`, or `none`).

### Step 4: Format Entries

Use the templates in `facts/MEMORY-INDEX.md` (`### YYYY-MM-DD: Title`). Rules must include `**Triggers:**`. Preserve wording. Label starter guesses.

### Step 5: Integrate into Files

1. Read the shared and operations pairs for duplicates and conflicts.
2. Flag conflicts for the operator; do not silently overwrite.
3. Append new entries (`Workflows: all` → shared; job id → operations). For large reference material (~50+ lines), use `facts/<topic>.md` plus a MEMORY-INDEX pointer.
4. Update `MyRole.txt` only if a new repeating job was approved.

### Step 6: Provide Summary

List added facts/rules, duplicates merged, conflicts, and next steps. If any rule trigger is not `none`, run `python scripts/memory/build_trigger_index.py`.

### Edge Cases

- Unclear fact vs rule: ask.
- New rule conflicts with existing: show both; ask which wins.
- New fact contradicts existing: ask whether to update, deprecate, or keep both with dates.

### Complements

- **remember**: one fact/rule from conversation
- **promote-facts-rules**: elevate Work Item memory
- **operator-qa**: verify notes before persisting
