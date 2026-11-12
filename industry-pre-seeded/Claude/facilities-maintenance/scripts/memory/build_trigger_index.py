#!/usr/bin/env python3
"""Build facts/TRIGGER-INDEX.md and facts/trigger-index.json from rules-*.md."""
import importlib.util
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

HEADER_RE = re.compile(r'^(#{2,3})\s+(\d{4}-\d{2}-\d{2}):\s+(.*?)\s*$')
TRIGGERS_RE = re.compile(r'^\*\*Triggers:\*\*\s*(.*?)\s*$')


def slugify(title):
    """GitHub-style anchor slug for a header title."""
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'\s+', '-', s).strip('-')
    return s


def load_known_tokens(hooks_dir: Path) -> set[str]:
    path = hooks_dir / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", path)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tokens = getattr(mod, "KNOWN_TOKENS", [])
    return set(tokens)


def parse_rules(filepath):
    """Yield dict per rule entry with triggers and body."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    entries = []
    current = None
    buf = []

    def flush():
        if current is not None:
            body = "".join(buf).rstrip()
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
                "triggers": None,
                "anchor": slugify(f"{date}-{title}"),
            }
            buf = [raw]
            continue
        if current is not None:
            buf.append(raw)
            if current["triggers"] is None:
                tm = TRIGGERS_RE.match(raw)
                if tm:
                    toks = [t.strip() for t in re.split(r'[,\s]+', tm.group(1)) if t.strip()]
                    current["triggers"] = toks
    flush()
    return entries


def main():
    root = Path(__file__).resolve().parents[2]
    base = root / "facts"
    if not base.is_dir():
        print(f"ERROR: facts/ not found at {base}", file=sys.stderr)
        return 1
    known = load_known_tokens(root / ".claude" / "hooks")
    rules_files = sorted(base.glob("rules-*.md"))
    token_map = defaultdict(list)
    missing = []
    unknown = []
    total = 0
    for fpath in rules_files:
        fname = fpath.name
        for e in parse_rules(fpath):
            total += 1
            if e["triggers"] is None:
                missing.append((fname, e["line"], e["title"]))
                continue
            for tok in e["triggers"]:
                if tok == "none":
                    continue
                if known and tok not in known:
                    unknown.append((fname, e["line"], e["title"], tok))
                token_map[tok].append((fname, e))
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
        f"{len(missing)} rules with no Triggers field."
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
        lines.append("## △ Rules with no **Triggers:** field")
        lines.append("")
        lines.append(
            "_These rules are invisible to the action hook until tagged. "
            "Add a **Triggers:** line (use `none` if truly background-only)._"
        )
        lines.append("")
        for fname, ln, title in missing:
            lines.append(f"- {title} — {fname}:{ln}")
        lines.append("")
    if unknown:
        lines.append("## Rules with a trigger the hook cannot produce")
        lines.append("")
        lines.append(
            "_Token is not in `KNOWN_TOKENS` from `.claude/hooks/inject_rules_on_action.py`._"
        )
        lines.append("")
        for fname, ln, title, tok in unknown:
            lines.append(f"- {title} — {fname}:{ln} (token `{tok}`)")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    json_map = {}
    for tok in sorted(token_map.keys()):
        json_map[tok] = [
            {
                "title": e["title"],
                "file": fname,
                "line": e["line"],
                "body": e["body"],
            }
            for fname, e in token_map[tok]
        ]
    json_out = base / "trigger-index.json"
    json_out.write_text(json.dumps(json_map, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Wrote {json_out}")
    print(f"{total} rules indexed, {len(token_map)} tokens, {len(missing)} missing Triggers")
    if unknown:
        print(f"WARNING: {len(unknown)} rules use tokens the hook cannot produce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
