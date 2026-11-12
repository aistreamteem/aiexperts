---
name: integrate-docs
description: "Use when the user provides documentation, notes, SOPs, PMS export samples, or policy PDFs to integrate into the expert system (facts, rules, and MyRole.txt role definition)."
---

# integrate-docs

**Purpose:** Integrate documentation, notes, or knowledge artifacts into the hotel-role expert (facts, rules, and role definition).

**When to use:**
- User provides new documentation (property SOP, rate-grid notes, tax-file legend, group-contract extract, PMS column map)
- User wants to update expert knowledge with how *this* inn works
- User wants to capture institutional knowledge from external sources

**Inputs:**
- Path(s) to document(s)
- Optional: domain hints, fact vs rule hints

**Outputs:**
- New facts in `facts/facts-operations.md`
- New rules in `facts/rules-operations.md`
- Optional pointer on `facts/MEMORY-INDEX.md`
- Updated `MyRole.txt` if new repeating jobs appear
- Summary of what was integrated

> **Memory model:** This role uses operations memory only (`facts-operations.md` / `rules-operations.md`).

---

## Behavior

### Step 1: Gather Documents

Ask for file path(s), a brief description, and whether this is primarily facts or rules. Read the documents.

### Step 2: Analyze Content

**Facts:** PMS column meanings, room-type codes, house-count legend, which flash line is official ADR, where BEOs live, DNR list owner.

**Rules:** Never invent a rate; tax-exempt needs a cert; night audit they run; ask when export missing; no PAN in this folder.

**Role/workflow updates:** A repeating job that is not yet in `workflow-registry.json`.

### Step 3: Classify and Organize

Group by role domain (arrivals, folios, groups, tax, rooms, night audit). Present the classification and ask whether it looks correct. Default workflow applicability: **all**.

### Step 4: Format Entries

Use the operations entry format (`### YYYY-MM-DD: Title`, Scope, Workflows: all, Source). Rules include **Rule:** / **Why:** / **Triggers:** (`write:doc`, `write:csv`, or `none`). Ask for Triggers when capturing a rule.

### Step 5: Integrate into Files

1. Read existing `facts-operations.md` / `rules-operations.md` for duplicates and conflicts.
2. Flag conflicts for the operator (their file wins over starter notes).
3. Append new entries. Update MEMORY-INDEX if a new browsing topic appears.
4. Propose MyRole / registry updates only for new repeating jobs.

### Step 6: Write Updates

Preserve existing content. Add new entries at the end of the operations file. Include source attribution. After a non-`none` rule trigger, regenerate `py -3 scripts/memory/build_trigger_index.py`.

### Step 7: Provide Summary

List facts added, rules added, conflicts, and next steps (operator backup of the Expert folder).

---

### Edge Cases

- Large docs: chunk and show progress.
- Ambiguous fact vs rule: ask.
- Conflicting rules: show both; operator chooses; starter notes yield to *this* property.
- Outdated facts: supersede with a note.

### Complements

- **remember**: one fact/rule during conversation
- **promote-facts-rules**: Work Item → Expert Role
- This skill: batch from existing documents into operations memory
