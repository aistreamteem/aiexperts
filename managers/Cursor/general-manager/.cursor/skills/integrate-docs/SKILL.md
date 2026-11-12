---
name: integrate-docs
description: "Use when the operator provides notes, exports, or write-ups to fold into facts, rules, and MyRole.txt."
trigger: User provides notes or says integrate this
---

# Integrate documents

Use this when define-role collects existing notes, and whenever the operator supplies a file or pasted text to remember.

## Steps

1. Ask for file paths, pasted text, or both, plus an optional hint about the topic. "I have no notes" means stop.
2. Read every path. Split the material into facts and rules.
   - Facts: who decides, cadence, stakeholders, historical outcomes, where trackers live.
   - Rules: how status is written, how a decision is recorded, what must be approved, who must be told.
3. Assign each entry to `management-initiative`, `management-escalation`, both, or `all` (shared). Set triggers from: decision:log, status:update, stakeholder:update, escalation:open, cadence:review, write:doc. Include a `**Triggers:**` line on every rule.
4. Hold back people-sensitive notes unless the operator explicitly says to store them in expert-role memory.
5. Show the proposed entries. Store only confirmed ones: `all` goes to the shared pair; otherwise the matching `facts/facts-*.md` or `facts/rules-*.md` files.
6. If a note describes a recurring workflow the registry does not have, propose it for MyRole.txt and, during define-role, put it in the role draft. Do not enable it before approval.
7. Update `facts/MEMORY-INDEX.md` when a new topic needs a pointer.
8. Summarize what was stored, what was skipped, and which files changed. Regenerate the trigger index when rules changed.
