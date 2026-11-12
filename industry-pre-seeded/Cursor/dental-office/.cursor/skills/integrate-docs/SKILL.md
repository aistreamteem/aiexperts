---
name: integrate-docs
description: "Use when the user provides documentation, notes, exports, or runbooks to integrate into this dental-role expert (facts, rules, MyRole.txt)."
---

# integrate-docs

**Purpose:** Integrate documentation into this dental front-role expert (operations facts/rules and role definition).

**When to use:**
- Operator provides office notes, form packets, export legends, or policy pages
- Operator wants to capture how *this* shop files claims, recalls, or day sheets

**Outputs:**
- Facts appended to `facts/facts-operations.md`
- Rules appended to `facts/rules-operations.md`
- Tool stubs under `docs/tools/` when they describe an app or export
- Pointers in `facts/MEMORY-INDEX.md` for new topics
- Updated `MyRole.txt` only if scope or must-nevers changed
- Summary of what was integrated

> **Memory model:** This role uses operations memory only (`facts/facts-operations.md` and `facts/rules-operations.md`).

## Behavior

### Step 1: Gather documents

Ask for path(s), a short description, and whether the material is mostly facts or rules.

### Step 2: Analyze

**Facts:** export headers, chair names, form packet list, payer names they use, where the day-close report lives, how they label broken appointments.

**Rules:** never diagnose, never guess fees, ask if a form is missing, quote the screenshot, one Work Item per pack.

**Role updates:** new repeating role job, tighter out-of-scope, new must-never.

### Step 3: Classify

Group by dental-role topics (scheduling, intake forms, eligibility, claims, EOBs, recall, day close, PHI). Confirm with the operator. Default workflow applicability: `all` or the matching job id (`day-list`, `forms-check`, …). For each rule, ask for **Triggers** (`write:doc`, `write:csv`, or `none`) so the action hook can surface it.

### Step 4: Format and append

Use the operations entry shape in `facts/MEMORY-INDEX.md` (`### YYYY-MM-DD: Title`, include `**Triggers:**` on rules). Label starter guesses. Do not copy full SSN, full card numbers, or extra clinical narrative from the source docs.

### Step 5: Tools

If the document describes how they export a day sheet, recall CSV, or EOB PDF, add or update `docs/tools/` and `docs/tools/INDEX.md`.

### Step 6: Confirm

List paths written. Offer **remember** only for leftovers that still need a yes/no. Regenerate the trigger index with `py -3 scripts/memory/build_trigger_index.py` if any new rule has a non-`none` trigger.
