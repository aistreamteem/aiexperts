---
name: integrate-docs
description: "Use when the user provides clinic notes, packet lists, export headers, or policy PDFs to integrate into shared/operations facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into this clinic front-role expert (facts, rules, and role definition).

**When to use:**
- User provides new documentation to integrate (price files, hours files, boarding forms, PIMS export samples, authorization process notes)
- User wants to update expert knowledge with how *this* clinic files
- User wants to capture institutional knowledge from external sources

**Inputs:**
- Path(s) to document(s) containing knowledge to integrate
- Optional: Domain/category hints from user
- Optional: Fact vs rule classification hints

**Outputs:**
- New facts appended to `facts/facts-shared.md` (`Workflows: all`) or `facts/facts-operations.md`
- New rules appended to `facts/rules-shared.md` (`Workflows: all`) or `facts/rules-operations.md`
- New/updated reference pointer in `facts/MEMORY-INDEX.md` when a new topic appears
- Updated `MyRole.txt` if a new repeating role job is confirmed
- Summary report of what was integrated

> **Memory model (read first):** Always-on (`Workflows: all`) entries go to the **shared** pair;
> job-scoped shop notes go to the **operations** pair. See `facts/MEMORY-INDEX.md`
> and `docs/role/work-item-method.md`. Do not route clinic knowledge into software-build
> or incident-response memory files.

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
- How this clinic names visit types, providers, and day-appointments columns
- Which intake pages they require
- Where authorization PDFs are saved
- Price-file location
- authorization form name and records-release log
- Team contacts for the window (no passwords)

**Rules (constraints, procedures, patterns to follow):**
- Must-never items (no diagnosis, no invented benefits, minimum necessary)
- When to ask (stale book or undated export, missing signature or required page)
- Check-in completeness requirements
- Records-release only on their form
- Safety checks before actions

**Role/Workflow Updates:**
- New pipeline patterns
- Workflow modifications
- Responsibility additions

---

### Step 3: Classify and Organize

Group extracted information by domain/category:

**Common Domains for Facts:**
- Application Architecture
- Environments
- Feature Flags
- Monitoring & Dashboards
- Config Changes
- Database Operations
- Common Errors
- Indexes
- Incident Response
- Local Development
- Testing
- Key Tables
- SQL Queries
- Team Collaboration
- Guardrails
- Codebase Structure

**Common Categories for Rules:**
- Config Change Procedures
- Incident Response
- Data Extension Changes
- Monitoring
- Testing
- Database Operations
- Auto-Indexing
- Code Navigation
- Communication Protocols
- Safety Checks

Present classification to user:
"I've analyzed the documentation and identified the following:"

FACTS (observations/data):
- [Domain: Application Architecture] 3 new entries about application architecture
- [Domain: Monitoring & Dashboards] 2 new dashboard URLs
- [Domain: Codebase Structure] 5 new code paths for feature X

RULES (procedures/constraints):
- [Category: Incident Response] 1 new escalation procedure
- [Category: Testing] 2 new test requirements
- [Category: Communication Protocols] 1 new notification rule

ROLE UPDATES:
- No new workflow patterns detected

Does this classification look correct?
"(Reply 'yes' to proceed, or tell me what to adjust)"

After user confirms classification, **ask for workflow applicability for each fact/rule**:
"Which workflows does '[fact/rule title]' apply to?"
- Default: "all" (shared pair; this role also loads operations for every job)
- Examples: day-appointments column meaning → all; never invent prices → all
- User can specify "all" or a registered job id (`day-appointments`, `new-client-forms`, …)

---

### Step 4: Format Entries

For each fact, use this format:
```markdown
### YYYY-MM-DD: [Descriptive Title]
**Scope:** expert-role
**Workflows:** all
**Captured:** YYYY-MM-DD
**Source:** [Document name/path]
**Status:** active

[Content with full formatting preserved]
```

For each rule, use this format:
```markdown
### YYYY-MM-DD: [Descriptive Title]
**Scope:** expert-role
**Workflows:** all
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** [Document name/path]
**Status:** active

**Rule:** [Clear statement of what must be done]

**Why:** [Reason/context for this rule]
```

---

### Step 5: Integrate into Files

**Route each entry to the correct file by its `Workflows:` value:**

| `Workflows:` value | Facts file | Rules file |
|---|---|---|
| `all` | `facts/facts-shared.md` | `facts/rules-shared.md` |
| any registered role job | `facts/facts-operations.md` | `facts/rules-operations.md` |

Prefer appending into shared (`all`) or operations rather than creating many extra `facts/*.md` files.

1. **Read the existing destination files:**
 - Read shared and operations facts/rules to check for duplicates and conflicts. Consult `facts/MEMORY-INDEX.md`.

2. **Detect duplicates/conflicts:**
 - Check if similar facts already exist (avoid redundancy)
 - Check if rules conflict with existing rules (flag for user review)

3. **Organize:**
 - Append new facts to shared or operations per the routing table
 - Append new rules to shared or operations per the routing table (include `**Triggers:**`)

4. **Update MEMORY-INDEX.md if needed:**
 - If a new high-value topic emerged, add a pointer under Operations.

5. **Update MyRole.txt if needed:**
 - If a new repeating role job is confirmed, propose a workflow file + registry entry
 - If new responsibilities identified, propose updates to role description

---

### Step 6: Write Updates

Use the Edit tool to add new entries to shared or operations facts/rules per the routing table (and
`facts/MEMORY-INDEX.md` if a new topic pointer is needed). After rules with non-`none` triggers, regenerate the trigger index.

**Important:**
 - Preserve all existing content
- Add new entries at the end of their respective domain/category sections
- Maintain consistent formatting
- Include source attribution

---

### Step 7: Provide Summary

Show user a summary:
```
✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → 3 entries (visit types, new-client packet, price file)

ADDED TO RULES:
- facts/rules-operations.md → 2 entries (stale book or undated export ask, missing signature or required page)

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
- The expert will now use this knowledge on clinic-role Work Items
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
Can you integrate this packet list I saved?
C:\clinic\new-patient-packet-pages.md
```

**Agent:**
```
I'll read and integrate the new-patient packet list.

[Reads document, analyzes content]

I've analyzed the file and identified:

FACTS:
- Named pages in the new-patient packet
- Where the required signaturenowledgment is filed

RULES:
- Do not mark intake complete without required signature or declined-to-sign

Does this classification look correct?
```

**User:**
```yes
```

**Agent:**
```
[Appends to facts-operations.md and rules-operations.md]

✓ Documentation Integration Complete

ADDED TO FACTS:
- facts/facts-operations.md → new-patient packet pages

ADDED TO RULES:
- facts/rules-operations.md → missing signature or required page ask

Total new facts: 1
Total new rules: 1

The expert will use this on new-client-forms Work Items.
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


After importing rules, regenerate the trigger index: `python scripts/memory/build_trigger_index.py`.
