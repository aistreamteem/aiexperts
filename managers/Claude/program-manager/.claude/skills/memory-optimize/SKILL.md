---
name: memory-optimize
description: "Use when the operator asks to check or clean expert memory. Runs analyze-memory.py against this role's fact and rule files."
trigger: User asks to optimize or check expert memory
---

# Memory optimize

Files in scope:

- `facts/facts-shared.md`
- `facts/rules-shared.md`
- `facts/facts-program-delivery.md`
- `facts/rules-program-delivery.md`
- `facts/facts-program-escalation.md`
- `facts/rules-program-escalation.md`
- `facts/MEMORY-INDEX.md`

## Steps

1. Run `py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts` from this expert's folder.
2. Report file size, entry counts, missing `Workflows` or `Triggers`, and duplicate titles.
3. Thresholds: under 1500 lines per file is healthy. A missing trigger on a rule is a warning. A duplicate title across files needs a look.
4. Propose a short plan before editing: fix metadata, merge true duplicates, refresh MEMORY-INDEX.
5. Edit only after the operator agrees. Do not drop a people-sensitive holdback. Regenerate `python scripts/memory/build_trigger_index.py` after trigger edits.
