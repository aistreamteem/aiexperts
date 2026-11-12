# Trigger Index (action -> rules)

> **GENERATED FILE – do not hand-edit.** Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.
>
> This is the **action axis** of the expert memory. Each rule carries a **Triggers:** field naming the tool-action(s) that should surface it. The preToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads this map and injects the matching rule text at the moment of the action – in **any** workflow, not just the one the rule is filed under. See [MEMORY-INDEX.md](MEMORY-INDEX.md) for the workflow (browsing) axis.

Indexed 35 rules across 1 files; 0 active trigger tokens; 0 rules with no Triggers field.
Hook vocabulary (`KNOWN_TOKENS`): write:doc, write:csv.
