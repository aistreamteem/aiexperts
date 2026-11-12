---
name: integrate-docs
description: "Use when the user provides documentation, notes, exports, or runbooks to integrate into this PT front-role expert (facts, rules, MyRole.txt)."
---

# integrate-docs

**Purpose:** Integrate documentation into this physical-therapy front-role expert (operations facts/rules and role definition).

**When to use:**
- Operator provides clinic notes, referral packets, export legends, or policy pages
- Operator wants to capture how *this* shop files remaining visits, recerts, or day lists

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

**Facts:** export headers, therapist names, referral packet list, payer names they use, where the day-close report lives, how they label no-shows.

**Rules:** never treat, never invent remaining visits, ask if a referral page is missing, quote the screenshot, one Work Item per pack.

**Role updates:** new repeating role job, tighter out-of-scope, new must-never.

### Step 3: Classify

Group by PT front-role topics (scheduling, remaining visits, referral/POC, recert, HEP print, no-show, wait list, day close, PHI). Confirm with the operator. Default workflow applicability: `all` or the matching job id (`day-list`, `auth-remaining-from-file`, …). For each new **rule**, ask for **Triggers** (`write:doc`, `write:csv`, or `none`).

### Step 4: Format and append

Use the operations entry shape in `facts/MEMORY-INDEX.md` with `### YYYY-MM-DD: Title` headers. Include `**Triggers:**` on every rule. Label starter guesses. Do not copy full SSN, full card numbers, or extra clinical narrative from the source docs.

### Step 5: Tools

If the document describes how they export a day list, auth tracker, or visit-count CSV, add or update `docs/tools/` and `docs/tools/INDEX.md`.

### Step 6: Confirm

List paths written. Offer **remember** only for leftovers that still need a yes/no. Run `python scripts/memory/build_trigger_index.py` if any new rule has a non-`none` trigger.
