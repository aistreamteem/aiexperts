---
name: integrate-docs
description: "Use when the user provides documentation, notes, handbooks, policy PDFs, or grant/donor procedure guides to integrate into facts, rules, and MyRole.txt."
disable-model-invocation: false
---

# integrate-docs

**Purpose:** Integrate shop documentation into Expert Role shared memory and, when needed, the role definition.

**When to use:**
- Operator drops a handbook, gift-acceptance policy, board-packet checklist, grant manual, or similar
- Operator wants this Expert to absorb how *this* office already works

**Outputs:**
- New facts in `facts/facts-shared.md`
- New rules in `facts/rules-shared.md`
- Optional tool stub under `docs/tools/`
- Pointer in `facts/MEMORY-INDEX.md` for a large reference
- `MyRole.txt` / workflow stubs only if a new recurring job is clearly named
- Summary report

> **Memory model:** Shared pair only. Do not create developer or incident-response memory files. `Workflows: all` or a registry job id routes within the shared files.

## Behavior

### Step 1: Gather documents

Ask for path(s) and whether the content is mostly facts (what is true) or rules (what must / must never).

### Step 2: Analyze

**Facts:** award-file layout, fiscal year, board-packet page list, donor CSV columns, ack template location, minutes draft vs adopted, restricted-fund coding notes.

**Rules:** never invent compliance, never move money, never give a deductibility opinion, never treat restricted cash as unrestricted, produce lists (they communicate with donors).

**Role/workflow:** a new named recurring job (only if they want a map).

### Step 3: Classify

Group by nonprofit-office domains (Grants and awards, Board packets and minutes, Donor records, Restricted funds, In-kind and unusual gifts). Confirm with the operator. Ask workflow applicability (`all` or registry ids). For each **rule**, ask action trigger: `none` | `write:doc` | `write:csv` (must match `KNOWN_TOKENS` in `.claude/hooks/inject_rules_on_action.py`).

### Step 4: Format and route

Append dated entries to shared files using `### YYYY-MM-DD: Title` headers. Rules include `**Triggers:**`. Large cross-job reference → `facts/<topic>.md` plus MEMORY-INDEX pointer. Check duplicates and conflicts; ask which wording wins.

### Step 5: Summary

List what was added. Do not treat starter public practice as this shop’s policy unless they said it is.

### Step 6: Regenerate trigger index

After adding or retagging any rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

- Single correction → **remember**
- Elevate a Work Item note → **promote-facts-rules**
