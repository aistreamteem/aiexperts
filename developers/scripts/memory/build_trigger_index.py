#!/usr/bin/env python3
"""Build facts/TRIGGER-INDEX.md and facts/trigger-index.json: the action-trigger axis of the expert memory.

The workflow-split rules files (facts/rules-*.md) are the *browsing / context-budget*
axis: they are loaded by session type (shared plus the current workflow). But the
thing that predicts *when* a rule is needed is the ACTION the agent is about to take
(write a .sql file, open a PR, push). Those actions cut across workflows, so a rule
filed under one workflow is invisible in the others.

This script scans every facts/rules-*.md for entries with a `**Triggers:**` line and
emits two artifacts:

1. facts/TRIGGER-INDEX.md   - human-readable `token -> [rule, ...]` map.
2. facts/trigger-index.json - machine-readable `{token: [{title, file, line, body}]}`
   consumed by the PreToolUse hook (.claude/hooks/inject_rules_on_action.py) so it can
   inject the FULL rule text at the moment of the action, in ANY workflow.

When the hook module is importable, its KNOWN_TOKENS table is the trigger vocabulary:
a rule tagged with a token outside it can never be surfaced, so it is listed under
"Rules with a trigger the hook cannot produce" and reported as a warning.

GENERATED FILES - never hand-edit either. Re-run after adding or retagging a rule:

    python scripts/memory/build_trigger_index.py

Standard library only.
"""
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"

# Header for an entry: "### 2026-06-17: Title" or "## 2026-07-30: Title"
HEADER_RE = re.compile(r'^(#{2,3})\s+(\d{4}-\d{2}-\d{2}):\s+(.*?)\s*$')
TRIGGERS_RE = re.compile(r'^\*\*Triggers:\*\*\s*(.*?)\s*$')


def load_known_tokens():
    """KNOWN_TOKENS from the rules hook, or None when the hook cannot be imported."""
    if not HOOK_PATH.is_file():
        return None
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("inject_rules_on_action", HOOK_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return set(module.KNOWN_TOKENS)
    except Exception as exc:  # noqa: BLE001 - any import failure means "unknown vocabulary"
        print(f"WARNING: could not import KNOWN_TOKENS from {HOOK_PATH.name}: {exc}", file=sys.stderr)
        return None


def slugify(title):
    """GitHub-style anchor slug for a header title."""
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'\s+', '-', s).strip('-')
    return s


