---
name: integrate-docs
description: "Use when the user provides shop notes, bake-sheet exports, allergen SOPs, or handbook pages to integrate into operations facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into the expert system (facts, rules, and role definition).

**When to use:**
- User provides new shop notes to integrate (bake sheets, allergen SOPs, handbook pages, exports)
- User wants to update expert knowledge with new domain information
- User wants to capture institutional knowledge from external sources

**Inputs:**
- Path(s) to document(s) containing knowledge to integrate
- Optional: Domain/category hints from user
- Optional: Fact vs rule classification hints

**Outputs:**
- New facts routed into `facts/facts-operations.md` (tag `**Workflows:**` with `all` or a registered bakery-cafe job id)
- New rules routed into `facts/rules-operations.md`
- New/updated reference doc in `facts/` (e.g. `facts/<topic>.md`) for large,
 cross-workflow reference material, with a pointer added to `facts/MEMORY-INDEX.md`
- Updated `facts/MEMORY-INDEX.md` navigation (reference list / Common Scenarios) so new knowledge is discoverable
- Updated `MyRole.txt` if new workflow patterns detected
- Summary report of what was integrated

> **Memory model (read first):** This role’s Expert Role memory is
> `facts/facts-operations.md` and `facts/rules-operations.md`. Each fact/rule
> carries a `Workflows:` field (`all` or a registered job id such as
> `bake-list-day`). See `facts/MEMORY-INDEX.md` and `facts/HOW-MEMORY-LOADING-WORKS.md`.

---

## Behavior

### Step 1: Gather Documents

Prompt user for document paths:
"What documentation would you like to integrate into the expert system?"

Please provide:
1. File path(s) to the document(s) (e.g., C:\docs\new-runbook.txt)
2. (Optional) A brief description of what this documentation covers
3. (Optional) Is this primarily facts (observations) or rules (procedures)?

You can provide multiple paths separated by commas.


Read all provided documents using the Read tool.

---

### Step 2: Analyze Content

For each document, analyze and identify:

**Facts (observations, data, context):**
- How this shop names bake-list items, formula cards, and mix counts
- Where case par, standing CSV, allergen sheet, and invoice PDFs live
- Cafe versus wholesale split as they coded it
- Holiday tabs, cake-order fields, receiving columns
- Tool locations (spreadsheet tabs, bakery-system exports)

**Rules (constraints, procedures, patterns to follow):**
- Never invent formula, mix count, par, servings, or allergen status
- Shorts, stales, and missing formulas stay visible
- Which sheet is live when two files disagree
- Required steps in a bake-list / wholesale / receiving job
- Who they notify (counter, account, mill) — this expert does not send money or email as a product
- Safety checks before actions

**Role/Workflow Updates:**
- New pipeline patterns
- Workflow modifications
- Responsibility additions

---

### Step 3: Classify and Organize

Group extracted information by domain/category:

**Common Domains for Facts:**
- Bake list and mix counts
- Case par and case count
- Wholesale standing and routes
- Custom cakes and wedding tickets
- Allergen sheet and labeling (their file)
- Receiving, invoices, vendors
- Ingredient pars (flour, butter, dairy)
- Waste, stales, holiday tabs
- Formula files, yield, scale weights

**Common Categories for Rules:**
- Never invent formula / qty / par / allergen
- Shorts, stales, missing formulas stay visible
- Live-sheet when two files disagree
- No inspector / FDA / gluten legal claim
- No pay / PAN / passwords
- Cafe vs wholesale split
- One Work Item, one folder

Present classification to user:
"I've analyzed the documentation and identified the following:"

FACTS (observations/data):
- [Bake list] 3 notes about how this shop names mix counts
- [Case par] 2 notes about weekend vs weekday tabs
- [Allergen sheet] 1 note about which matrix is live

RULES (procedures/constraints):
- [Never invent] 1 rule about formula cards
- [Visible shorts] 1 rule about receiving
- [Live sheet] 1 rule about two allergen files

For each new **rule**, ask whether it needs an action trigger (`none` default, or `write:sheet` / `write:pack` / `file:intake`).

ROLE UPDATES:
- No new workflow patterns detected

Does this classification look correct?
"(Reply 'yes' to proceed, or tell me what to adjust)"

