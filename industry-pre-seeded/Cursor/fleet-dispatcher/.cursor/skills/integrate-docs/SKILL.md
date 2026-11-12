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
- New facts routed into `facts/facts-operations.md`
- New rules routed into `facts/rules-operations.md`
- New/updated reference doc in `facts/` (e.g. a shop reference topic file) for large,
 cross-workflow reference material, with a pointer added to `facts/MEMORY-INDEX.md`
- Updated `facts/MEMORY-INDEX.md` navigation (reference list / Common Scenarios) so new knowledge is discoverable
- Updated `MyRole.txt` if new workflow patterns detected
- Summary report of what was integrated

> **Memory model (read first):** This role’s Expert Role memory is
> `facts/facts-operations.md` and `facts/rules-operations.md`. Each fact/rule
> carries a `Workflows:` field (`all` or a registered role job id). See
> `facts/MEMORY-INDEX.md` and `facts/HOW-MEMORY-LOADING-WORKS.md`.

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
- Roster, unit, trailer, and driver field names this shop uses
- How POD, DVIR, ELD, GPS, and fuel files are named
- Customer standing notes, exception codes, site hours
- Historical context (why this fleet files a day that way)
- Tool locations (TMS export path, ELD vendor they already use — not a sale)

**Rules (constraints, procedures, patterns to follow):**
- Must-never items (no invented GPS/ETA/POD/DVIR, no HOS legal stamp)
- Required steps in a dispatch pack
- When to ask vs when a missing file is just "missing"
- Who reviews fuel/HOS questions
- What may go in a widely emailed pack

**Role/Workflow Updates:**
- New role jobs to register
- Workflow modifications
- Responsibility additions

---

### Step 3: Classify and Organize

Group extracted information by domain/category:

**Common Domains for Facts:**
- Roster and assignment
- Routes, stops, windows
- DVIR and equipment
- POD and BOL
- Exceptions, breakdown, detention
- ELD / HOS files
- Fuel and IFTA files
- GPS / telematics
- Customer and site notes
- How we file work items

**Common Categories for Rules:**
- Do not invent
- Ask when missing
- One day / one unit / one folder
- Flag, do not accuse
- Secrets and passwords
- FMCSA is orientation only

Present classification to user:
"I've analyzed the documentation and identified the following:"

FACTS (observations/data):
- [Domain: Roster and assignment] 3 new entries about roster columns
- [Domain: POD and BOL] 2 new POD file-name patterns
- [Domain: ELD / HOS files] 1 new export header they use

RULES (procedures/constraints):
- [Category: Do not invent] 1 new no-invent-ETA note
- [Category: Ask when missing] 2 new missing-DVIR questions
- [Category: Secrets and passwords] 1 new no-gate-codes note

ROLE UPDATES:
- No new workflow patterns detected

Does this classification look correct?
"(Reply 'yes' to proceed, or tell me what to adjust)"

After user confirms classification, **ask for workflow applicability for each fact/rule**:
"Which workflows does '[fact/rule title]' apply to?"
- Default: "all" (unless content clearly workflow-specific)
- Examples:
 - Inspection file names → dvir-gap
 - Signature-required flag → pod-check
 - Roster columns → assignment-pack / all
- User can specify "all", a registered role job id, or a comma-separated list

---

### Step 4: Format Entries

For each fact, use this format:
```markdown
## Domain: [Domain Name]

### YYYY-MM-DD: [Descriptive Title]
**Scope:** expert-role
**Workflows:** [all | registered role job id | comma-separated]
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
**Workflows:** [all | registered role job id | comma-separated]
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
| `all` | `facts/facts-shared.md` | `facts/rules-shared.md` |
| any registered role job | `facts/facts-operations.md` | `facts/rules-operations.md` |

**Reference-doc option (for large, cross-workflow material):** when the content is a sizable reference
(~50 lines, e.g. a schema, a catalog, validator internals) that several workflows consult, create or
extend a dedicated `facts/<topic>.md` reference doc instead of inflating a workflow file, and add a
pointer to it in `facts/MEMORY-INDEX.md` (reference list + a Common Scenarios entry). This mirrors the
existing MEMORY-INDEX pointer pattern.

1. **Read the existing destination files:**
 - Read the shared and/or operations destination from the routing table (or the reference doc)
    to check for duplicates and conflicts. Consult `facts/MEMORY-INDEX.md`.

2. **Detect duplicates/conflicts:**
 - Check if similar facts already exist (avoid redundancy)
 - Check if rules conflict with existing rules (flag for user review)

3. **Organize by domain/category:**
 - Route `Workflows: all` to the shared pair; registered job ids to the operations pair
 - Create new domain/category sections if needed
 - For each **rule**, ensure a `**Triggers:**` line (`write:doc`, `write:csv`, or `none`)

4. **Update MEMORY-INDEX.md if needed:**
 - If a new reference doc was created or a new high-value scenario emerged, add a line to the
    reference list and/or a "Common Scenarios → Memory References" entry so it is discoverable.

5. **Update MyRole.txt if needed:**
 - If new workflow patterns detected, propose additions to pipeline definitions
 - If new responsibilities identified, propose updates to role description

---

### Step 6: Write Updates

Use the Edit tool to add new entries to the shared or operations files from the routing table (and
any reference doc + `facts/MEMORY-INDEX.md` pointer). After appending rules whose Triggers are not
`none`, regenerate `python scripts/memory/build_trigger_index.py`.

**Important:**
 - Preserve all existing content
- Add new entries at the end of their respective domain/category sections
- Maintain consistent formatting (`### YYYY-MM-DD: Title`)
- Include source attribution

---

### Step 7: Provide Summary

Show user a summary:
```
✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → Domain: Roster and assignment → 5 entries
- facts/facts-operations.md → Domain: POD and BOL → 2 entries
- facts/facts-operations.md → Domain: ELD / HOS files → 3 entries

ADDED TO RULES:
- facts/rules-operations.md → Category: Do not invent → 1 entry
- facts/rules-operations.md → Category: Ask when missing → 2 entries
- facts/rules-operations.md → Category: Secrets and passwords → 1 entry

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
- Must-follow procedures (dispatch packs, missing-file questions)
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
Can you integrate this new dispatch SOP I created?
C:\docs\Morning-Board-SOP.md
```

**Agent:**
```
I'll read and integrate the morning-board SOP.

[Reads document, analyzes content]

I've analyzed the SOP and identified:

FACTS (observations/data):
- [Domain: Roster and assignment] 1 new entry: How this shop names spare units
- [Domain: DVIR and equipment] 2 new notes on tractor vs trailer files

RULES (procedures/constraints):
- [Category: Ask when missing] 3 new procedures:
 1. Ask if today's DVIR folder is empty
 2. Ask which date is live when a reschedule moved a stop
 3. Leave blank driver columns blank unless they asked for a labeled draft

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
- facts/facts-operations.md → Domain: Roster and assignment → 1 entry
- facts/facts-operations.md → Domain: DVIR and equipment → 2 entries

ADDED TO RULES:
- facts/rules-operations.md → Category: Ask when missing → 3 entries

Total new facts: 3
Total new rules: 3

The expert will now reference the morning-board SOP on assignment, routes, and DVIR packs.
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
- **Route to operations memory**: write to `facts/facts-operations.md` / `facts/rules-operations.md`.
 Large reference material may go in a dedicated `facts/<topic>.md` pointer from `MEMORY-INDEX.md`.
