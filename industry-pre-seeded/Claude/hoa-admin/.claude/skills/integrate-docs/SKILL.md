---
name: integrate-docs
description: "Use when the user provides documentation, notes, Confluence exports, runbooks, or code comments to integrate into the expert system (facts, rules, and MyRole.txt role definition)."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into the expert system (facts, rules, and role definition).

**When to use:**
- User provides new documentation to integrate (notes files, confluence exports, code comments, runbooks, etc.)
- User wants to update expert knowledge with new domain information
- User wants to capture institutional knowledge from external sources

**Inputs:**
- Path(s) to document(s) containing knowledge to integrate
- Optional: Domain/category hints from user
- Optional: Fact vs rule classification hints

**Outputs:**
- New facts routed into `facts/facts-operations.md` (this role has no developer/incident memory files)
- New rules routed into `facts/rules-operations.md`
- New/updated reference doc in `facts/` (e.g. `facts/<topic>.md`) for large,
 cross-workflow reference material, with a pointer added to `facts/MEMORY-INDEX.md`
- Updated `facts/MEMORY-INDEX.md` navigation (reference list / Common Scenarios) so new knowledge is discoverable
- Updated `MyRole.txt` if new workflow patterns detected
- Summary report of what was integrated

> **Memory model (read first):** This HOA role stores Expert Role memory in
> `facts/facts-operations.md` and `facts/rules-operations.md`. Each fact/rule
> carries a `Workflows:` field (`all` or a registered job id such as
> `acc-completeness`, `violations`, `dues-aging`). See `facts/MEMORY-INDEX.md`
> and `facts/HOW-MEMORY-LOADING-WORKS.md`.

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
- How this association files ACC forms, violation logs, ledgers, board packets
- Lot/unit identifiers, software export names, meeting calendars
- Vendor certificate fields, reserve-study cover data, roster columns
- Historical context (why this board files a certain way)
- Tool locations (which PDF, which export)

**Rules (constraints, procedures, patterns to follow):**
- Must-never items (no legal stamp, no demand letter, no ACC approval)
- Required completeness checks before a pack
- Notice-step order from their adopted file
- One association per list
- Label starter guesses

**Role/Workflow Updates:**
- New repeating role jobs to register
- Responsibility additions in MyRole.txt

---

### Step 3: Classify and Organize

Group extracted information by domain/category:

**Common Domains for Facts:**
- Architectural applications
- Violations and notice steps
- Dues aging and ledgers
- Board meeting files
- Vendor bids and certificates
- Common-area work orders
- Elections and rosters
- Reserve studies
- Governing documents as quoted files
- How we file work items

**Common Categories for Rules:**
- Must never (legal, funds, ACC stamp)
- One association / one project
- Label guesses
- Minutes and privacy
- Photo and lot identity
- Vendor list and insurance presence

Present classification to user:
"I've analyzed the documentation and identified the following:"

FACTS (observations/data):
- [Domain: Architectural applications] 3 new entries about the ACC form
- [Domain: Board meeting files] 2 new packet exhibit names
- [Domain: How we file work items] 1 naming pattern

RULES (procedures/constraints):
- [Category: Must never] 1 no-demand-letter reminder
- [Category: One association / one project] 2 list rules
- [Category: Label guesses] 1 starter-label rule

ROLE UPDATES:
- No new workflow patterns detected

Does this classification look correct?
"(Reply 'yes' to proceed, or tell me what to adjust)"

After user confirms classification, **ask for workflow applicability for each fact/rule**:
"Which workflows does '[fact/rule title]' apply to?"
- Default: "all" (unless content clearly workflow-specific)
- Examples:
 - ACC form fields → acc-completeness
 - Aging columns → dues-aging
 - Must-never legal/funds → all

For each **rule**, also ask the action trigger:
"What tool-action should surface '[rule title]'?" Vocabulary: `write:doc`, `write:csv`, or `none`.
- User can specify "all", a registered job id, or comma-separated list

---

### Step 4: Format Entries

For each fact, use this format:
```markdown
## Domain: [Domain Name]

### YYYY-MM-DD: [Descriptive Title]
**Scope:** expert-role
**Workflows:** [all | registered job id]
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
**Workflows:** [all | registered job id]
**Triggers:** [write:doc | write:csv | none]
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
| `all` or any registered HOA job id | `facts/facts-operations.md` | `facts/rules-operations.md` |

**Reference-doc option (for large, cross-workflow material):** when the content is a sizable reference
(~50 lines, e.g. a schema, a catalog, validator internals) that several workflows consult, create or
extend a dedicated `facts/<topic>.md` reference doc instead of inflating a workflow file, and add a
pointer to it in `facts/MEMORY-INDEX.md` (reference list + a Common Scenarios entry).

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
- After appending any rule whose `Triggers:` is not `none`, regenerate the trigger index: `python scripts/memory/build_trigger_index.py`

---

### Step 7: Provide Summary

Show user a summary:
```
✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → Domain: Architectural applications → 5 entries
- facts/facts-operations.md → Domain: Board meeting files → 2 entries
- facts/facts-operations.md → Domain: How we file work items → 3 entries

ADDED TO RULES:
- facts/rules-operations.md → Category: Must never → 1 entry
- facts/rules-operations.md → Category: One association / one project → 2 entries
- facts/rules-operations.md → Category: Label guesses → 1 entry

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
- Review the changes in facts-operations.md / rules-operations.md (and MEMORY-INDEX.md)
- The expert will now use this knowledge on matching HOA role jobs
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
 - Association-specific details (form names, ledger columns, lot keys)
- Operational knowledge (how this role files ACC, violations, board packets)
- Historical context (why this board files a certain way)
- Tool locations (which PDF, which export)

**Rule Extraction Priorities:**
- Must-never items (legal stamp, demand letters, ACC approval, fund movement)
- Completeness checks before a pack
- One association / one project
- Label starter guesses

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
Can you integrate this new runbook I created?
C:\docs\Failover-Procedure-2026.md
```

**Agent:**
```
I'll read and integrate the association's architectural-guidelines PDF.

[Reads document, analyzes content]

I've analyzed the guidelines and identified:

FACTS (observations/data):
- [Domain: Architectural applications] 1 new entry: neighbor signature required on page 2
- [Domain: Architectural applications] 2 new exhibit names (sketch, color sample)

RULES (procedures/constraints):
- [Category: Must never] 1 reminder: completeness only, no ACC stamp
- [Category: Label guesses] 1 reminder: do not invent a solar rule

Does this classification look correct?
```

**User:**
```yes
```

**Agent:**
```
[Routes content into operations memory]

✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → Domain: Architectural applications → 3 entries

ADDED TO RULES:
- facts/rules-operations.md → Category: Must never → 1 entry
- facts/rules-operations.md → Category: Label guesses → 1 entry

Total new facts: 3
Total new rules: 2

The expert will now use this knowledge on ACC completeness jobs.
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
- **Route to operations**: write Expert Role captures to `facts/facts-operations.md` / `facts/rules-operations.md`.
 Large reference material may live as a dedicated `facts/<topic>.md` file with a `MEMORY-INDEX.md` pointer.
