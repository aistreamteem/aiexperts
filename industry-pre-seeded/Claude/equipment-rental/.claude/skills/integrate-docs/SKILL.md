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
- New facts appended to `facts/facts-shared.md` (or the active Work Item `work-items/<id>/facts/facts.md`)
- New rules appended to `facts/rules-shared.md` (or the active Work Item `work-items/<id>/facts/rules.md`)
- Pointer added to `facts/MEMORY-INDEX.md` when a new topic is worth finding later
- Updated `MyRole.txt` if new rental-role job patterns are detected
- Summary report of what was integrated

> **Memory model (read first):** This Expert stores role memory in operations files:
> `facts/facts-shared.md` and `facts/rules-shared.md`. Set `**Workflows:**` to
> `all` or a registered job id. See `facts/MEMORY-INDEX.md` and `facts/HOW-MEMORY-LOADING-WORKS.md`.

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
- How this yard names fleet items, categories, serials, and statuses
- Where rate, zone, COI, PM, and meter files live
- Column names on their exports
- What a contract, reservation, or inspection sheet contains
- Historical context (why this yard files a certain way)
- Tool locations (folders, spreadsheets) — never passwords

**Rules (constraints, procedures, patterns to follow):**
- Required contract / inspection / COI fields
- When to hold the gate or ask
- What must never be invented (rates, meters, serials, fees)
- Required photos for damage
- Utilization formula as they wrote it
- Out-of-scope refusals already in `MyRole.txt`

**Role/Workflow Updates:**
- New pipeline patterns
- Workflow modifications
- Responsibility additions

---

### Step 3: Classify and Organize

Group extracted information by domain/category:

**Common Domains for Facts:**
- Fleet and serials
- Rates and fees
- Reservations and contracts
- Inspections and photos
- COI and renter account
- Delivery and zones
- Meters and utilization
- Maintenance due
- How we file Work Items

**Common Categories for Rules:**
- Rates only from their file
- No invented hours, zones, or deposits
- Inspection both ways
- COI completeness (not a coverage opinion)
- Ask on missing serial / meter / contract fields
- Stay inside the rental-role role

Present classification to user:
"I've analyzed the documentation and identified the following:"

FACTS (observations/data):
- [Domain: Fleet and serials] 3 new entries about how this yard names units
- [Domain: Rates and fees] 2 new notes about the rate-file location
- [Domain: COI and renter account] 1 new folder path

RULES (procedures/constraints):
- [Category: Ask on missing contract fields] 1 new required-field list
- [Category: Rates only from their file] 2 new constraints
- [Category: Stay inside the rental-role role] 1 new refusal

ROLE UPDATES:
- No new workflow patterns detected

Does this classification look correct?
"(Reply 'yes' to proceed, or tell me what to adjust)"

After user confirms classification, **ask for workflow applicability for each fact/rule**:
"Which workflows does '[fact/rule title]' apply to?"
- Default: "all" (unless content is clearly one registered job)
- Examples:
 - Rate-file location → all
 - Outgoing inspection photo rule → outgoing-inspection or all
 - Today-only export filename → keep at Work Item scope
- User can specify "all" or a registry job id

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
**Triggers:** write:doc | write:csv | none
**Captured:** YYYY-MM-DD
**Source:** [Document name/path]
**Rule:** [Clear statement of what must be done]

**Why:** [Reason/context for this rule]

**How to apply:**
[Step-by-step application instructions]

**Violation:** [Consequence of not following this rule]

---
```

When classifying a rule in step 3, also ask which action trigger fits (`write:doc`, `write:csv`, or `none`).

---

### Step 5: Integrate into Files

**Route each entry to shared memory (this role has no developer/incident split):**

| Scope | Facts file | Rules file |
|---|---|---|
| Expert Role | `facts/facts-shared.md` | `facts/rules-shared.md` |
| This Work Item only | `work-items/<id>/facts/facts.md` | `work-items/<id>/facts/rules.md` |

1. **Read the existing destination files:**
 - Read `facts/facts-shared.md` and/or `facts/rules-shared.md` (or the Work Item files) to check for duplicates and conflicts. Consult `facts/MEMORY-INDEX.md`.

2. **Detect duplicates/conflicts:**
 - Check if similar facts already exist (avoid redundancy)
 - Check if rules conflict with existing rules (flag for user review)

3. **Organize by domain/category:**
 - Add new facts to `facts/facts-shared.md` (or the Work Item facts file)
 - Add new rules to `facts/rules-shared.md` (or the Work Item rules file)
 - Create new domain/category sections if needed

4. **Update MEMORY-INDEX.md if needed:**
 - If a new reference doc was created or a new high-value scenario emerged, add a line to the
    reference list and/or a "Common Scenarios → Memory References" entry so it is discoverable.

5. **Update MyRole.txt if needed:**
 - If new workflow patterns detected, propose additions to pipeline definitions
 - If new responsibilities identified, propose updates to role description

---

### Step 6: Write Updates

Use the Edit tool to add new entries to `facts/facts-shared.md` / `facts/rules-shared.md` (and
`facts/MEMORY-INDEX.md` when a new topic needs a pointer).

**Important:**
 - Preserve all existing content
- Add new entries at the end of their respective domain/category sections
- Maintain consistent formatting
- Include source attribution
 - After appending any rule whose `Triggers:` is not `none`, regenerate the trigger index: `py -3 scripts/memory/build_trigger_index.py`

---

### Step 7: Provide Summary

Show user a summary:
```
✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-shared.md → Domain: Fleet and serials → 3 entries
- facts/facts-shared.md → Domain: Rates and fees → 2 entries

ADDED TO RULES:
- facts/rules-shared.md → Category: Ask on missing contract fields → 1 entry
- facts/rules-shared.md → Category: Stay inside the rental-role role → 1 entry

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
Can you integrate this yard note I created?
C:\docs\COI-checklist.md
```

**Agent:**
```
I'll read and integrate the COI checklist.

[Reads document, analyzes content]

I've analyzed the note and identified:

FACTS (observations/data):
- [Domain: COI and renter account] 1 new entry: commercial jobs use the COI folder
- [Domain: Rates and fees] 2 new notes about which rate-file tab to read

RULES (procedures/constraints):
- [Category: COI completeness] 3 new procedures:
 1. Compare named insured to the renter name
 2. Check dates cover the rental
 3. List missing certificates; do not give a coverage opinion

Does this classification look correct?
```

**User:**
```yes
```

**Agent:**
```
[Routes content into shared memory for this rental role]

✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-shared.md → Domain: COI and renter account → 1 entry
- facts/facts-shared.md → Domain: Rates and fees → 2 entries

ADDED TO RULES:
- facts/rules-shared.md → Category: Ask on missing contract fields → 3 entries

Total new facts: 3
Total new rules: 3

The expert will now use these yard notes on the next contract-completeness job.
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