def parse_rules(filepath):
    """Return one dict per rule entry: {date, title, line, triggers, anchor, body}.

    An entry runs from its header to the next header (or EOF). The **Triggers:** line
    inside the block is parsed; the full block text is kept as 'body' (header included,
    trailing '---' and blank lines trimmed). triggers is None when the field is missing.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    entries = []
    current = None
    buf = []

    def flush():
        if current is not None:
            body = "".join(buf).rstrip()
            # Drop a trailing horizontal-rule separator so injected text is clean.
            body = re.sub(r'\n-{3,}\s*$', '', body).rstrip()
            current["body"] = body
            entries.append(current)

    for i, raw in enumerate(lines):
        m = HEADER_RE.match(raw)
        if m:
            flush()
            _, date, title = m.groups()
            current = {
                "date": date,
                "title": title,
                "line": i + 1,
                "triggers": None,  # None => field missing entirely
                "anchor": slugify(f"{date}-{title}"),
            }
            buf = [raw]
            continue
        if current is not None:
            buf.append(raw)
            if current["triggers"] is None:
                tm = TRIGGERS_RE.match(raw)
                if tm:
                    current["triggers"] = [t.strip() for t in re.split(r'[,\s]+', tm.group(1)) if t.strip()]
    flush()
    return entries


def main():
    base = ROOT / "facts"
    if not base.is_dir():
        print(f"ERROR: facts/ not found at {base}", file=sys.stderr)
        return 1
    rules_files = sorted(p.name for p in base.glob("rules-*.md"))
    if not rules_files:
        print("WARNING: no facts/rules-*.md files found", file=sys.stderr)
    known = load_known_tokens()
    if known is None:
        print("WARNING: trigger vocabulary unavailable; not checking for unknown tokens", file=sys.stderr)

    token_map = defaultdict(list)  # token -> [(file, entry), ...]
    missing = []  # rules with no **Triggers:** line at all
    unknown = []  # (file, line, title, [bad tokens])
    total = 0
    for fname in rules_files:
        for e in parse_rules(base / fname):
            total += 1
            if e["triggers"] is None:
                missing.append((fname, e["line"], e["title"]))
                continue
            bad = []
            for tok in e["triggers"]:
                if tok == "none":
                    continue
                if known is not None and tok not in known:
                    bad.append(tok)
                    continue
                token_map[tok].append((fname, e))
            if bad:
                unknown.append((fname, e["line"], e["title"], bad))

    # --- Emit TRIGGER-INDEX.md ---
    out = base / "TRIGGER-INDEX.md"
    lines = []
    lines.append("# Trigger Index (action -> rules)")
    lines.append("")
    lines.append("> **GENERATED FILE – do not hand-edit.** Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.")
    lines.append(">")
    lines.append("> This is the **action axis** of the expert memory. Each rule carries a **Triggers:** field naming the tool-action(s) that should surface it. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads this map and injects the matching rule text at the moment of the action – in **any** workflow, not just the one the rule is filed under. See [MEMORY-INDEX.md](MEMORY-INDEX.md) for the workflow (browsing) axis.")
    lines.append("")
    lines.append(
        f"Indexed {total} rules across {len(rules_files)} files; "
        f"{len(token_map)} active trigger tokens; "
        f"{len(missing)} rules with no Triggers field; "
        f"{len(unknown)} rules with an unknown trigger."
    )
    lines.append("")
    for tok in sorted(token_map.keys()):
        rules = token_map[tok]
        lines.append(f"## {tok} ({len(rules)})")
        lines.append("")
        for fname, e in rules:
            link = f"{fname}#{e['anchor']}"
            lines.append(f"- [{e['title']}]({link}) — {fname}:{e['line']}")
        lines.append("")
    if missing:
        lines.append("## Rules with no **Triggers:** field")
        lines.append("")
        lines.append("_These rules are invisible to the action hook until tagged. Add a **Triggers:** line (use `none` if truly background-only)._")
        lines.append("")
        for fname, ln, title in missing:
            lines.append(f"- {title} — {fname}:{ln}")
        lines.append("")
    if unknown:
        lines.append("## Rules with a trigger the hook cannot produce")
        lines.append("")
        lines.append("_The hook only produces the tokens in `KNOWN_TOKENS` (`.claude/hooks/inject_rules_on_action.py`). Retag these rules with a listed token, or add the token to the hook._")
        lines.append("")
        for fname, ln, title, bad in unknown:
            lines.append(f"- {title} — {fname}:{ln} — unknown: {', '.join(bad)}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")

    # --- Emit trigger-index.json (machine-readable, for the hook) ---
    json_map = {}
    for tok in sorted(token_map.keys()):
        json_map[tok] = [
            {"title": e["title"], "file": fname, "line": e["line"], "body": e["body"]}
            for fname, e in token_map[tok]
        ]
    json_out = base / "trigger-index.json"
    json_out.write_text(json.dumps(json_map, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {out}")
    print(f"Wrote {json_out}")
    print(f"{total} rules indexed, {len(token_map)} tokens, {len(missing)} missing Triggers, {len(unknown)} unknown triggers")
    for tok in sorted(token_map.keys()):
        print(f"  {tok}: {len(token_map[tok])}")
    if missing:
        print(f"WARNING: {len(missing)} rules have no **Triggers:** line (listed in the index)")
    for fname, ln, title, bad in unknown:
        print(f"WARNING: {fname}:{ln} '{title}' uses unknown trigger(s): {', '.join(bad)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
