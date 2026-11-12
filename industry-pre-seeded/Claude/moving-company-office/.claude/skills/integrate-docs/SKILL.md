---
name: integrate-docs
description: "Use when the user provides shop notes, rate-book pages, inventory examples, runbooks, or other moving-office documents to integrate into facts, rules, and MyRole.txt."
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
- New facts appended to `facts/facts-shared.md` or `facts/facts-operations.md`
- New rules appended to `facts/rules-shared.md` or `facts/rules-operations.md`
- Optional large reference file under `facts/` with a pointer in `facts/MEMORY-INDEX.md`
- Updated `MyRole.txt` if new role jobs are detected
- Summary report of what was integrated

> **Memory model (read first):** This moving-office role stores Expert Role knowledge in
> shared memory for `Workflows: all` and operations memory for job-scoped entries.
> `Workflows:` is `all` or a registered job id. See `facts/MEMORY-INDEX.md`.

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
- How this shop files rates, inventories, calendars, scale tickets, claims
- Column names on their sheets
- Who owns the claims log or dispatch board
- Starter vs confirmed shop practice
- Tool locations (jobber export path, rate-book PDF)

**Rules (constraints, procedures, patterns to follow):**
- Never invent weight, cube, extras, crew names, or delivery hours
- Rates and materials from their live file only
- Claims route, do not adjust
- Required papers (high-value list, binding type)
- One Work Item folder per move

**Role/Workflow Updates:**
- New registered role jobs
- Changes to `docs/role/work-item-method.md`
- Scope / must-never updates in `MyRole.txt`

---

### Step 3: Classify and Organize

Group extracted information by domain/category:

**Common Domains for Facts:**
- Rate file / extras / fuel
- Inventory / cube / PBO vs CP / high-value list
- Crew / truck calendar / delivery windows
- Scale tickets / weight
- Claims routing / photos / BOL
- Building / accessorials as their file

**Common Categories for Rules:**
- Ask don't invent (weight, cube, stairs, shuttle, overtime)
- Rate-from-file / missing rate
- Claims route not adjust
- One Work Item, one folder
- No pay / no PAN / no tariff or DOT legal
- Communication Protocols
- Safety Checks

Present classification to user:
"I've analyzed the documentation and identified the following:"

FACTS (observations/data):
- [Domain: Rate file] 3 new notes about how this shop prices local vs weight
- [Domain: Inventory] 2 new column names on their cube sheet
- [Domain: Claims] 1 new log-owner name

RULES (procedures/constraints):
- [Category: Ask don't invent] 1 new stairs-count rule
- [Category: Rate-from-file] 2 new missing-file asks
- [Category: One folder] 1 filing rule

ROLE UPDATES:
- No new workflow patterns detected

Does this classification look correct?
"(Reply 'yes' to proceed, or tell me what to adjust)"

After user confirms classification, **ask for workflow applicability for each fact/rule**:
"Which workflows does '[fact/rule title]' apply to?"
- Default: "all" (unless content clearly workflow-specific)
- Examples:
 - Stairs extras → estimate-from-rate-file or all
 - Claims log owner → claims-routing or all
 - Rate book location → all
- User can specify "all", a registered job id, or a comma-separated list
- Route `all` to the shared pair; job-scoped to operations

For each **rule**, also ask for `**Triggers:**` (`write:csv`, `write:doc`, `write:estimate`, or `none`).

---

### Step 4: Format Entries

For each fact, use this format:
```markdown
## Domain: [Domain Name]

### YYYY-MM-DD: [Descriptive Title]
**Scope:** expert-role
**Workflows:** [all | estimate-from-rate-file | crew-day | claims-routing | comma-separated job ids]
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
**Workflows:** [all | estimate-from-rate-file | crew-day | claims-routing | comma-separated job ids]
**Triggers:** [write:csv | write:doc | write:estimate | none]
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

**Route each entry:**

| `Workflows:` value | Facts file | Rules file |
|---|---|---|
| `all` | `facts/facts-shared.md` | `facts/rules-shared.md` |
| registered moving-office job id | `facts/facts-operations.md` | `facts/rules-operations.md` |

**Reference-doc option (for large, cross-workflow material):** when the content is a sizable reference
(~50 lines, e.g. a catalog) that several jobs consult, create or
extend a dedicated `facts/<topic>.md` reference doc instead of inflating a workflow file, and add a
pointer to it in `facts/MEMORY-INDEX.md`.

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
- After adding any rule whose Triggers are not `none`, regenerate the index: `python scripts/memory/build_trigger_index.py`

---

### Step 7: Provide Summary

Show user a summary:
```
✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → Domain: Rate file → 5 entries
- facts/facts-operations.md → Domain: Inventory → 2 entries
- facts/facts-operations.md → Domain: Claims → 3 entries

ADDED TO RULES:
- facts/rules-operations.md → Category: Ask don't invent → 1 entry
- facts/rules-operations.md → Category: Rate-from-file → 2 entries
- facts/rules-operations.md → Category: One folder → 1 entry

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
- Keep those files with the Expert folder
- The expert will now use this knowledge on matching jobs
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
- Must-follow procedures (rate from file, claims route not adjust, never invent weight)
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
Can you integrate this claims-routing note I created?
C:\docs\Claims-Routing-Note.md
```

**Agent:**
```
I'll read and integrate the claims-routing note.

[Reads document, analyzes content]

I've analyzed the note and identified:

FACTS (observations/data):
- [Domain: Claims] 1 new entry: who owns the claims log
- [Domain: Claims] 2 photo-naming notes

RULES (procedures/constraints):
- [Category: Claims route not adjust] 3 procedures:
 1. Assemble photos, inventory lines, BOL number
 2. Quote deadline words from their form only
 3. Hand the pack to the person they named

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
- facts/facts-operations.md → Domain: Claims → 3 entries

ADDED TO RULES:
- facts/rules-operations.md → Category: Claims route not adjust → 3 entries

Total new facts: 3
Total new rules: 3

The expert will now reference this shop's claims-routing notes on claims jobs.
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
