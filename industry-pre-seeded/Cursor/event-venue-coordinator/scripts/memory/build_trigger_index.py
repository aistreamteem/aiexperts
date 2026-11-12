#!/usr/bin/env python3
"""Build facts/TRIGGER-INDEX.md – the action-trigger axis of the expert memory.

This role loads shared rules. The thing that predicts *when* a rule is needed is
the ACTION the agent is about to take (write a .md pack, write a .csv). This
script scans every rules-*.md entry for a `**Triggers:**` line and emits:
1. facts/TRIGGER-INDEX.md
2. facts/trigger-index.json
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HEADER_RE = re.compile(r"^(#{2,3})\s+(\d{4}-\d{2}-\d{2}):\s+(.*?)\s*$")
TRIGGERS_RE = re.compile(r"^\*\*Triggers:\*\*\s*(.*?)\s*$")


def load_known_tokens(root: Path) -> list[str]:
    hook = root / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return []
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(getattr(module, "KNOWN_TOKENS", []) or [])


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s


def parse_rules(filepath: Path):
    lines = filepath.read_text(encoding="utf-8").splitlines(keepends=True)
    entries = []
    current = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal current, buf
        if current is not None:
            body = "".join(buf).rstrip()
            body = re.sub(r"\n-{3,}\s*$", "", body).rstrip()
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
                    toks = [
                        t.strip()
                        for t in re.split(r"[,\s]+", tm.group(1))
                        if t.strip()
                    ]
                    current["triggers"] = toks
    flush()
    return entries


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    base = root / "facts"
    if not base.is_dir():
        print(f"ERROR: facts/ not found at {base}", file=sys.stderr)
        return 1
    known = set(load_known_tokens(root))
    rules_files = sorted(path.name for path in base.glob("rules-*.md"))
    token_map: dict[str, list] = defaultdict(list)
    missing = []
    unknown = []
    total = 0
    for fname in rules_files:
        fpath = base / fname
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
    lines = [
        "# Trigger Index (action -> rules)",
        "",
        "> **GENERATED FILE – do not hand-edit.** Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.",
        ">",
        "> This is the **action axis** of the expert memory. Each rule carries a **Triggers:** field naming the tool-action(s) that should surface it. The preToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads this map and injects the matching rule text at the moment of the action – in **any** workflow, not just the one the rule is filed under. See [MEMORY-INDEX.md](MEMORY-INDEX.md) for the workflow (browsing) axis.",
        "",
        f"Indexed {total} rules across {len(rules_files)} files; "
        f"{len(token_map)} active trigger tokens; "
        f"{len(missing)} rules with no Triggers field.",
        "",
    ]
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
        lines.append("## △ Rules with a trigger the hook cannot produce")
        lines.append("")
        lines.append(
            "_These tokens are not in `KNOWN_TOKENS` from "
            "`.cursor/hooks/inject_rules_on_action.py`._"
        )
        lines.append("")
        for fname, ln, title, tok in unknown:
            lines.append(f"- {title} (`{tok}`) — {fname}:{ln}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    json_map = {
        tok: [
            {
                "title": e["title"],
                "file": fname,
                "line": e["line"],
                "body": e["body"],
            }
            for fname, e in token_map[tok]
        ]
        for tok in sorted(token_map.keys())
    }
    json_out = base / "trigger-index.json"
    json_out.write_text(json.dumps(json_map, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Wrote {json_out}")
    print(
        f"{total} rules indexed, {len(token_map)} tokens, "
        f"{len(missing)} missing Triggers, {len(unknown)} unknown tokens"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
