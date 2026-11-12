---
name: integrate-docs
description: "Use when the user provides documentation, notes, exports, or runbooks to integrate into this veterinary-role expert (facts, rules, MyRole.txt)."
---

# integrate-docs

**Purpose:** Integrate documentation into this veterinary front-role expert (shared facts/rules and role definition).

**When to use:**
- Operator provides clinic notes, form packets, export legends, or policy pages
- Operator wants to capture how *this* shop files appointments, records, or reminders

**Outputs:**
- Facts appended to `facts/facts-shared.md`
- Rules appended to `facts/rules-shared.md`
- Tool stubs under `docs/tools/` when they describe an app or export
- Pointers in `facts/MEMORY-INDEX.md` for new topics
- Updated `MyRole.txt` only if scope or must-nevers changed
- Summary of what was integrated

> **Memory model:** This role uses shared memory only (`facts/facts-shared.md` and `facts/rules-shared.md`). Route `Workflows: all` here. Do not invent developer or incident-response buckets.

## Behavior

### Step 1: Gather documents

Ask for path(s), a short description, and whether the material is mostly facts or rules.

### Step 2: Analyze

**Facts:** export headers, appointment-type names, form packet list, price-file tabs, where the reminder report lives, how they label boarding vs surgery drop-off.

**Rules:** never diagnose, never guess fees, ask if a form is missing, quote the price file, one Work Item per pack.

**Role updates:** new repeating role job, tighter out-of-scope, new must-never.

### Step 3: Classify

Group by veterinary-role topics (appointments, emergency flag, new-client forms, records, reminders, estimates, checkout, boarding, privacy). Confirm with the operator. Default workflow applicability: `all` or the matching job id (`day-appointments`, `records-in`, …).

For rules, also ask **Triggers** (`none` | `write:doc` | `write:csv`).

### Step 4: Format and append

Use the shared entry shape in `facts/MEMORY-INDEX.md` (`### YYYY-MM-DD: Title`). Include `**Triggers:**` on every rule. Label starter guesses. Do not copy full card numbers, portal passwords, or extra clinical narrative from the source docs.

### Step 5: Tools

If the document describes how they export a day book, reminder CSV, or invoice file, add or update `docs/tools/` and `docs/tools/INDEX.md`.

### Step 6: Confirm

List paths written. Offer **remember** only for leftovers that still need a yes/no. Regenerate the trigger index with `python scripts/memory/build_trigger_index.py` if any new rule has a non-`none` trigger.