After user confirms classification, **ask for workflow applicability for each fact/rule**:
"Which workflows does '[fact/rule title]' apply to?"
- Default: "all" (unless content is clearly one job)
- Examples:
 - Weekend croissant par tab → `case-par-vs-count, bake-list-day`
 - Standing-change effective date → `wholesale-day`
 - Live allergen matrix filename → `allergen-sheet-index`
- User can specify "all", a registered job id, or a comma-separated list

---

### Step 4: Format Entries

For each fact, use this format:
```markdown
## Domain: [Domain Name]

### YYYY-MM-DD: [Descriptive Title]
**Scope:** expert-role
**Workflows:** [all | bake-list-day | wholesale-day | comma-separated]
**Captured:** YYYY-MM-DD

**Source:** [Document name/path]

[Content with full formatting preserved]

**Key Points:**
- [Bullet point summary if content is long]

---
```

For each rule, use this format:
```markdown
## Category: [Category Name]

### YYYY-MM-DD: [Descriptive Title]
**Scope:** expert-role
**Workflows:** [all | bake-list-day | wholesale-day | comma-separated]
**Triggers:** [none | write:sheet | write:pack | file:intake]
**Captured:** YYYY-MM-DD
**Source:** [Document name/path]
**Rule:** [Clear statement of what must be done]

**Why:** [Reason/context for this rule]

**How to apply:**
[Step-by-step application instructions]

**Violation:** [Consequence of not following this rule]

---
```

---

### Step 5: Integrate into Files

**Route each entry to the correct file by its `Workflows:` value:**

| `Workflows:` value | Facts file | Rules file |
|---|---|---|
| `all` | `facts/facts-shared.md` | `facts/rules-shared.md` |
| any registered bakery-cafe job | `facts/facts-operations.md` | `facts/rules-operations.md` |

**Reference-doc option (for large, cross-workflow material):** when the content is a sizable reference
(~50 lines) that several jobs consult, create or extend a dedicated `facts/<topic>.md` reference doc
instead of inflating a workflow file, and add a pointer in `facts/MEMORY-INDEX.md`.

1. **Read the existing destination files:**
 - Read the target `facts/facts-*.md` and/or `facts/rules-*.md` (or the reference doc) for the chosen
    workflow(s) to check for duplicates and conflicts. Consult `facts/MEMORY-INDEX.md` to confirm the
    right file. (Do NOT use the archived `facts-ARCHIVE-*.md` / `rules-ARCHIVE-*.md` files.)

2. **Detect duplicates/conflicts:**
 - Check if similar facts already exist (avoid redundancy)
 - Check if rules conflict with existing rules (flag for user review)

3. **Organize by domain/category:**
 - Add new facts to the appropriate domain section in the chosen `facts/facts-*.md` (or reference doc)
 - Add new rules to the appropriate category section in the chosen `facts/rules-*.md`
 - Create new domain/category sections if needed

4. **Update MEMORY-INDEX.md if needed:**
 - If a new reference doc was created or a new high-value scenario emerged, add a line to the
    reference list and/or a "Common Scenarios → Memory References" entry so it is discoverable.

5. **Update MyRole.txt if needed:**
 - If new workflow patterns detected, propose additions to pipeline definitions
 - If new responsibilities identified, propose updates to role description

---

### Step 6: Write Updates

Use the Edit tool to add new entries to the routed `facts/facts-*.md` / `facts/rules-*.md` files (and
any reference doc + `facts/MEMORY-INDEX.md` pointer).

**Important:**
 - Preserve all existing content
- Add new entries at the end of their respective domain/category sections
- Maintain consistent formatting
- Include source attribution
- After adding any rule whose Triggers is not `none`, regenerate with `python scripts/memory/build_trigger_index.py`

---

### Step 7: Provide Summary

Show user a summary:
```
✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → Bake list / case par / standing notes → N entries

ADDED TO RULES:
- facts/rules-operations.md → Never-invent / visible-shorts rules → N entries

REFERENCE DOCS:
- (if created) facts/<topic>.md + pointer added to facts/MEMORY-INDEX.md

ROLE UPDATES:
- No changes to MyRole.txt

DUPLICATES DETECTED:
- 2 facts were similar to existing entries (merged into existing)

CONFLICTS DETECTED:
- None

Total new facts: 8
Total new rules: 4

Next steps:
- Review the changes in the routed facts-*/rules-* files (and MEMORY-INDEX.md)
- Commit the updates: git add facts/ && git commit -m "Integrate [document name]"
- The expert will now use this knowledge in the matching workflow(s)
```

