---
name: integrate-docs
description: "Use when the user provides documentation, notes, shop SOPs, route exports, or price-file packets to integrate into the expert system (facts, rules, and MyRole.txt role definition)."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into the expert system (facts, rules, and role definition).

**When to use:**
- User provides new documentation to integrate (shop notes, log templates, closeout lists, export samples)
- User wants to update expert knowledge with new domain information
- User wants to capture institutional knowledge from external sources

**Inputs:**
- Path(s) to document(s) containing knowledge to integrate
- Optional: Domain/category hints from user
- Optional: Fact vs rule classification hints

**Outputs:**
- New facts appended to `facts/facts-operations.md`
- New rules appended to `facts/rules-operations.md`
- New/updated reference doc in `facts/` (e.g. a topic reference such as `price-file-notes.md`) for large,
 cross-workflow reference material, with a pointer added to `facts/MEMORY-INDEX.md`
- Updated `facts/MEMORY-INDEX.md` navigation (reference list / Common Scenarios) so new knowledge is discoverable
- Updated `MyRole.txt` if new workflow patterns detected
- Summary report of what was integrated

> **Memory model (read first):** This landscaping-office Expert stores Expert Role
> memory in `facts/facts-operations.md` and `facts/rules-operations.md` only.
> See `facts/MEMORY-INDEX.md` and `facts/HOW-MEMORY-LOADING-WORKS.md`. Do not write
> extra software-engineering or outage-role memory files.

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
- How this shop names jobs, tickets, and routes
- Export locations and template filenames (no passwords)
- Column names on their ticket / route / price-file sheets
- Where they keep rosters, skip lists, and photo folders
- Team contacts and channels
- Historical context (why decisions were made)
- Error message catalogs
- Tool locations and versions

**Rules (constraints, procedures, patterns to follow):**
- Standard operating procedures
- Extra-work authorization follow-up
- Skip-list, dog-flag, and weather-they-call rules
- Required steps in a process
- Validation requirements
- Pack checks (CSV columns, file exists)
- Communication protocols (who to notify, when)
- Safety checks before actions

**Role/Workflow Updates:**
- New registered-job patterns
- Workflow modifications
- Responsibility additions

---

### Step 3: Classify and Organize

Group extracted information by domain/category:

**Common Domains for Facts:**
- Job tickets and property lists
- Crew roster and route day
- Price file and estimates
- Material pull and equipment
- Weather postpone and skip lists
- Callbacks and photos
- Seasonal calendar and enhancements
- How this shop files

**Common Categories for Rules:**
- Quote the file / do not invent
- One job, one Work Item folder
- No pesticide license, tree diagnosis, or payroll
- Extra-work auth and commercial PO
- Weather is their call
- Template and column names they use
- Gate codes stay out of this folder

Present classification to user:
"I've analyzed the documentation and identified the following:"

FACTS (observations/data):
- [Domain: Job tickets] 3 new entries about their ticket columns
- [Domain: Price file] 2 new export filenames
- [Domain: How this shop files] 1 crew-day folder pattern

RULES (procedures/constraints):
- [Category: Quote the file] 1 quote-both-files rule
- [Category: Never invent a dump fee] 1 ask-if-blank rule
- [Category: Extra-work auth] 1 auth-file rule

ROLE UPDATES:
- No new workflow patterns detected

Does this classification look correct?
"(Reply 'yes' to proceed, or tell me what to adjust)"

After user confirms classification, **ask for workflow applicability for each fact/rule**:
"Which workflows does '[fact/rule title]' apply to?"
- Default: "all" (unless content clearly workflow-specific)
- Examples:
 - Ticket columns → all or crew-day
 - Price-file rules → all or estimate-from-price
 - Weather-call notes → all or weather-postpone-list
- User can specify "all", single workflow, or comma-separated list

For each **rule**, also ask **Triggers:** `write:doc`, `write:csv`, or `none` (vocabulary matches `.cursor/hooks/inject_rules_on_action.py`).

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
| `all` or a registered job id | `facts/facts-operations.md` | `facts/rules-operations.md` |

**Reference-doc option (for large, cross-workflow material):** when the content is a sizable reference
(~50 lines, e.g. a schema, a catalog, validator internals) that several workflows consult, create or
extend a dedicated `facts/<topic>.md` reference doc instead of inflating a workflow file, and add a
pointer to it in `facts/MEMORY-INDEX.md` (reference list + a Common Scenarios entry). This mirrors the
MEMORY-INDEX pointer pattern.

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
 - After appending any rule whose Triggers is not `none`, regenerate the trigger index: `py -3 scripts/memory/build_trigger_index.py`

---

### Step 7: Provide Summary

Show user a summary:
```
✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → ticket / route columns
- facts/facts-operations.md → price-file names they use

ADDED TO RULES:
- facts/rules-operations.md → no-invent-dump-fee / no-pesticide-license
- facts/rules-operations.md → quote both files when they disagree

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
- Must-follow procedures (quote the file, one job per pack)
- Safety checks (what to verify before taking action; incidents stay human)
- Communication requirements (who to notify, when)
- Validation requirements (CSV columns, file exists)
- Error handling patterns (what to do when a source file is missing)

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
Can you integrate this closeout checklist I created?
C:\docs\Closeout-Checklist-2026.md
```

**Agent:**
```
I'll read and integrate the closeout checklist.

[Reads document, analyzes content]

I've analyzed the checklist and identified:

FACTS (observations/data):
- [Domain: Punch and closeout] 1 new entry: Required O&M tabs they named
- [Domain: How this shop files] 2 filenames for warranty logs

RULES (procedures/constraints):
- [Category: Quote the file / do not invent] 1 presence/absence rule
- [Category: Punch complete only from their sheet] 1 complete-only-from-file rule

Does this classification look correct?
```

**User:**
```yes
```

**Agent:**
```
[Routes content into operations memory for this landscaping-office role]

✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → crew-roster export path they named

ADDED TO RULES:
- facts/rules-operations.md → never invent a dump fee if the price file has no line

Total new facts: 1
Total new rules: 1

The expert will now use those notes on later packs.
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
