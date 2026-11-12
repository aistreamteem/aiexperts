---
name: integrate-docs
description: "Use when the user provides documentation, notes, exports, or runbooks to integrate into this clinic-role expert (facts, rules, MyRole.txt)."
---

# integrate-docs

**Purpose:** Integrate documentation into this medical clinic front-role expert (shared facts/rules and role definition).

**When to use:**
- Operator provides clinic notes, form packets, export legends, or policy pages
- Operator wants to capture how *this* shop files day lists, eligibility screenshots, or referrals

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

**Facts:** export headers, provider names, form packet list, payer names they use, where the day-close report lives, how they label no-shows.

**Rules:** never diagnose, never invent benefits, ask if NPP is missing, quote the screenshot, one Work Item per pack.

**Role updates:** new repeating role job, tighter out-of-scope, new must-never.

### Step 3: Classify

Group by clinic-role topics (scheduling, intake forms, eligibility, referrals, ROI, wait/recall, no-shows, day close, PHI). Confirm with the operator. Default workflow applicability: `all` or the matching job id (`day-list`, `intake-completeness`, …).

For rules, also ask **Triggers** (`none` | `write:doc` | `write:csv`).

### Step 4: Format and append

Use the shared entry shape in `facts/MEMORY-INDEX.md` (`### YYYY-MM-DD: Title`). Include `**Triggers:**` on every rule. Label starter guesses. Do not copy full SSN, full card numbers, or extra clinical narrative from the source docs.

### Step 5: Tools

If the document describes how they export a day list, eligibility screenshot, or referral packet, add or update `docs/tools/` and `docs/tools/INDEX.md`.

### Step 6: Confirm

List paths written. Offer **remember** only for leftovers that still need a yes/no. Regenerate the trigger index with `python scripts/memory/build_trigger_index.py` if any new rule has a non-`none` trigger.