---

### Edge Cases

#### Large Documents

If document is very large (>1000 lines):
1. Inform user it will take time to process
2. Break into chunks and analyze incrementally
3. Show progress updates

#### Ambiguous Content

If unclear whether content is fact or rule:
- **Fact**: Describes what IS (observations, data, context)
- **Rule**: Describes what MUST BE DONE (procedures, constraints)
- Ask user for clarification if truly ambiguous

#### Conflicting Rules

If new rule conflicts with existing rule:
1. Flag the conflict clearly
2. Show both rules side-by-side
3. Ask user which to keep or how to reconcile
4. Document the decision in the rule's "Why" section

#### Outdated Facts

If new fact contradicts existing fact:
1. Flag the contradiction
2. Ask user if old fact should be updated, deprecated, or both kept with version notes
3. Add "Superseded by" note to old fact if applicable

#### Duplicate Prevention

Before adding a fact/rule:
1. Search existing facts/rules for similar content
2. If >70% similar, ask user: "This seems similar to existing entry. Merge or keep separate?"
3. If merge, combine and note both sources
4. If separate, ensure both are clearly differentiated

---

### Guidelines

**Fact Extraction Priorities:**
 - System-specific details (URLs, table names, procedures)
- Operational knowledge (how systems work)
- Historical context (why decisions were made)
- Contact information (teams, channels, escalation paths)
- Tool locations and usage

**Rule Extraction Priorities:**
- Must-follow procedures (incident response, deployment)
- Safety checks (what to verify before taking action)
- Communication requirements (who to notify, when)
- Validation requirements (what to check)
- Error handling patterns (what to do when X happens)

**Formatting Standards:**
- Use consistent date format: YYYY-MM-DD
- Preserve code blocks with proper language tags
- Preserve tables and lists from source documents
- Include enough context to be self-contained
- Add "Key Points" summary for long facts

**Source Attribution:**
- Always include source in **Source:** field
- For files: Use file name (e.g., "GGNotes_App.txt")
- For URLs: Include full URL
- For team knowledge: Include person/team name and date
- For runbooks: Include runbook name and location

---

### Example Usage

**User:**
```
Can you integrate this allergen SOP I dropped?
C:\shop\allergen-matrix-notes.md
```

**Agent:**
```
I'll read and integrate the allergen SOP.

[Reads document, analyzes content]

I've analyzed the notes and identified:

FACTS (observations/data):
- [Allergen sheet] 1 note about which matrix is live
- [Receiving] 1 note about how this dock files shorts

RULES (procedures/constraints):
- [Allergen / receiving] 3 procedures:
 1. Quote the live allergen matrix only
 2. Keep receiving shorts visible next to the invoice
 3. Ask when a formula card is missing

Does this classification look correct?
```

**User:**
```yes
```

**Agent:**
```
[Routes content into operations memory – allergen and receiving notes are bakery-cafe jobs]

✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → Allergen / receiving notes → 3 entries

ADDED TO RULES:
- facts/rules-operations.md → Live-sheet and visible-shorts rules → 3 entries

Total new facts: 3
Total new rules: 3

The expert will now quote the live allergen matrix and keep receiving shorts visible.
```

---

### Integration with Other Skills

**Complements:**
- **remember**: For ad-hoc single facts/rules during conversation
- **promote-facts-rules**: For elevating Work Item learnings to Expert Role level

**Difference from remember:**
- **remember**: Interactive capture during work (user says "remember this")
- **integrate-docs**: Batch processing of existing documentation
- **remember**: Usually 1 fact/rule at a time
- **integrate-docs**: Usually 5-50+ facts/rules from a document

---

### Notes

- This skill does NOT modify Work Item-level facts/rules (only Expert Role level)
- For Work Item-specific knowledge, use the remember skill during active Work Item
- Always maintain source attribution for audit trail
- Prefer facts over rules when ambiguous (facts are informational, rules are restrictive)
- When in doubt about classification, ask the user
- **Route by workflow**: Expert Role memory is workflow-split – write to the `facts-*` / `rules-*` file
 that matches each entry's `Workflows:` value.
 Large cross-workflow reference material goes in a dedicated `facts/<topic>.md` reference doc with a
`MEMORY-INDEX.md` pointer.
