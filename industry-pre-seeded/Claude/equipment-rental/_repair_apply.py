"""One-shot repair apply for Claude/equipment-rental. Delete after use."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent.parent / "Cursor" / "equipment-rental"
BAKERY = ROOT.parent / "bakery-cafe-admin"

CONTEXT_BLOCK = """### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.
"""


def adapt_cursor(text: str) -> str:
    text = text.replace(".cursor", ".claude")
    text = text.replace("AGENTS.md", "CLAUDE.md")
    text = text.replace("Cursor Agent Skills", "Claude skills")
    text = text.replace("`.cursor/rules/expert.mdc`", "`.claude/rules/expert.md`")
    text = text.replace("expert.mdc", "expert.md")
    text = text.replace("hooks.json", "settings.json")
    text = text.replace("sessionStart`, `beforeSubmitPrompt`, or `preToolUse`", "PreToolUse / Stop hooks")
    text = text.replace("preToolUse", "PreToolUse")
    text = text.replace("subagentStop", "SubagentStop")
    text = text.replace("stop/", "Stop/")
    # memory rename (D4)
    text = text.replace("facts/facts-operations.md", "facts/facts-shared.md")
    text = text.replace("facts/rules-operations.md", "facts/rules-shared.md")
    text = text.replace("facts-operations.md", "facts-shared.md")
    text = text.replace("rules-operations.md", "rules-shared.md")
    text = text.replace("operations memory", "shared memory")
    text = text.replace("Operations memory", "Shared memory")
    text = text.replace("Expert Role operations memory", "Expert Role shared memory")
    return text


def copy_adapted(rel: str, dst_rel: str | None = None) -> None:
    src = SRC / rel
    dst = ROOT / (dst_rel or rel)
    if not src.is_file():
        print(f"SKIP missing {rel}")
        return
    text = adapt_cursor(src.read_text(encoding="utf-8"))
    # script paths that still say .cursor in comments after adapt are fine
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8", newline="\n")
    print(f"copied {rel} -> {dst.relative_to(ROOT)}")


def rename_memory() -> None:
    mapping = {
        "facts-operations.md": "facts-shared.md",
        "rules-operations.md": "rules-shared.md",
    }
    facts = ROOT / "facts"
    for old, new in mapping.items():
        op = facts / old
        np = facts / new
        if op.is_file():
            text = op.read_text(encoding="utf-8")
            text = text.replace("# Facts — Operations", "# Facts — Shared")
            text = text.replace("# Rules — Operations", "# Rules — Shared")
            text = text.replace("(pre-seeded)", "(pre-seeded; Workflows: all)")
            # normalize entry headers to ###
            text = re.sub(r"^## (\d{4}-\d{2}-\d{2}:)", r"### \1", text, flags=re.M)
            np.write_text(text, encoding="utf-8", newline="\n")
            op.unlink()
            print(f"renamed {old} -> {new}")


def bulk_replace() -> None:
    exts = {".md", ".txt", ".py", ".json", ".yml", ".yaml", ".sh"}
    skip = {".git", "__pycache__", "visual-page"}
    reps = [
        ("facts/facts-operations.md", "facts/facts-shared.md"),
        ("facts/rules-operations.md", "facts/rules-shared.md"),
        ("facts-operations.md", "facts-shared.md"),
        ("rules-operations.md", "rules-shared.md"),
        ("workflowID-", "workflow-"),
        ("WorkflowID-", "Workflow-"),
        ("newID-workflow", "new-workflow"),
        ("folloWID-up", "follow-up"),
        ("inject-rules-on-action.sh", "inject_rules_on_action.py"),
        ("inject-journal-context.sh", "inject_journal_context.py"),
        ("merge-agent-notes.sh", "merge_agent_notes.py"),
        ("post-journal-update.sh", "journal_snapshot.py"),
        ("config:change", "write:doc"),  # only if leftover; careful - better skip
    ]
    # Do NOT blindly replace config:change with write:doc - remove mentions instead
    reps = [r for r in reps if r[0] != "config:change"]

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(p in skip for p in path.parts):
            continue
        if path.name.startswith("_repair"):
            continue
        if path.suffix.lower() not in exts and path.name not in {"CLAUDE.md", "MyRole.txt", "DESIGN.md"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        orig = text
        for a, b in reps:
            text = text.replace(a, b)
        # stop writing legacy pointer
        text = re.sub(
            r"(?m)^.*also write(?:s)? to `?\.claude/active-work-item\.txt`?.*\n?",
            "",
            text,
        )
        text = re.sub(
            r"(?m)^.*also `?\.claude/active-work-item\.txt`?.*\n?",
            "",
            text,
        )
        text = re.sub(
            r"(?m)^.*If work-item: also write to `\.claude/active-work-item\.txt`.*\n?",
            " - Do not write the legacy `.claude/active-work-item.txt` (read fallback only).\n",
            text,
        )
        text = text.replace(
            "Write `.claude/active-context.txt` as `work-item:<id>` and `.claude/active-work-item.txt`.",
            "Write `.claude/active-context.txt` as `work-item:<id>` only (do not write the legacy `.claude/active-work-item.txt`).",
        )
        text = text.replace(
            "Write `.claude/active-context.txt` as `<context_type>:<context_id>`. If work-item, also `.claude/active-work-item.txt`.",
            "Write `.claude/active-context.txt` as `<context_type>:<context_id>`. Do not write the legacy `.claude/active-work-item.txt`.",
        )
        text = text.replace(
            " - If work-item: also write to `.claude/active-work-item.txt` for backward compatibility",
            " - Do not write the legacy `.claude/active-work-item.txt` (read fallback only).",
        )
        # operations wording leftovers for this role
        text = text.replace("operations memory (`facts/facts-shared.md`", "shared memory (`facts/facts-shared.md`")
        text = text.replace("Equipment-rental operations memory", "Equipment-rental shared memory")
        text = text.replace("Expert Role operations memory", "Expert Role shared memory")
        text = text.replace("into Expert Role operations memory", "into Expert Role shared memory")
        text = text.replace("and operations memory under `facts/`", "and shared memory under `facts/`")
        if text != orig:
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"updated {path.relative_to(ROOT)}")


def fix_skill_context_blocks() -> None:
    skills = ROOT / ".claude" / "skills"
    patterns = [
        re.compile(
            r"(?ms)^\*\*Get Work Item context:\*\*\n(?:- .*\n)+",
        ),
        re.compile(
            r"(?ms)^### 0\. Work Item [Cc]ontext\n(?:.*?\n)+?(?=^### |^## |\Z)",
        ),
        re.compile(
            r"(?ms)^## Work Item [Cc]ontext\n(?:.*?\n)+?(?=^## |\Z)",
        ),
    ]
    for skill_md in skills.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        orig = text
        # Replace common old Work Item Context blocks
        text = re.sub(
            r"(?ms)^(?:###? )?(?:\*\*)?(?:0\.\s*)?Work Item [Cc]ontext(?:\*\*)?\n(?:[-*].*\n|Read .*\n|Journal:.*\n|Active .*\n|Artifacts:.*\n|STATUS.*\n|Flat journal:.*\n|Active note:.*\n|1\..*\n|2\..*\n|3\..*\n|4\..*\n)+",
            CONTEXT_BLOCK + "\n",
            text,
            count=1,
        )
        text = text.replace(
            "`work-items/<work-item-id>/journal/progress.md`",
            "`journals/work-items/<id>/progress.md`",
        )
        text = text.replace(
            "`work-items/<id>/journal/progress.md`",
            "`journals/work-items/<id>/progress.md`",
        )
        text = text.replace(
            "work-items/<work-item-id>/journal/progress.md",
            "journals/work-items/<id>/progress.md",
        )
        text = text.replace(
            "Read active Work Item ID from `.claude/active-work-item.txt`",
            "Read active Work Item ID from `.claude/active-context.txt` (`work-item:<id>`; legacy `.claude/active-work-item.txt` read-only fallback)",
        )
        if text != orig:
            skill_md.write_text(text, encoding="utf-8", newline="\n")
            print(f"skill context {skill_md.parent.name}")


def strip_escaped_md(path: Path) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    # Only outside fenced code: simple pass for known damage
    text2 = text.replace("\\#", "#").replace("\\*", "*").replace("\\[", "[").replace("\\]", "]")
    text2 = text2.replace("&#x20;", " ")
    # collapse triple+ blank lines to double
    text2 = re.sub(r"\n{3,}", "\n\n", text2)
    if text2 != text:
        path.write_text(text2, encoding="utf-8", newline="\n")
        print(f"unescaped {path.relative_to(ROOT)}")


def main() -> None:
    # Scripts from Cursor sibling
    copy_adapted("scripts/test_journal_hook.py")
    copy_adapted("scripts/test_rules_hook.py")
    copy_adapted("scripts/test_stop_hooks.py")
    copy_adapted("scripts/check_scaffold.py")
    copy_adapted("scripts/memory/build_trigger_index.py")
    copy_adapted(
        ".cursor/skills/memory-optimize/scripts/analyze-memory.py",
        ".claude/skills/memory-optimize/scripts/analyze-memory.py",
    )

    # agent-notes template
    notes = ROOT / "journals" / "work-items" / "_TEMPLATE" / "agent-notes"
    notes.mkdir(parents=True, exist_ok=True)
    src_readme = SRC / "journals" / "work-items" / "_TEMPLATE" / "agent-notes" / "README.md"
    if src_readme.is_file():
        (notes / "README.md").write_text(
            adapt_cursor(src_readme.read_text(encoding="utf-8")),
            encoding="utf-8",
            newline="\n",
        )
        print("agent-notes README")

    # D7 remove legacy journal pointer template
    legacy = ROOT / "work-items" / "_TEMPLATE" / "journal"
    if legacy.exists():
        shutil.rmtree(legacy)
        print("removed work-items/_TEMPLATE/journal")

    # STATUS template from sibling if better
    copy_adapted("work-items/_TEMPLATE/STATUS.md")

    # CONTEXT-SYSTEM
    copy_adapted(".cursor/CONTEXT-SYSTEM.md", ".claude/CONTEXT-SYSTEM.md")

    # HOW-MEMORY and MEMORY-INDEX from sibling then rename
    copy_adapted("facts/HOW-MEMORY-LOADING-WORKS.md")
    copy_adapted("facts/MEMORY-INDEX.md")

    rename_memory()
    bulk_replace()
    fix_skill_context_blocks()

    for rel in [
        "facts/MEMORY-INDEX.md",
        "facts/HOW-MEMORY-LOADING-WORKS.md",
        "work-items/_TEMPLATE/facts/facts.md",
        "work-items/_TEMPLATE/facts/rules.md",
    ]:
        strip_escaped_md(ROOT / rel)

    # Fix test scripts that still say cursor- in prefixes / .cursor after adapt should be .claude
    for rel in [
        "scripts/test_journal_hook.py",
        "scripts/test_rules_hook.py",
        "scripts/test_stop_hooks.py",
        "scripts/check_scaffold.py",
        "scripts/memory/build_trigger_index.py",
    ]:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        text = text.replace("cursor-journal-", "claude-journal-")
        text = text.replace("cursor-rules-", "claude-rules-")
        text = text.replace("cursor-stop-", "claude-stop-")
        text = text.replace("cursor journal hook", "claude journal hook")
        text = text.replace("cursor rules hook", "claude rules hook")
        text = text.replace("Cursor preToolUse", "Claude PreToolUse")
        text = text.replace("Cursor equipment-rental", "Claude equipment-rental")
        # check_scaffold should look at CLAUDE.md not AGENTS
        text = text.replace('"AGENTS.md"', '"CLAUDE.md"')
        text = text.replace("AGENTS.md", "CLAUDE.md")
        p.write_text(text, encoding="utf-8", newline="\n")

    # Ensure .gitattributes / gitignore
    (ROOT / ".gitattributes").write_text("* text=auto\n*.sh text eol=lf\n", encoding="utf-8", newline="\n")
    (ROOT / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8", newline="\n")

    # GitHub workflow optional
    yml_src = SRC / ".github" / "workflows" / "scaffold.yml"
    if yml_src.is_file():
        dst = ROOT / ".github" / "workflows" / "scaffold.yml"
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = adapt_cursor(yml_src.read_text(encoding="utf-8"))
        text = text.replace(".claude/hooks.json", ".claude/settings.json")
        dst.write_text(text, encoding="utf-8", newline="\n")
        print("scaffold.yml")

    print("DONE")


if __name__ == "__main__":
    main()
