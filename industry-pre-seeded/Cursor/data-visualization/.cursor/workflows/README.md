# Role workflows

Named chart packs for **Data visualization from their files**. Each file is a self-contained job: when to use it, how to run it, initial phase `question`, and a YAML work map that **continue** walks (one ready step, or the whole named job if they asked).

Jobs are listed in `workflow-registry.json`. Default: `describe-csv`. Method: `docs/role/work-item-method.md`.

## Available jobs

1. **Describe CSV** (`describe-csv`) — Load the named CSV and write a numeric summary plus a write-up.
2. **Group Compare Bars** (`group-compare-bars`) — Group a named measure by a named category; aggregated CSV, PNG bars, write-up.
3. **Histogram Pack** (`histogram-pack`) — Histogram a named numeric column; values CSV, PNG, write-up.
4. **Missing and Outliers** (`missing-and-outliers`) — Missing-count CSV and outlier list for named columns.
5. **Refresh from New Export** (`refresh-from-new-export`) — Reload a new CSV with the same columns; dated PNG and comparison write-up.
6. **Scatter and Correlation** (`scatter-and-corr`) — Scatter two named numeric columns; points, descriptive correlation, PNG, write-up.
7. **Small Multiples** (`small-multiples`) — Repeat the same chart for each value of a named facet column.
8. **Time Series Line** (`time-series-line`) — Date column, range, and grain they named; series CSV and PNG line.

## How to run

1. Match a named job (or **workflow-selector** if none is set).
2. Open or continue `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`.
3. Walk the instruction file: read the tool doc, produce the artifact, run the check from the Work Item folder, **journal-keeper**.
4. One ready step per **continue**, or the whole named job if they asked.

Data moves only as named files (`needs` / `produces`). Do not skip a step with a chat summary.

## Adding a job

1. Create `.cursor/workflows/<id>.md` with When to use, How to run, Initial phase `question`, and a YAML work map.
2. Add a registry entry in `workflow-registry.json` (key = filename stem).
3. Point `MyRole.txt`, `AGENTS.md`, and `docs/role/work-item-method.md` at the new file.

Do not put live maps under `docs/workflows/`. That folder only points here.
