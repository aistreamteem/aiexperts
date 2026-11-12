---
name: integrate-docs
description: "Use when the user provides shop documentation, notes, SOP exports, or traveler examples to integrate into shared/operations facts, rules, tools, and MyRole.txt."
---

# integrate-docs

**Purpose:** Fold operator documents into this production-scheduler Expert (facts, rules, tools, role).

**When to use:** They drop an SOP, ERP column list, calendar policy, traveler example, or similar shop documentation.

> **Memory model:** `Workflows: all` → `facts/facts-shared.md` / `facts/rules-shared.md`. Job-specific → `facts/facts-operations.md` / `facts/rules-operations.md`. Large reference material may live as `docs/tools/<topic>.md` plus a MEMORY-INDEX pointer. Do not invent developer or incident-response memory pairs.

## Behavior

1. Ask for path(s) and a short description. Read the documents.
2. Split into **facts** (what their shop files contain), **rules** (must/never), **tools** (how to open an export), **role** (scope changes).
3. Show the classification. Ask workflow applicability: `all` (shared) or a registered job (`dispatch-list`, `kit-list`, …). Default `all`. For each rule, ask for `**Triggers:**` (`none`, `write:doc`, or `write:csv`).
4. Check shared + operations files for duplicates/conflicts. Quote conflicts and ask.
5. Append new entries with header `### YYYY-MM-DD: Title`. Add or update `docs/tools/` when they described an export or app. Update `docs/tools/INDEX.md`. Update MEMORY-INDEX only for new topics.
6. If any rule trigger is not `none`, regenerate the trigger index: `py -3 scripts/memory/build_trigger_index.py`.
7. Propose `MyRole.txt` edits only if scope or must-never changed. Wait for approval.
8. Summarize paths written. **journal-keeper** if a pack is active.

Shop-oriented domains: work orders, routers/travelers, BOM/kit, inventory/shortage, calendar/shifts, work centers, machine-down, outside process, ECO/drawing rev, hot/priority, lot/serial, filing.

This skill does not modify Work Item facts/rules (use **remember** during a pack).

