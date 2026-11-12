---
name: integrate-docs
description: "Use when the user provides documentation, notes, handbooks, policy PDFs, or SIS export guides to integrate into facts, rules, and MyRole.txt."
disable-model-invocation: false
---

# integrate-docs

**Purpose:** Integrate office documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, records-process file, enrollment checklist, immunization log guide, or similar
- Operator wants this Expert to absorb how *this* office already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared pair only. Do not create developer or incident-response memory files. Route `Workflows: all` into the shared pair.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** SIS export columns, attendance codes, packet checklist location, immunization log layout, pickup-list file, calendar file location, tuition sheet, waitlist order.

**Rules:** never invent grades, never release records without their process, never copy SSNs, pickup list wins, handbook PDF wins, immunization is present-or-missing only.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by school-office domains (Attendance, Enrollment packets, Immunization files, Calendars, Pickup/dismissal, Records/transcripts, Tuition files, Waitlist). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask Triggers: `none` | `write:doc` | `write:csv`.

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to shared files. Include `**Triggers:**` on every rule. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this office’s policy unless they said it is.

### Step 6: Regenerate trigger index

After adding or retagging any rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

- Single correction → **remember**
- Elevate a Work Item note → **promote-facts-rules**
