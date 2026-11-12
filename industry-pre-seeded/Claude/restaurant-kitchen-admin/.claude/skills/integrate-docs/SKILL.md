---
name: integrate-docs
description: "Use when the user provides shop notes, count sheets, allergen SOPs, or handbook pages to integrate into operations facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into the expert system (facts, rules, and role definition).

**When to use:**
- User provides new kitchen notes to integrate (count sheets, par lists, allergen SOPs, invoice folders, handbook pages)
- User wants to update expert knowledge with new domain information
- User wants to capture institutional knowledge from external sources

**Inputs:**
- Path(s) to document(s) containing knowledge to integrate
- Optional: Domain/category hints from user
- Optional: Fact vs rule classification hints

**Outputs:**
- New facts routed into `facts/facts-operations.md` (tag `**Workflows:**` with `all` or a registered kitchen job id)
- New rules routed into `facts/rules-operations.md`
- New/updated reference doc in `facts/` for large cross-job reference material, with a pointer added to `facts/MEMORY-INDEX.md`
- Updated `facts/MEMORY-INDEX.md` navigation so new knowledge is discoverable
- Updated `MyRole.txt` if new workflow patterns detected
- Summary report of what was integrated

> **Memory model (read first):** This role’s Expert Role memory is
> `facts/facts-operations.md` and `facts/rules-operations.md`. Each fact/rule
> carries a `Workflows:` field (`all` or a registered job id such as
> `prep`). See `facts/MEMORY-INDEX.md` and `facts/HOW-MEMORY-LOADING-WORKS.md`.

---

## Behavior

### Step 1: Gather Documents

Prompt user for document paths:
"What documentation would you like to integrate into the expert system?"

Please provide:
1. File path(s) to the document(s)
2. (Optional) A brief description of what this documentation covers
3. (Optional) Is this primarily facts (observations) or rules (procedures)?

Read all provided documents using the Read tool.

---

### Step 2: Analyze Content

For each document, analyze and identify:

**Facts (observations, data, context):**
- How this kitchen names pars, count units, and 86 items
- Where count sheets, par files, allergen matrix, and invoice PDFs live
- Shift splits (AM / PM / brunch / close)
- Vendor delivery days, catch-weight, split-case notes
- Tool locations (spreadsheet tabs, POS exports, vendor portal pointers)

**Rules (constraints, procedures, patterns to follow):**
- Never invent on-hand, par, allergen status, or holding time as law
- 86s, shorts, and missing counts stay visible
- Which sheet is live when two files disagree
- Required steps in a prep / order / receiving job
- Who they notify (chef, expo, vendor) — this expert does not send money
- Safety checks before actions

**Role/Workflow Updates:**
- New repeating jobs
- Workflow modifications
- Responsibility additions

---

### Step 3: Classify and Organize

Group extracted information by kitchen domain:

**Common domains for facts:** par, count, prep, 86, order guide, receiving, invoices, waste, allergens, catering, vendors, date marks (as their system)

**Common categories for rules:** never invent, visible holes, live sheet, one folder per job, no inspector stamp, no pay/PAN

Present classification to user, then ask workflow applicability for each fact/rule:

- Default: "all" (unless content is clearly one job)
- Examples:
  - Weekend chicken par tab → `par-review, prep`
  - Sysco Tuesday cutoff → `order-guide`
  - Live allergen matrix filename → `allergen-quote`
- User can specify "all", a registered job id, or a comma-separated list

---

### Step 4: Format Entries

Use the operations entry format in `facts/MEMORY-INDEX.md`. For a rule, include `**Rule:**` and default `**Triggers:**` to `none` unless they want `write:sheet`, `write:pack`, or `file:intake`.

---

### Step 5: Integrate into Files

**Route each entry to the operations pair:**

| `Workflows:` value | Facts file | Rules file |
|---|---|---|
| `all` or any registered kitchen job | `facts/facts-operations.md` | `facts/rules-operations.md` |

Do not route into software-design or incident-bridge memory files.

1. Read the destination operations files and `facts/MEMORY-INDEX.md`. Check for duplicates and conflicts.
2. If a new statement disagrees with an existing entry, quote both and ask which is live. Do not silently overwrite.
3. Append confirmed entries. After a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.
4. Update MEMORY-INDEX job pointers only if a new topic appeared.
5. If a new repeating job appeared, ask whether to add it to `MyRole.txt` and the workflow registry.

---

### Step 6: Report

Summarize paths written, facts/rules added, conflicts asked, and any MyRole or registry follow-up.

## Rules

- Route only into operations memory (or Work Item `facts/` if they said this pack only).
- Keep their wording. Label starter/guess material as such.
- Do not invent allergen legal status, holding times as law, inspection outcomes, or on-hand quantities while integrating.
- Confirm classification before writing.
