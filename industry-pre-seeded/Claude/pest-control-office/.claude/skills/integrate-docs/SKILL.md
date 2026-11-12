---
name: integrate-docs
description: "Use when the user provides documentation, notes, label files, route exports, or chemical-log templates to integrate into the expert system (facts, rules, and MyRole.txt role definition)."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into the expert system (facts, rules, and role definition).

**When to use:**
- User provides new documentation to integrate (route-export legend, chemical-log template, bait-map numbering note, WDO form checklist)
- User wants to update expert knowledge with how *this* pest office files work
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
- Updated `MyRole.txt` if new pest-office job patterns detected
- Summary report of what was integrated

> **Memory model (read first):** This pest-control office stores Expert Role memory in operations files. See `facts/MEMORY-INDEX.md` and `facts/HOW-MEMORY-LOADING-WORKS.md`. Do not route pest-office content into developer or production-incident files.

---

## Behavior

### Step 1: Gather Documents

Prompt user for document paths and an optional description (route CSV legend, chemical-log columns, bait-map numbering, WDO checklist, price-file layout).

Read all provided documents using the Read tool.

---

### Step 2: Analyze Content

For each document, identify:

**Facts (observations, data, context):**
- How this shop names a ticket, route, skip, callback, chemical log, bait map
- File locations they already use
- Column names and flags as they labeled them
- Frequency, commercial vs residential, pet/child/food/school flags as written

**Rules (constraints, procedures):**
- Never invent mix / EPA / rate
- Skip list wins
- Missing ticket or missing target label → ask
- No gate codes in this folder
- Completeness is present-or-missing

**Role updates:**
- New recurring jobs to register
- New must-never or out-of-scope lines

Do not persist unverified guesses. If wording is ambiguous, run **operator-qa** first.

---

### Step 3: Classify and store

1. Fact vs rule vs tool pointer.
2. Work Item vs Expert Role. Default Expert Role for shop-wide docs; Work Item for one route day or ticket.
3. For each **rule**, ask for **Triggers** (`write:doc` | `write:csv` | `write:pack` | `none`) so the action hook can surface it.
4. Append dated entries (`### YYYY-MM-DD: Title`, with `**Triggers:**` on rules) to `facts/facts-operations.md` or `facts/rules-operations.md` (or the Work Item pair). Use the shape in `facts/MEMORY-INDEX.md`.
5. Tool how-to → `docs/tools/` + INDEX row.
6. New topic → pointer in `facts/MEMORY-INDEX.md`.
7. If a new rule’s Triggers field is not `none`, regenerate: `py -3 scripts/memory/build_trigger_index.py`.

---

### Step 4: Confirm

List what was stored, where, and what was left as a question. Journal with **journal-keeper**.
