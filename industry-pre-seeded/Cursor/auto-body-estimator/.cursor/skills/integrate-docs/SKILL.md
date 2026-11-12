---
name: integrate-docs
description: "Use when the user provides documentation, notes, exports, runbooks, or shop files to integrate into shared facts, rules, and MyRole.txt."
disable-model-invocation: false
---

# integrate-docs

**Purpose:** Integrate documentation into this Auto body estimator / office Expert (facts, rules, role).

**When to use:**
- Operator provides shop notes, DRP guidelines they are allowed to store, procedure lists, naming conventions, or exports
- Operator wants to capture institutional knowledge from files they dropped

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional pointer in `facts/MEMORY-INDEX.md`
- Tool stubs under `docs/tools/` when they described an app or file
- `MyRole.txt` updates only if a new repeating job appeared
- Summary of what was integrated

> **Memory model:** This role uses the shared pair only. Route `Workflows: all` here.

---

## Behavior

### Step 1: Gather Documents

Ask for paths and a one-line description. Read the files. Never store passwords, portal logins, or card PAN.

### Step 2: Analyze Content

**Facts (what is true here):** assignment layout, VIN source, photo naming, labor matrix location, parts file columns, supplement log columns, cycle calendar fields, DRP flags they filed.

**Rules (what must be done):** hours from matrix, no invented prices, auth required, one Work Item per claim, label guesses, refer mechanical out.

**Role/workflow updates:** a new repeating job that belongs in `.cursor/workflows/` and the registry.

### Step 3: Classify

Group by collision-office domains: Assignment, VIN/vehicle, Photos, Estimate/labor/parts, OEM procedures, Authorization, Supplements, Parts order, Pay types, Cycle time, Scope/must-never.

Confirm classification with the operator. Default **Workflows:** `all`.

### Step 4: Format and integrate

Append dated entries (`### YYYY-MM-DD: Title`) to the shared files. For rules, include `**Triggers:**` (role tokens or `none`). Check duplicates and conflicts; ask which wins. Update MEMORY-INDEX if a new topic appears, then regenerate the trigger index after tagging rules. Propose MyRole/workflow changes; do not invent a job they did not describe.

### Step 5: Summary

List paths, counts, conflicts, and next steps (continue the Work Item, or remember a leftover one-liner).

## Complements

- **remember** — one fact/rule during chat
- **promote-facts-rules** — elevate Work Item learnings
- **operator-qa** — verify notes before persisting
