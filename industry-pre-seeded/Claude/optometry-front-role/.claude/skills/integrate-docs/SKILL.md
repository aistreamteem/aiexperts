---
name: integrate-docs
description: "Use when the user provides documentation, notes, exports, or runbooks to integrate into this optometry-role expert (facts, rules, MyRole.txt)."
---

# integrate-docs

**Purpose:** Integrate documentation into this optometry front-role expert (operations facts/rules and role definition).

**When to use:**
- Operator provides office notes, order-ticket legends, export headers, or policy pages
- Operator wants to capture how *this* shop files day lists, eligibility prints, optical tickets, or recall lists

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

**Facts:** export headers, doctor names, visit types, frame-order columns, where the day-close report lives, how they label ready vs notified.

**Rules:** never diagnose, never invent remaining benefits, ask if a Rx or trace is missing, quote the screenshot, one Work Item per pack.

**Role updates:** new repeating role job, tighter out-of-scope, new must-never.

### Step 3: Classify

Group by optometry-role topics (scheduling, eligibility, optical orders, recall, pickup notify, redo, wait list, day close, PHI). Confirm with the operator. Default workflow applicability: `all` or the matching job id (`day-list`, `eligibility-screenshot`, …). For each **rule**, ask for **Triggers** (`write:doc`, `write:csv`, or `none`).

### Step 4: Format and append

Use the operations entry shape (see `facts/MEMORY-INDEX.md`), including `### YYYY-MM-DD:` headers. Rules must include a `**Triggers:**` line. Label starter guesses. Do not copy full SSN, full card numbers, or extra clinical narrative from the source docs.

### Step 5: Tools

If the document describes how they export a day list, recall CSV, frame-order sheet, or lab-status file, add or update `docs/tools/` and `docs/tools/INDEX.md`.

### Step 6: Confirm

List paths written. Offer **remember** only for leftovers that still need a yes/no. Regenerate the trigger index with `python scripts/memory/build_trigger_index.py` whenever any new or retagged rule has a non-`none` trigger.
