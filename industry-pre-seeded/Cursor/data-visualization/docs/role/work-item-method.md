# Role work-item method — Data visualization from their files

This expert produces **descriptive charts, tables, and write-ups from files the operator drops**. It is not a data-science engagement, not analytics engineering, and not a software HLD/DD/implement pipeline.

Industry practice for chart work from supplied tables (exploratory analysis plus presentation charts) follows a question-first loop: name the question and audience, inspect the file, choose a form that matches the data shape, build an honest visual with labeled axes and source, then review and iterate. Sources informing this method: University of Toronto Map and Data Library visualization workflow; ONE Data visualisation design process; Datafield “from question to publish” chart workflow; standard EDA cycles (question → inspect → surprise → next check).

Starter notes in memory are **guesses until this shop teaches**. Their file wins over a typical note.

## Typical phases

| Phase | What happens | Typical artifacts (under `work-items/<id>/`) | Human gates |
| --- | --- | --- | --- |
| **1. Question** | Name the question, audience, measure, columns, date range, and filters. Refuse causal, forecast-as-product, scrape, BI-site, or invented-column asks. | Journal decisions; optional `in/` note of the question | Operator names the question and columns before a PNG is treated as done |
| **2. Intake** | Open or continue one Work Item. Place the named export in `in/`. Record source file name and version. | `in/<source>.csv` (or xlsx); source named in journal | Missing file, encoding, or sheet name → ask. Missing Python package → install ask, not a fake picture |
| **3. Profile** | Read dtypes, missingness, n, date range, and units. List parse failures. Do not impute. | `work/` summary or missing CSV | Header, date format, separator, timezone, or week-start guesses must be labeled and asked |
| **4. Prepare** | Filter, join, aggregate, or reshape **only** as they named. Write the table the chart will plot. | `work/*.csv` of plotted values | Dual axis, log scale, clip, derived column, impute, or invented join key → ask. Do not proceed on a missing named column |
| **5. Chart** | Choose the form that matches the question and data shape (bars, histogram, line, scatter, small multiples, missing/outlier lists). Colorblind-safe. Zero baseline for count/dollar bars. Units on axes. | `out/*.png` (or PDF); optional companion PNG | Truncating a count/dollar bar axis to lie is refused. PII identifiers stay off the picture |
| **6. Pack** | Write-up: question, source file, columns, filters, n, missing, and **what was not claimed**. | `out/*.md`; check logs in `evidence/` | Pack is not done until the write-up exists and named files pass their checks |
| **7. Review** | Operator reads the pack. Corrections become facts/rules via **remember**. Same question + new export uses refresh. | Dated PNG / comparison write-up on refresh | Operator acceptance (or documented exception). “Continue” is not approval of an open question |

## Chart-form map (question → registered workflow)

| Question shape | Registered workflow |
| --- | --- |
| What is in this file? counts, missing, min/max/mean | `describe-csv` (default) |
| How is a named numeric distributed? | `histogram-pack` |
| Compare a named measure across a named category | `group-compare-bars` |
| How did a named series move over dates they named? | `time-series-line` |
| Do two named numerics associate in this file? | `scatter-and-corr` |
| Same chart, once per value of a named facet | `small-multiples` |
| Where is missing, and which points sit outside their fence? | `missing-and-outliers` |
| Same question, new export, same columns | `refresh-from-new-export` |

If none of these match, **workflow-selector** offers only the registry. Do not invent an unregistered process. A folder of PNG/CSV/markdown files is the “dashboard”; a hosted BI product is out of scope.

## How a Work Item runs here

1. **workflow-selector** (if no workflow) → one folder `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, then this Work Item’s facts/rules.
3. Walk the selected `.cursor/workflows/<id>.md` map: read the tool doc, write the produced file, run the check from the Work Item folder, **journal-keeper**.
4. One ready step per **continue**, unless they asked for the whole named job.
5. **operator-qa** when a column meaning, filter, gate, or shop procedure is missing. Do not invent how this shop works.
6. Done = map checks pass (or documented exceptions), named charts and work CSVs exist, write-up states question / source / columns / filters / not-claimed.

Canonical expert skills for this loop: `continue`, `workflow-selector`, `journal-keeper`, `operator-qa`, `remember`, `integrate-docs`, `promote-facts-rules`, `switch-context`. Role *how* lives in the workflow files and `docs/tools/`, not in a parallel process-skill layer.
