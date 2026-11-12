---
name: integrate-docs
description: "Use when the user provides documentation, notes, policy PDFs, leftover-form templates, or roster exports to integrate into the expert system (facts, rules, and MyRole.txt role definition)."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into the expert system (facts, rules, and role definition).

**When to use:**
- User provides new documentation to integrate (event-order templates, leftover policy, allergen sheet legend, house equipment list notes)
- User wants to update expert knowledge with how *this* catering office files work
- User wants to capture institutional knowledge from external sources

**Inputs:**
- Path(s) to document(s) containing knowledge to integrate
- Optional: Domain/category hints from user
- Optional: Fact vs rule classification hints

**Outputs:**
- New facts routed into `facts/facts-operations.md`
- New rules routed into `facts/rules-operations.md`
- New/updated tool stub in `docs/tools/` when the doc is how they use a file or app
- Updated `facts/MEMORY-INDEX.md` navigation so new knowledge is discoverable
- Updated `MyRole.txt` if new catering-job patterns detected
- Summary report of what was integrated

> **Memory model (read first):** This catering office stores Expert Role memory in operations files. See `facts/MEMORY-INDEX.md` and `facts/HOW-MEMORY-LOADING-WORKS.md`. Do not route catering content into developer or production-incident files.

---

## Behavior

### Step 1: Gather Documents

Prompt user for document paths and an optional description (event orders, leftover policy, allergen chart, roster, rental vendor file).

Read all provided documents using the Read tool.

---

### Step 2: Analyze Content

For each document, identify:

**Facts (observations, data, context):**
- How this shop names an event order, guarantee, pack-out, leftover form
- File locations they already use
- House equipment names and counts as they labeled them
- Cutoff clocks, delivery windows, leftover policy as written

**Rules (constraints, procedures, patterns to follow):**
- Must-ask items (missing guarantee, missing window, missing allergen sheet)
- Never-invent items (price, tax, delivery fee, food cost, overtime)
- Routing (allergen flags route; you do not treat)
- One event, one Work Item folder

**Role/Workflow Updates:**
- New repeated catering jobs
- Responsibility additions (still must stay inside `MyRole.txt` out-of-scope)

---

### Step 3: Classify and Organize

Group extracted information by catering-office domain, for example:

**Facts:** Event order, guarantee, dietary/allergen, pack-out, house equipment, rentals, staffing, delivery/vehicle, leftover policy, fees copied from file

**Rules:** Ask-if-missing, never-invent, leftover-form-if-required, change-after-cutoff-logged, one-item-one-folder, label-guesses

Present classification to user and ask whether it looks correct.

After user confirms, **workflow applicability** defaults to `all` (operations memory).

---

### Step 4: Format Entries

Use the operations entry shape already in `facts/facts-operations.md` / `facts/rules-operations.md` (`### YYYY-MM-DD: Title`, Scope, Workflows, Captured, Source, Status, body). Rules also get `**Triggers:**` (`write:doc`, `write:csv`, `git:commit`, `git:push`, `pr:open`, or `none`) and a **Rule:** line. Ask which trigger fits each new rule.

---

### Step 5: Integrate into Files

Route to `facts/facts-operations.md` or `facts/rules-operations.md`. Large reference material may live as a tool doc under `docs/tools/` with an INDEX row.

1. Read the destination file for duplicates and conflicts.
2. Flag conflicts for the operator (quote both; ask which is right).
3. Append new entries. Update MEMORY-INDEX.md if a new browse topic appeared.
4. Update MyRole.txt only if they approved a new job or a new must-never.
5. If any new rule’s Triggers value is not `none`, regenerate with `python scripts/memory/build_trigger_index.py`.

---

### Step 6: Write Updates

Preserve existing content. Add new entries at the end. Include source attribution.

---

### Step 7: Provide Summary

List added facts, added rules, tool docs, duplicates merged, conflicts still open.

---

### Guidelines

- Never copy passwords, card PAN, or portal logins from a dropped doc into memory.
- Prefer facts over rules when ambiguous.
- Starter notes in this folder are guesses until they confirm; do not overwrite a taught shop rule with a generic catering article.
- Route by operations memory only.

**Complements:** **remember** for one-off chat captures; **promote-facts-rules** for Work Item → Expert Role.
