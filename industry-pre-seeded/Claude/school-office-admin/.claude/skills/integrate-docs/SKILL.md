---
name: integrate-docs
description: "Use when the user provides documentation, notes, handbooks, policy PDFs, or giving-software export guides to integrate into facts, rules, and MyRole.txt."
disable-model-invocation: false
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, child-protection policy, statement-process file, fund chart, or similar
- Operator wants this Expert to absorb how *this* office already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Operations only. Do not create developer or incident-response memory files.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** giving-software export columns, count-sheet batch id, fund chart location, statement process, volunteer role list, COI checklist, board-packet page list, calendar file location.

**Rules:** never invent a fund, never give a tax opinion, never move money, never decide a background verdict, calendar from their file, handbook PDF wins.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by school-office domains (Giving & funds, Calendars & rooms, Volunteers & background dates, Facility & COI, Board/session packs, Statements & pledges). Confirm with the operator. Ask workflow applicability (`all` or registry ids).

### Step 4: Format and route

Append dated entries to shared files. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

## Complements

- Single correction → **remember**
- Elevate a Work Item note → **promote-facts-rules**
