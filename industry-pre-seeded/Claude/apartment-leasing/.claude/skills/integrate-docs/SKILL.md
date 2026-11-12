---
name: integrate-docs
description: "Use when the user provides documentation, notes, community policies, leasing playbooks, or PMS export guides to integrate into facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, community-policy PDF notes, required-forms list, hours memo, or similar
- Operator wants this Expert to absorb how *this* shop already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared pair only. Do not create developer or incident-response memory files. Route `Workflows: all` to the shared pair (`facts-shared` / `rules-shared`).

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** hours file location, required application forms, addendum checklist, specials sheet columns, waitlist order field, make-ready codes, guest-card source labels.

**Rules:** never invent a fee, never approve/deny, never copy SSNs, hours file wins, waitlist order theirs, ask when a form is missing.

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by leasing domains (Guest cards & traffic, Showings & hours, Applications & screening files, Lease packets, Make-ready & move-in, Waitlists, Fair-housing operational limits). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each rule, ask **Triggers:** (`none`, `write:doc`, or `write:csv`).

### Step 4: Format and route

Append dated entries (`### YYYY-MM-DD: Title`) to shared files. Rule format must include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate trigger index

After adding or retagging rules, run `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember** — one correction in chat
- **promote-facts-rules** — lift a Work Item note to shop-wide
