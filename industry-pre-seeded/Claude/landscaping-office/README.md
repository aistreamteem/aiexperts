# Landscaping / lawn-care office Expert

Office Expert for a US lawn-care or landscape-maintenance shop: crews, routes, job tickets, seasonal calendars, estimates from the shop’s price file, material lists, and weather postpones as **their** call.

- **Role:** `MyRole.txt`
- **How work runs:** `docs/role/work-item-method.md`
- **Agent instructions:** `CLAUDE.md`
- **Memory:** `facts/facts-shared.md`, `facts/rules-shared.md`
- **Workflows:** `.claude/workflows/` (see `workflow-registry.json`)
- **Tools:** `docs/tools/`
- **Jobs:** `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`
- **Journals:** `journals/expert/` and `journals/work-items/<id>/` (active id in `.claude/active-context.txt`)
- **Hooks:** `.claude/settings.json` runs `py -3` PreToolUse / Stop hooks under `.claude/hooks/`

This Expert does **not** apply chemicals as a license, diagnose trees, stamp irrigation or drainage engineering, pay crews, invent wages or dump fees, or store gate codes.

## Quick start

1. Open this folder in Claude Code.
2. Say **continue** (or name a crew day / ticket / week). If `MyRole.txt` is pending, **define-role** runs first.
3. Drop source sheets/PDFs into `work-items/<id>/in/`. **continue** walks one ready workflow step and updates the journal.
4. Shop facts/rules live under `facts/` (shared memory). Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`.
5. Finished packs land in that Work Item’s `out/` with sources, artifacts, and checks noted in the journal / STATUS.

Starter notes are typical practice until this shop teaches otherwise.
