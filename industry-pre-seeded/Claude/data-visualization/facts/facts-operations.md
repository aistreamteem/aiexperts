# Facts — Operations (pre-seeded)


---

## 2026-11-08: Aggregation they asked for
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/aggregation.md
**Status:** active

**Starter / guess until they teach.**

Aggregation is a sum, count, mean, median, min, or max they named, over a group they named, for a measure they named. Typical US SMB asks are sales by week, tickets by tech, or units by SKU. The Expert may run Python here, import pandas, and call groupby with the agg they asked for, then write the result to a work CSV that the chart reads. Do not switch mean and sum to make a story. Do not average percents across groups unless they said that is the measure — percent of what stays explicit. Do not add a weighted mean unless a weight column exists and they named it. Count of rows is not count of unique customers unless they named the unique key. Missing groups that have no rows stay absent unless they asked to show zeros from a list they provided. Aggregation is descriptive. It is not a forecast and not a causal model. The write-up names the function, the group columns, and the source file. Starter until they teach how *this* shop rolls days into weeks and which total they trust.

---

## 2026-11-08: Annotations from a file they stored
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/annotations-from-file.md
**Status:** active

**Starter / guess until they teach.**

An annotation is a date or category mark that comes from a file they stored: a holiday list, a store-open date, a note column. Typical US SMB owners remember “that was the flood week” but the role only plots it when the date is in a file. The Expert may run Python, merge the annotation file on the key they named, and call annotate or axvline, then save the PNG. Do not invent an event. Do not scrape a holiday API. Do not write a witty callout that claims a cause. If the annotation file is missing, the chart stays unannotated and the write-up says so. PII does not appear in callouts. Text stays short so it does not cover the series. A work CSV can list which annotation dates fell inside the plotted range. This is still a descriptive chart, not a news product. Starter until they teach where *this* shop keeps event dates.

---

## 2026-11-08: Axis truncation that lies
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/axis-truncation.md
**Status:** active

**Starter / guess until they teach.**

Truncating a y-axis on a bar or area of counts or dollars so the axis does not start at zero can make a small change look huge. Typical US SMB slideware does this to “show impact.” This role does not truncate a count or dollar bar axis to lie. If they ask to zoom a line chart of a large level, say that the axis does not start at zero and give an untruncated companion or the min/max in the caption. Do not use a broken axis as a trick. Dual axis is a different caution. Clipping outliers is a different ask and still needs the list. Matplotlib will happily start at 90 percent of max if you set ylim — do not. Done is a PNG whose scale a skeptical owner can trust. Starter until they teach when *this* shop accepts a zoomed line versus a zero-baseline bar.

---

## 2026-11-08: Bar chart for named groups
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/bar-chart.md
**Status:** active

**Starter / guess until they teach.**

A bar chart compares a measure they named across a category they named. Typical US SMB bars are sales by location, counts by status, or hours by crew. The Expert may run Python here, import pandas then matplotlib or seaborn, compute the aggregation they asked for, and call barplot or bar, then save out/*.png. Sort order is an ask: by the measure, by their list, or alphabetical — do not silently sort to dramatize a winner. Zero baseline is the default for counts and dollars unless they asked otherwise and the write-up says why. Color is colorblind-safe by default. Do not invent a category. Do not turn a bar chart into an A/B winner stamp. Error bars from a sample they did not define are not added. A table of the plotted values is written to work/ so the picture can be checked. If a package is missing, ask; do not fake bars. The write-up names the question, file, columns, and what was not claimed. Starter until they teach *this* shop’s compare order.

---

## 2026-11-08: Baseline they named
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/baseline-they-named.md
**Status:** active

**Starter / guess until they teach.**

A baseline is a comparison they named: last week in the file, a target column they store, a staffed-hour denominator, or a prior export they dropped. Typical US SMB “baseline” talk is a remembered good week. The Expert plots the baseline only from a column or a second file they named. Do not invent a target. Do not scrape an industry benchmark. Do not draw a goal line from a speech. If they have a target sheet, merge on the key they name and show actual versus target as description, not as a performance verdict you own. A baseline change (new store, new filter) is called out in the write-up. Write both series to work/. Charts label which line is baseline. A missing baseline file is an ask, not a remembered good week you type in. Starter until they teach what *this* shop treats as the comparison.

---

## 2026-11-08: Box or violin for a named numeric by group
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/box-or-violin.md
**Status:** active

**Starter / guess until they teach.**

A box or violin plot shows spread of a numeric column they named, often split by a group they named. Typical US SMB asks are ticket dollars by location or duration by job type. The Expert may run Python in this workspace, import seaborn, and call boxplot or violinplot, then save out/*.png. Say what the box edges mean in ordinary English (quartiles as computed) and say the n per group. Do not treat a longer whisker as a quality failure. Do not hide outliers if they asked to see them as a list. Violin density is sensitive to small n; prefer a box or a strip when groups are tiny and say so. Do not invent a group. Units stay on the axis. This is descriptive. It is not a test verdict and not a hiring decision. Write a summary CSV of count, median, and quartiles per group when they want the numbers. If seaborn is missing, ask and install; do not draw a fake box. Starter until they teach whether *this* shop reads medians or means.

---

## 2026-11-08: Caption says what was not claimed
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/caption-what-not-claimed.md
**Status:** active

**Starter / guess until they teach.**

The write-up and, when they want it on the picture, a caption state what was not claimed: no cause, no forecast, no A/B winner, no policy from a p-value. Typical US SMB slides let the title do the arguing. The Expert writes a short not-claimed list next to the question, the source file, the columns, and the filters. Do not bury the caveat in a footnote no one opens. Do not use a caption to sneak a causal verb. If they asked for a correlation, the caption says association in this file only. If a dual axis or a zoomed line was used, the caption says that too. Small n and missing counts belong here. This is how the role stays a chart-from-their-files Expert and not a data-science stamp. Done is out/*.md that a skeptical owner can read without the PNG. Starter until they teach how *this* shop wants the weekly caveat worded.

---

## 2026-11-08: Chart file formats
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/chart-file-formats.md
**Status:** active

**Starter / guess until they teach.**

Chart deliverables on this role are files: PNG for slides and chat, PDF for print, SVG if they asked and the library can write it. Typical US SMB owners want a PNG they can paste. The Expert calls savefig or FacetGrid.savefig to a path under out/ with a name that includes the question slug and a date if this is a refresh. Do not deliver only a GUI window. Do not screenshot a notebook and call it the chart file if they asked for a named PNG. DPI is an ask; a readable default is fine and should be written if they care about print. PDF pages that hide a second series are not a trick you use. Keep the work CSV of plotted values next to the picture. If matplotlib is missing, ask and install; do not drop a blank PNG. This is not a hosted dashboard. Starter until they teach which format *this* shop pastes into the weekly note.

---

## 2026-11-08: Clipping the view only if they ask
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/clipping-ask.md
**Status:** active

**Starter / guess until they teach.**

Clipping is a y-limit or x-limit that hides values outside a window they named. Typical US SMB owners want to “zoom” a busy week. The Expert clips only when they asked, and still provides an unclipped file or a note that points were cut. Do not clip to manufacture a steep slope. Do not clip outliers without also writing the outlier list. Axis truncation that starts above zero for a count or dollar bar is a separate lie-risk; see that fact. Matplotlib set_ylim is fine when requested. The caption says the window. Filtered rows (a date range) are not the same as clipping an axis on rows that remain — say which. If they want both zoom and context, two PNGs. A clip is not a filter of rows and is not a reason to drop the outlier list. Starter until they teach when *this* shop wants a zoomed inset versus the full range.

---

## 2026-11-08: Cohort only if they define it
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/cohort-if-they-define.md
**Status:** active

**Starter / guess until they teach.**

A cohort is a set of rows that share a start they defined: first-purchase month, hire week, or install date — from columns in their file. Typical US SMB “cohort” talk is informal. The Expert builds a cohort table only when they named the start column and the measure, then plots a table or small multiples they asked for. Do not invent a first-touch from a scrape. Do not treat retention as a productized SaaS metric with borrowed formulas. If the start date is missing, ask. Survival-looking charts are still descriptive counts from their file, not a clinical or credit model. PII stay off the chart; cohort labels are dates or their codes. Write the cohort counts to work/. This is not a CRM journey product and not a causal lift study. If they did not define a cohort, refuse that frame and offer a filter they can name instead. Starter until they teach how *this* shop dates a start.

---

## 2026-11-08: Color and colorblind defaults
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/color-and-colorblind.md
**Status:** active

**Starter / guess until they teach.**

Color on this role is for categories they named or for a numeric scale they named, not for decoration that invents urgency. Typical US SMB slides use red-green that many people cannot separate. The Expert defaults to a colorblind-safe palette from seaborn or a matplotlib colormap they keep, and says so in the write-up if they asked. Do not use red to mean “bad” unless their file has a status called bad and they asked for that code color. Do not encode a third measure only in color if a label or a second panel would be clearer. Print and PDF still need contrast. Category colors stay stable across refresh files so week two is not a new rainbow. PII is not color-coded as a personal flag. If seaborn is missing, matplotlib tab10 or a documented colorblind map is fine; ask to install rather than invent a custom brand kit. This is not a marketing website. Starter until they teach *this* shop’s brand colors — and still keep the colorblind default unless they override in words.

---

## 2026-11-08: Column types as stored
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/column-types.md
**Status:** active

**Starter / guess until they teach.**

Column type is what the file actually holds after a read, not what a slide title hopes it is. Typical US SMB exports mix numbers stored as text, dates as serials, and currency with dollar signs. The Expert may run Python in this workspace, import pandas, and use dtypes, to_numeric with errors shown, or to_datetime on the columns they named. Write a short type table to a work CSV so the write-up can say which fields were numeric, text, or datetime after the read. Do not silently coerce a text ID into a float and drop leading zeros. Do not invent a type that was not supported by the cells. Percent columns that are already 0–1 or already 0–100 stay labeled as they came; ask if the file does not say. Boolean flags they typed as Y/N stay as their codes unless they asked for a mapped column and named the map. Type cleanup is for the chart they asked for, not a warehouse project. Missing parse failures stay listed. Starter until they teach how *this* shop types money, dates, and IDs.

---

## 2026-11-08: Correlation is not cause
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/correlation-not-cause.md
**Status:** active

**Starter / guess until they teach.**

Correlation is a descriptive number about two numeric columns they named in this file, for the rows after their filters. Typical US SMB owners see two lines move and want a why. The Expert may compute Pearson or Spearman with pandas, numpy, or scipy.stats if they asked, show a scatter, and write that the number is not a cause, not a lever, and not a reason to spend money. Do not invent a mechanism. Do not stamp an A/B winner. Outliers they listed can move the number; point at the outlier list. Small n is said. A fit line, if they asked, is a description of these points. Confounders are not “controlled” unless they named a method and the columns exist — and still you do not write a causal claim. Done is a PNG, a number in the write-up, and the caption of what was not claimed. Starter until they teach how *this* shop wants association wording.

---

## 2026-11-08: Count versus rate
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/count-vs-rate.md
**Status:** active

**Starter / guess until they teach.**

A count is how many rows or units. A rate is a count divided by a denominator they named (visits, hours, days open, customers in the file). Typical US SMB charts mix “ten more tickets” with “a higher rate” and then argue. The Expert plots what they asked for and labels it as count or rate in the title and axis. Do not invent a denominator. Do not divide by a population you do not have in the file. Do not treat a count chart as a rate in the write-up. If they asked for both, two panels or two files are clearer than a dual axis unless they asked for dual and accepted the caution. Small denominators make rates jump; say the n. A rate is still descriptive. It is not a quality verdict and not a causal claim. pandas can compute the ratio only from columns they named. Done is a work CSV with the count, the denominator, and the rate, plus a PNG that does not hide the n. Starter until they teach which denominator *this* shop uses.

---

## 2026-11-08: Dashboard means a folder of files
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/dashboard-as-folder-not-product.md
**Status:** active

**Starter / guess until they teach.**

A “dashboard” on this role is a folder of named PNG, PDF, and CSV files plus a write-up, not a hosted BI site, not a live CRM tile, and not an email campaign product. Typical US SMB owners say dashboard when they want last week’s pictures in one place. The Expert writes those files under out/ and work/ and lists them in markdown. Do not stand up Tableau, Power BI, Looker, or a marketing site as this product. Do not keep a live query against a passworded warehouse. Refresh is a new export they drop, then a new dated PNG. Small multiples can live in one PNG. The folder is done when the question, source file, and what-was-not-claimed are readable. No email blast of the folder as a marketing product. Starter until they teach how *this* shop wants the weekly folder named.

---

## 2026-11-08: Date parse from their column
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/date-parse.md
**Status:** active

**Starter / guess until they teach.**

Dates come from the column they named. Typical US SMB exports use m/d/y text, ISO strings, or Excel serials. The Expert may run Python here, import pandas, and call to_datetime on that column, with the format they named if the file is ambiguous. Write a work CSV that keeps the parsed date and the original text when a parse fails, and list failure counts in the write-up. Do not invent a timezone. If the file has no zone and they care about close-of-day versus UTC, ask. Fiscal calendars and week-start rules are theirs; do not assume a calendar year or a Monday week unless they said so. Do not fill a missing date from a neighboring row. A date filter they named (from, to) is applied after a successful parse and is written in the caption. Daylight-saving oddities are questions, not silent fixes. This is not a live clock scrape. If pandas is missing, ask; do not type dates by hand into a fake chart. Starter until they teach how *this* shop dates tickets, invoices, and shifts.

---

## 2026-11-08: Descriptive stats table
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/descriptive-stats.md
**Status:** active

**Starter / guess until they teach.**

Descriptive stats are count, missing count, min, max, and mean or median for numeric columns they named, plus distinct count for text if they asked. Typical US SMB packs start here before anyone draws a picture. The Expert may run Python, import pandas, and call describe or a small custom table, then write work/*.csv and a write-up. Do not treat the mean as the typical row when the median is what they read. Do not hide min and max. Do not drop missing before describe unless they asked, and then say how many dropped. Text IDs are not averaged. Dates get min and max as a range, not a mean of serials unless they asked. This table is not a scientific paper and not a policy. Units stay next to column names. If they asked for a subset, filter first and say so. Starter until they teach which columns *this* shop always summarizes.

---

## 2026-11-08: Dual axis only if they ask
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/dual-axis-caution.md
**Status:** active

**Starter / guess until they teach.**

A dual-axis chart puts two measures with different scales on one picture. Typical US SMB asks overlay dollars and ticket count, or temperature and units. Dual axes make a false match look like a lockstep story. This role uses a dual axis only when they asked, and the write-up says both scales and that the overlay is not a causal proof. Prefer two panels with a shared x when they will accept it. Do not rescale an axis so two lines hug. Do not invent a second measure. Matplotlib twinx is available if they insist; seaborn is not a reason to skip the caution. Units must appear on both axes. A correlation number, if shown, stays descriptive. If they did not ask for dual axis, use two files or small multiples. Done is a PNG that a skeptical owner can still read, plus a work CSV of both series. Starter until they teach whether *this* shop accepts two panels instead.

---

## 2026-11-08: File encodings and separators
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/encodings.md
**Status:** active

**Starter / guess until they teach.**

Encoding and delimiter are how their file is stored on disk, not a guess from another shop. Typical US SMB Windows exports arrive as CSV with commas, sometimes semicolons, sometimes tab, and sometimes a header in Latin-1 or Windows-1252 that breaks a naive UTF-8 read. The Expert may run Python in this workspace, import pandas, and call read_csv with the encoding and separator they named — or try the obvious ones and report which one read without mojibake, without inventing columns. Write the chosen encoding in the write-up. Do not scrape a new file from the web to replace a broken export. Do not store passwords to a portal to re-export. If the file is actually an Excel workbook, say so and use read_excel. Quoted fields and embedded commas stay as pandas parsed them. A wrong encoding that splits one name column into two is a read error, not a new attribute you keep. Done is a readable work CSV plus a note of encoding and separator. Starter until they teach how *this* shop exports from the register or the accounting system.

---

## 2026-11-08: Export the CSV of what was plotted
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/export-csv-of-plotted.md
**Status:** active

**Starter / guess until they teach.**

Every chart pack includes a CSV of the values that actually went to the picture: the aggregated x, y, group, and n. Typical US SMB arguments are “the chart is wrong” with no table. The Expert writes work/*.csv via pandas to_csv after the groupby and before or after savefig. Column names stay readable. Filters and the source file name belong in the write-up and may be extra columns if they asked. Do not export extra PII that was not plotted. Do not export a different aggregation than the PNG. The check for many workflows is that this CSV exists and has the expected columns. Refresh writes a new dated CSV or a clear name so last week is not overwritten unless they said replace. Starter until they teach where *this* shop files the numbers behind the picture and whether last week’s CSV is kept.

---

## 2026-11-08: Filters they named
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/filters-they-named.md
**Status:** active

**Starter / guess until they teach.**

Filters are the rows they asked to keep: a date range, a location, a product line, a status code. Typical US SMB owners say “last quarter, store 3, finished jobs only.” The Expert applies only those filters, using pandas boolean masks or query on columns that exist, and writes the filtered row count next to the unfiltered count in the write-up. Do not add a quiet extra filter to remove “ugly” points. Do not exclude outliers unless they said to. Do not change the date range to make a trend look nicer. If a filter column is missing, ask; do not invent it. Keep the filter text in the chart title or caption so a later export can be compared honestly. A filter is not a causal claim that the excluded rows do not matter. Refresh jobs reuse the same named filters on the new file. Done is a work CSV of the filtered rows when they asked for one, plus a PNG that matches that subset. Starter until they teach *this* shop’s usual slices.

---

## 2026-11-08: Forecast is not a product on this role
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/forecast-refuse-as-product.md
**Status:** active

**Starter / guess until they teach.**

A forecast as a product — next month’s sales, a predicted winner, a fitted future line presented as a plan — is out of scope. Typical US SMB owners ask for a projection after a good week. The Expert may plot history they have, including a rolling mean they asked for, and must not extend a line past the last date as if the future were in the file. Do not ship a statsmodels forecast as a decision pack. Do not scrape a macro series to “complete” a model. If they insist on a what-if arithmetic they typed (last week times a factor they named), label it as their arithmetic, not a forecast product, and still do not stamp it as likely. This is not a data-scientist engagement. The write-up says the future was not claimed. Starter until they teach that *this* shop wants history pictures, not a prediction role.

---

## 2026-11-08: Funnel only if they define the steps
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/funnel-if-they-define.md
**Status:** active

**Starter / guess until they teach.**

A funnel is a sequence of steps they defined, with counts from their file at each step. Typical US SMB “funnels” are estimate-to-job or lead-to-booked using status columns they already have. The Expert counts rows at each named step, in the order they named, and plots bars or a simple step chart. Do not invent a step. Do not scrape a website funnel. Do not call a step drop a conversion-rate winner or a marketing verdict. People can skip steps; say if the file allows skip or backtrack. Percents need a named base (of first step, of prior step). This is not a CRM or email product. Write the step counts to a work CSV. Small n at the bottom is said. If they have no step column, ask rather than infer from timestamps you reinterpret. Starter until they teach *this* shop’s status order.

---

## 2026-11-08: Heatmap caution
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/heatmap-caution.md
**Status:** active

**Starter / guess until they teach.**

A heatmap colors a matrix of values they named, often a pivot of two categories. Typical US SMB uses are hour-by-weekday ticket counts or SKU-by-store units. The Expert may run Python here, import seaborn, and call heatmap on a pivot they asked for, then save a PNG. Color scale is an ask: sequential for counts, and a diverging scale only if they named a meaningful midpoint (for example zero change they defined). Do not treat a hot cell as a causal hotspot or a staffing verdict. Missing cells in the pivot stay visible, not silently zero, unless they said zeros. Small n in a cell should be readable, perhaps as text on the cell if they asked. Colorblind-safe colormaps are the default. PII must not be a row or column label. A heatmap is not a correlation-as-cause stamp even if the matrix is a correlation matrix they requested as description. Write the pivot CSV to work/. If seaborn is missing, ask; do not paste a colored table as a fake heatmap file. Starter until they teach when *this* shop wants a matrix versus bars.

---

## 2026-11-08: Histogram of a named numeric column
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/histogram.md
**Status:** active

**Starter / guess until they teach.**

A histogram shows how a numeric column they named is spread across bins. Typical US SMB asks are ticket dollars, wait minutes, or order quantities. The Expert may run Python in this workspace, import matplotlib or seaborn, and call histplot or hist on that column after the filters they named, then save a PNG or PDF under out/. Bin count or bin width is an ask; if they did not name it, pick a simple default and say so in the write-up — do not hunt bins until the shape matches a story. Do not drop outliers unless they asked. Do not treat a bump as a causal segment. Small n belongs on the caption. Units go on the x-axis. A density y-axis is only if they asked; count of rows is the usual SMB read. Write a work CSV of bin edges and counts if they want the table behind the picture. If matplotlib or seaborn is missing, ask and install; do not paste a fake picture. This is not a forecasting product. Starter until they teach how *this* shop bins money and time.

---

## 2026-11-08: How this role files work items
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/how-we-file.md
**Status:** active

**Starter / guess until they teach.**

Day-to-day work does **not** go in one shared pile. Each **work item** (one chart pack: question + source file) gets its own folder under `work-items/<id>/` so Tuesday does not overwrite Monday, and one pack does not mix with the next. Journals for that pack live under `journals/work-items/<id>/`.

Typical name for *this* role (until they teach a different pattern):

- **What one folder is:** question + source file date
- **How to name it:** a dated slug under `work-items/` (for example sales-by-week) or a `WID-` id
- **Pattern:** `work-items/YYYY-MM-DD-question-short/`

Inside every Work Item folder:

- `in/` — files they dropped for *this* pack only
- `work/` — scratch and plotted-value CSVs while this pack is in progress
- `out/` — the finished charts and write-up for *this* pack
- `evidence/` — check logs for this pack only

Charts and the CSV they plotted live together. A refresh of the same question gets a new dated folder or a dated file inside if they said to replace.

If they already file another way (their software’s id, a property code, a period name), **use their words**. Ask before starting if it is unclear which pack this is. Never dump new files into yesterday’s folder. Never put two questions, two source dates, or two periods in the same Work Item folder unless they asked for a combined pack and named it that way.


---

## 2026-11-08: Joins only on keys they name
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/joins-from-their-keys.md
**Status:** active

**Starter / guess until they teach.**

A join combines two files they dropped using key columns they named. Typical US SMB packs are a sales export plus a store list, or tickets plus a staff roster, with messy name keys. The Expert may run Python here, import pandas, and call merge on those keys, then write the joined work CSV and a short count of matched versus unmatched rows. Do not invent a key. Do not fuzzy-match names into a new ID unless they asked and named the rule. Unmatched rows stay visible; do not drop them to make a total look clean. If the same key appears twice on one side, say so — a silent many-to-many explode is a mistake. Column names that collide get suffixes, not silent overwrites. This is not a warehouse model and not a CRM link. You do not scrape a third file to complete the join. The write-up names both source files, the keys, and the join type they asked for (left, inner, or as they said). Starter until they teach how *this* shop keys customers, SKUs, and locations.

---

## 2026-11-08: KPI they named
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/kpi-they-named.md
**Status:** active

**Starter / guess until they teach.**

A KPI on this role is a measure they named in words and mapped to columns in their file. Typical US SMB owners say “utilization” or “close rate” with different math. The Expert writes the formula as they stated it, computes it with pandas from those columns, and puts the number on a table or a simple chart. Do not pick a KPI from a consulting list. Do not change the formula to match a benchmark you remember. If they cannot name the columns, ask. A KPI is not a causal score and not a traffic-light policy unless they already store those thresholds in a file. Sample versus the whole file stays said. Write the inputs and the result to a work CSV so they can check the arithmetic. This is not a BI KPI product with drill-through. Refresh uses the same named formula on the new export. Starter until they teach the exact KPI *this* shop wants on the weekly pack.

---

## 2026-11-08: Legend for named series
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/legend.md
**Status:** active

**Starter / guess until they teach.**

A legend names the series they asked to plot, using the labels they use in the shop. Typical US SMB files have codes (A, B, loc_1) that need their label file if they have one — otherwise use the code and ask. The Expert places a legend that does not cover the data, or puts the legend below the plot, then saves the PNG. Do not invent a series. Do not hide a series in an unreadably small legend. Color and line style stay consistent with the colorblind default. If there is only one series, a legend may be omitted when the title already names it; say that choice. Small multiples may share one legend. A legend is not a causal footnote. Write the series list into the write-up so a color print still has words. If matplotlib is missing, ask; do not deliver a chart with an unreadable key. Starter until they teach *this* shop’s series names.

---

## 2026-11-08: Line chart for a named series
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/line-chart.md
**Status:** active

**Starter / guess until they teach.**

A line chart connects a measure they named along an order they named, usually a parsed date. Typical US SMB lines are daily sales, weekly tickets, or monthly units. The Expert may run Python in this workspace, import pandas and matplotlib, sort by the date column, and call plot, then save a PNG. Gaps stay gaps unless they asked to connect across missing days and said so. Do not smooth a line into a story. A rolling mean is a separate series they requested, not a replacement for the raw line unless they said replace. Do not extend the line past the last date in the file as a forecast. Dual axis with a second measure is an ask with caution. Annotations come from a file they stored, not from your guess about a holiday. Units and the source file name belong on the chart. If matplotlib is missing, ask and install. Done is out/*.png plus a work CSV of the plotted x and y. Starter until they teach how *this* shop spaces days and weeks.

---

## 2026-11-08: Log scale only if they ask
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/log-scale-ask.md
**Status:** active

**Starter / guess until they teach.**

A log axis changes how gaps look. Typical US SMB size mixes (tiny SKUs next to one huge account) tempt a log scale. The Expert uses log only when they asked, labels the axis as log, and keeps a linear version if they want both files. Do not apply log to hide a spike you do not want discussed. Zero and negative values cannot sit on a log axis; say so and do not silently drop them to force the scale. Units still appear. This is not a model. Matplotlib set_yscale log is the usual call. The write-up says who asked for log and why in their words. If they did not ask, stay linear. Done is a PNG that cannot be mistaken for a linear dollar axis. Starter until they teach whether *this* shop accepts log for size mixes.

---

## 2026-11-08: Map only if they have geo fields
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/map-only-if-geo.md
**Status:** active

**Starter / guess until they teach.**

A map is in scope only when their file has geo fields they named (lat/lon, a zip they want as a labeled table, or a region code) and they asked for a picture. Typical US SMB “maps” are a zip column with no shapes. The Expert does not scrape a live geocoder or a tile API as this product. If they stored a simple region list, a bar or a table may be the honest chart. If they have coordinates and a mapping library is installed, a static PNG may be written to out/; if the library is missing, ask — do not fake a map screenshot. PII street addresses do not become point labels. Counts by zip are a bar or heatmap-of-table, not a claim about neighborhoods. This is not a GIS engagement. Starter until they teach what geo *this* shop actually stores.

---

## 2026-11-08: Matplotlib defaults are a starting point
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/matplotlib-defaults.md
**Status:** active

**Starter / guess until they teach.**

Matplotlib defaults (font size, grid, color cycle) are a starting point, not a house style you invent as a brand system. Typical US SMB charts need larger tick labels and a tight layout so titles do not clip. The Expert may run Python, import matplotlib.pyplot, set a readable figsize, call tight_layout or constrained_layout, and savefig to out/. Do not spend the pack on ornament. Do not hide the default grid if they want to read values. If matplotlib is missing, ask and install; do not deliver a fake PNG. Style sheets they stored may be used; do not download a random style pack from the web as a scrape. Pin the matplotlib version only if their requirements file says so. Done is a readable file, not a default window that vanished. Starter until they teach *this* shop’s size and font needs.

---

## 2026-11-08: Missing cells stay visible
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/missing-data.md
**Status:** active

**Starter / guess until they teach.**

Missing data is a blank, NA, or unreadable cell in their file, not a zero you typed to finish a chart. Typical US SMB sheets have empty months, skipped SKUs, and rows people never filled. The Expert may run Python here, import pandas, and call isna, sum, and a missing-count table written to work as a CSV. The write-up names the file, the columns, and how many rows were blank in each field they asked about. Do not impute a mean, a last value, or a seasonal fill unless they said exactly how. Do not drop rows silently to make a line look continuous. If they asked to drop incomplete rows, say how many dropped and keep the filter in the write-up. A hole in a time series is a hole; annotate from a note they stored if they have one. Missing is not a causal story about why the cell is empty. Charts must not pretend the series was complete. If they want zeros for truly zero sales, they say so in words. Starter until they teach how *this* shop treats blanks versus true zeros.

---

## 2026-11-08: Multiple files they dropped
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/multiple-files.md
**Status:** active

**Starter / guess until they teach.**

Multiple files are separate exports they dropped, often one per month or per system. Typical US SMB folders have overlapping dates and slightly different headers. The Expert may run Python, import pandas, and concat files only when they asked and columns match or they named a column map. Write a source-file column from the file name so rows stay traceable. Do not silently union mismatched schemas. Do not treat two files as YoY growth if stores or filters differ — compare file names and overlapping columns honestly. Joins are a different step with keys they name. Do not scrape a third file to fill gaps. A pack can be one chart per file plus a comparison write-up. Done includes a work CSV that still has the source file name. Do not invent a master key across systems. Starter until they teach how *this* shop splits exports.

---

## 2026-11-08: NumPy for array math they asked for
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/numpy-arrays.md
**Status:** active

**Starter / guess until they teach.**

NumPy, when installed, is for array math they asked for: percentiles, a numeric mask, or a simple vector difference between two aligned series. Typical US SMB work still starts in pandas; numpy sits underneath or is used for a fence they named. The Expert may import numpy and write results back into a DataFrame and a work CSV. Do not invent a matrix factorization as a product. Do not treat a percentile as a policy threshold unless they already store that rule. NaN handling must match the missing-data rule — do not nan_to_num a hole into zero unless they said so. If numpy is missing, ask; do not fake an array result. Charts still go through matplotlib savefig. This is not a machine-learning role and not a custom array library. Starter until they teach which numeric extras *this* shop wants on the weekly pack.

---

## 2026-11-08: Outliers as a listed file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/outliers-as-list.md
**Status:** active

**Starter / guess until they teach.**

An outlier on this role is a row that looks extreme next to the rest of the file, listed so they can read it, not a point you delete to beautify a chart. Typical US SMB sales and count files have a huge return day, a typed extra zero, or a one-time event they already know. The Expert may run Python in this workspace, import pandas and numpy, and flag rows using a rule they named (for example a threshold they typed) or a simple descriptive fence such as a multiple of the interquartile range they asked to see. Write those rows to a work CSV with the original columns plus a note of the rule. Do not drop the rows from the main chart unless they asked. Do not call a point an error without their file saying so. Do not treat a fence as a scientific finding or a policy. Small n makes fences noisy; say the row count. The list is for their review. They decide whether a point stays, is a typo they will fix, or is a real spike they want labeled. Starter until they teach how *this* shop reviews extremes.

---

## 2026-11-08: pandas groupby for the table behind the chart
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/pandas-groupby.md
**Status:** active

**Starter / guess until they teach.**

pandas groupby is how this role turns a tidy work table into the numbers a bar, line, or facet will plot. Typical US SMB asks are sum of amount by day and location. The Expert may run Python, import pandas, and call groupby or pivot_table with the columns and functions they named, then to_csv under work/. Do not aggregate a column they did not name. Do not switch sum and mean. Do not drop NA groups silently unless they asked. observed=True versus unused categories is an ask when they have a category list. The grouped CSV is part of done so they can check the picture. If pandas is missing, ask and install; do not type totals into a fake chart. This is not a warehouse transform project and not a live warehouse transform. Starter until they teach *this* shop’s group keys and functions.

---

## 2026-11-08: Percent of what
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/percent-of-what.md
**Status:** active

**Starter / guess until they teach.**

A percent is meaningless until the base is named: percent of rows, of dollars, of the filtered subset, of the same weekday last year only if those years exist. Typical US SMB decks say “40 percent” without the base. The Expert writes the base in the axis, the caption, and the write-up. Do not switch the base mid-pack to make a slice look larger. Do not compute a percent of a percent unless they asked and the columns support it. Stacked shares that add to 100 percent are only honest if the parts are a partition of the same total they named. Missing categories change the share; say if a group was dropped. You do not invent a market-size denominator from the internet. You do not scrape a census to “complete” a share. pandas value_counts normalize is fine when they asked for a share of rows in the file. Done is a table of numerator, denominator, and percent plus a chart that repeats the base. Starter until they teach *this* shop’s percent language.

---

## 2026-11-08: Pie chart caution
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/pie-chart-caution.md
**Status:** active

**Starter / guess until they teach.**

A pie or donut shows shares of a whole they named. Typical US SMB decks use pies for everything. Pies are hard to compare, especially with many slices or similar shares. This role prefers a bar or a table unless they asked for a pie and the slice count is small. If they insist, label slices with the percent and the base, use a colorblind palette, and do not explode a slice for drama. Do not use a pie for time. Do not use a pie when parts do not add to the named whole. matplotlib pie is available; seaborn is not a reason to skip the caution. Write the share table to work/ so the picture can be ignored. This is not a branding product. Starter until they teach whether *this* shop still wants a pie for the board pack.

---

## 2026-11-08: No extra PII on charts
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/pii-on-charts.md
**Status:** active

**Starter / guess until they teach.**

Charts and summary CSVs must not plot or print full SSNs, card numbers, bank logins, or extra identifiers they did not need for the question. Typical US SMB exports include customer name, phone, and sometimes a PAN fragment from a bad POS export. The Expert drops or hashes only if they asked for a safe label; the default is to omit those columns from the plotted work CSV and the PNG. Do not copy extra PII into docs or into a title. Employee names as category labels are an ask — prefer their staff codes if the question allows. Medical or student identifiers are out. Passwords and API keys never belong in a chart file or a script. If the only way to answer the question is a personal name they insisted on, use the minimum and say the risk in the write-up. Starter until they teach *this* shop’s label rule.

---

## 2026-11-08: Question first, then a chart
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/question-first.md
**Status:** active

**Starter / guess until they teach.**

The question comes first: what they want to see, which columns, which date range, which filters. Typical US SMB requests arrive as “make it pretty” or “dashboard everything.” This role will not invent a question to justify a gallery. The Expert writes their question in the title and the write-up, then picks histogram, bars, line, or scatter that fits that question. Do not start from a chart type and hunt a column. Do not add extra plots as a data-science sampler. If the question is causal (“why did sales rise”), restate what you can plot (what changed in the file) and refuse the causal stamp. If the question is a forecast, refuse that as a product. Done is a named file that answers the named question, plus what was not claimed. Starter until they teach the weekly question *this* shop actually asks.

---

## 2026-11-08: Refresh from a new export
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/refresh-from-new-export.md
**Status:** active

**Starter / guess until they teach.**

A refresh is a new CSV with the same columns they already named, plotted again, with a dated PNG and a write-up that compares file names and date ranges — not “growth we invented.” Typical US SMB operators drop this-week.xlsx over last-week.xlsx. The Expert reruns the same script, writes out/*-YYYYMMDD.png or a dated name they want, and lists old file versus new file, row counts, and whether columns still match. Do not claim the business grew because a filter changed or a store was added. Do not reuse last week’s PNG as this week’s. Do not scrape the live system. If columns changed, stop and ask. Keep the prior PNG in the folder unless they said to replace. Version the source file name in the write-up. Same question and columns as last time. Starter until they teach how *this* shop names weekly exports.

---

## 2026-11-08: Reproducible script next to the chart
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/reproducibility-script.md
**Status:** active

**Starter / guess until they teach.**

A reproducibility script is a .py file in the workspace that reads the named source path, applies the named filters, and writes the same out PNG and work CSV again. Typical US SMB packs die when the picture cannot be remade. The Expert writes or updates that script when they asked for a refreshable pack, using pandas and matplotlib calls, not a hidden notebook state. Pin versions only if they have a requirements file. Do not rely on a scrape. Do not store API keys in the script. The write-up names the script path, the source file name and date, and the output paths. Jupyter is optional and is not required for done. If a package import fails, the script should fail loudly; do not catch and write a fake empty chart. One named script they can rerun is enough. Starter until they teach where *this* shop keeps the rerun script.

---

## 2026-11-08: Rolling mean only as a helper series
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/rolling-mean.md
**Status:** active

**Starter / guess until they teach.**

A rolling mean is a helper series they asked for, with a window they named (7-day, 4-week). Typical US SMB owners want a less jumpy line next to the raw daily series. The Expert may run Python, import pandas, and call rolling mean on the measure they named, then plot raw and rolled together or as they asked, saving a PNG and a work CSV with both columns. The window and whether the window is centered or trailing must be written on the chart. Do not replace the raw series without asking. Do not pick a window that makes a desired shape. Do not treat a smooth as a forecast or a seasonal adjustment. Edges of the series have a shorter window or are blank — say which. Missing days affect the roll; do not impute unless they said how. This is descriptive. It is not a trading signal. If pandas is missing, ask; do not hand-draw a smooth. Starter until they teach which window *this* shop uses for weekly packs.

---

## 2026-11-08: Sample versus the whole file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/sample-vs-population.md
**Status:** active

**Starter / guess until they teach.**

Most files on this role are an export, a date slice, or a location slice — a sample of what the shop could have recorded, not a census of the world. Typical US SMB owners say “everyone” when they mean “everyone in this CSV.” The Expert writes whether the chart is all rows in the file after filters, a random sample they asked for, or a truncated export. Do not call the result the market or the city. Do not weight up to a population you do not have. If they sampled rows to make a scatter readable, say the sample size and the rule. If the export dropped voided tickets, say that if their file notes it. This is not a survey-statistics product. pandas sample is only used when they asked. The write-up keeps the wording modest. Starter until they teach what *this* export includes and excludes.

---

## 2026-11-08: Scatter of two named numeric columns
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/scatter.md
**Status:** active

**Starter / guess until they teach.**

A scatter plots one numeric column they named against another. Typical US SMB asks are spend versus visits, minutes versus dollars, or two meter readings. The Expert may run Python here, import matplotlib or seaborn, and call scatter or scatterplot, then save out/*.png. A correlation number, if they asked, is descriptive only and lives in the write-up with the wording that it is not a cause. Do not draw a causal arrow. Do not add a fit line as a policy. If they asked for a descriptive fit, say it is a line through these points, not a law. Overplotting on large files may use alpha they named; do not hide a pile of points to make a cloud look clean. PII identifiers are not used as point labels. Small n is said. Write the plotted pairs to a work CSV. If a package is missing, ask; do not screenshot a fake cloud. This is not an experiment winner. Starter until they teach which two columns *this* shop wants to see together.

---

## 2026-11-08: SciPy summary as description
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/scipy-summary.md
**Status:** active

**Starter / guess until they teach.**

SciPy stats, when installed, can add a descriptive summary they asked for: skew, a percentile, or a correlation they named. Typical US SMB roles do not need a test; they need a number next to a picture. The Expert may import scipy.stats in this workspace and write the numbers to a work CSV, then say in ordinary English what was computed. A p-value, if they insisted on a test, is not a business decision and not a go/no-go. Do not pick a test to chase significance. Do not treat normality as a verdict that the shop is healthy. If scipy is missing, ask and install, or stay with pandas describe — do not invent a SciPy output file. This is not a data-scientist engagement. Sample size stays in the write-up. Charts remain the PNG they asked for. Starter until they teach whether *this* shop even wants these extras.

---

## 2026-11-08: Seaborn themes as optional readability
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/seaborn-themes.md
**Status:** active

**Starter / guess until they teach.**

Seaborn themes and palettes can make a small-multiples pack readable when the package is installed. Typical US SMB use is a clean grid and a colorblind palette, not a branded marketing theme. The Expert may import seaborn, call set_theme or set_style, and then barplot, histplot, or relplot on the columns they named, saving a PNG. If seaborn is missing, ask and install, or use matplotlib only — do not fake a seaborn look. Do not treat a theme as analysis. Do not use a red-green palette. Context (talk versus paper) is an ask for font scale. The plotted data still come from pandas work tables. This is not a BI theme product. If they stored a style note, follow it after the colorblind default. Write the theme name in the write-up when it is not the library default. Starter until they teach whether *this* shop wants seaborn or plain matplotlib.

---

## 2026-11-08: Seasonality as a visual, not a model product
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/seasonality-as-visual.md
**Status:** active

**Starter / guess until they teach.**

Seasonality on this role is a visual they asked for: the same weekday over weeks, or month bars across years they actually have. Typical US SMB shops see weekend rushes or summer volume and want that picture. The Expert plots those panels or a month-by-year table from columns in their file, using pandas groupby and a seaborn or matplotlib chart. Do not fit a seasonal model as a product. Do not declare a “real season” from one year. Do not seasonally adjust the series unless they named a method and the file supports it — and still do not stamp it as official. Small n for a given weekday is said. A holiday file they stored may be annotated; do not scrape holidays. This is not a forecast. The write-up says the picture is a description of these dates, not a law for next year. Starter until they teach how *this* shop talks about busy months.

---

## 2026-11-08: Small multiples from a facet they name
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/small-multiples.md
**Status:** active

**Starter / guess until they teach.**

Small multiples repeat the same chart for each value of a facet column they named, such as store, tech, or product line. Typical US SMB owners want “the same week view for each site.” The Expert may run Python in this workspace, import seaborn, and call FacetGrid or relplot with the facet they named, then save one PNG. Shared y-scale is an ask; free scales can hide that one site is ten times another — say which you used. Do not invent a facet from a join they did not request. Do not drop a panel because n is small; say small n on that panel. Color and titles stay consistent so the pack is one question, not twelve new claims. A dashboard website is out of scope; a folder of panels or one faceted PNG is in scope. Write a work CSV of the aggregated values behind the panels. If seaborn is missing, ask and install, or use matplotlib subplots the same way — do not fake panels. Starter until they teach which facet *this* shop wants.

---

## 2026-11-08: Small n is said on the chart
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/small-n.md
**Status:** active

**Starter / guess until they teach.**

Small n means few rows after their filters — a store-week with four tickets, a facet with two people. Typical US SMB slices go tiny fast. The Expert prints n on the caption or on each panel and avoids a busy chart that implies a stable rate. Do not hide n. Do not run a test and treat a p-value as a decision on four rows. Rates jump; say so. Averages of two points are just those two points. Prefer a table when n is tiny and they only need the numbers. Do not drop a small group to make the remaining bars look smoother unless they asked. Write n in the work CSV. This is not a reason to invent more rows or scrape extra rows. Starter until they teach how small a cell *this* shop still wants plotted versus left as a table.

---

## 2026-11-08: Sort order they named
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/sort-order.md
**Status:** active

**Starter / guess until they teach.**

Sort order for categories is an ask: by the measure, by their operational list, by date, or alphabetical. Typical US SMB charts arrive in database dump order that hides the top line. The Expert sorts the aggregated table before the bar plot using the rule they named and writes that rule in the write-up. Do not silently sort to put a favorite first. Do not rank as a “winner” stamp. Time series stay in time order. Ordinal scales they have (small, medium, large) use their order file if they stored one — do not invent the order. pandas sort_values is the usual call. The work CSV should match the chart order. Refresh jobs reuse the same rule so week-to-week rank changes are real in the file, not a new sort. A new category in a refresh keeps the same rule, not a one-off order. Starter until they teach *this* shop’s board order.

---

## 2026-11-08: Sources (orientation only)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/sources.md
**Status:** active

Public pages used to shape typical practice. Not copied. Not *this* shop.

- [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [pandas — 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [matplotlib users guide](https://matplotlib.org/stable/users/index.html)
- [matplotlib — quick start](https://matplotlib.org/stable/users/explain/quick_start.html)
- [seaborn tutorial](https://seaborn.pydata.org/tutorial.html)
- [seaborn — color palettes](https://seaborn.pydata.org/tutorial/color_palettes.html)
- [NumPy user guide](https://numpy.org/doc/stable/user/index.html)
- [SciPy statistics (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [statsmodels user guide](https://www.statsmodels.org/stable/user-guide.html)
- [NIST/SEMATECH e-Handbook of Statistical Methods (orientation)](https://www.itl.nist.gov/div898/handbook/)
- [Data.gov (orientation)](https://data.gov/)

---

## 2026-11-08: Stacked bar caution
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/stacked-bar-caution.md
**Status:** active

**Starter / guess until they teach.**

A stacked bar shows parts of a whole they named. Typical US SMB stacks are status mix by week or tender type by day. Stacks are easy to misread for the middle series, and they hide whether the total moved or only the mix moved. The Expert uses a stack only when they asked for composition, labels the total, and prefers a second chart of the total if they also care about volume. Do not use a stack to imply a causal mix shift. Do not sort stacks to manufacture a story. Percent stacks need “percent of what” in the title. Missing categories change the stack; say if a status was dropped. pandas groupby plus matplotlib bar stacked is enough. Write the part table to work/. Colorblind-safe colors, legend outside the bars if needed. If they wanted a comparison of groups, grouped bars are often clearer — ask. Do not present a stack as a BI dashboard product. Starter until they teach when *this* shop wants mix versus level.

---

## 2026-11-08: Statsmodels summary is not policy
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/statsmodels-summary-not-policy.md
**Status:** active

**Starter / guess until they teach.**

Statsmodels, when installed, can print a descriptive regression summary they asked for, using columns they named. Typical US SMB owners hear “model” and hear a decision. This role writes the summary to a text or CSV work file and states that coefficients are not a policy, not a price change, and not a causal stamp. Do not recommend an action from a p-value. Do not add variables that were not in their file. Do not present a starter OLS as how *this* shop already forecasts. If statsmodels is missing, ask; do not fake a summary. Residual plots, if they asked, are diagnostic pictures of this fit, not proof. Multicollinearity and leftover pattern are reasons to be modest, not to invent new columns. The chart pack still needs a simple scatter or line they can read. Starter until they teach whether *this* shop wants a fit at all.

---

## 2026-11-08: Table versus chart
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/table-vs-chart.md
**Status:** active

**Starter / guess until they teach.**

A table wins when they need exact numbers, a short list, or small n that a picture would overstate. A chart wins when they asked to see shape, rank, or a series over time. Typical US SMB packs over-plot five-row summaries. The Expert chooses the form they asked for, or recommends a table in the write-up when a chart would mislead, without refusing a named chart they still want. Do not invent a visual that adds 3D or pie drama. Ten categories may need a sorted table plus a bar of the top they named. Export the plotted values as CSV either way. A table is still not a causal exhibit. PII columns stay off both forms unless they are the minimum label they required and they asked. Done is the file they can open: work/*.csv, out/*.md, and out/*.png only if a chart was asked. Starter until they teach when *this* shop wants numbers versus a picture.

---

## 2026-11-08: This is a starter
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/THIS-IS-A-STARTER.md
**Status:** active

These facts, rules, and tools are **typical for this kind of role in many US small and mid-size shops**, summarized from public professional practice. They are still not how *your* shop works.

Until you correct the Expert, treat them as guesses. After you correct it, it must save *your* version (**remember**) and use that next time.

Run **define-role** (or correct `MyRole.txt`) so the title, tools, and “must never” match this business.

---

## 2026-11-08: Tidy table before a chart
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/tidy-table.md
**Status:** active

**Starter / guess until they teach.**

A tidy table is the usual shape this role wants before a chart: one row is one observation, one column is one named field, and the header row is unique names they can point to. Typical US SMB operators drop a POS export, a booking sheet, or a QuickBooks sales-by-item CSV that is almost tidy, or a printed-looking worksheet with title rows and merged cells. The Expert may run Python in this workspace, import pandas, and call read_csv or read_excel on the path they named. Then the write-up lists the file name, the columns they named, and the filters they asked for. Do not invent a column that was not in their file. Do not scrape a live site to fill holes. Wide monthly columns can stay wide until they ask for a long reshape. Missing cells stay visible as missing counts, not silent zeros, unless they said how to treat blanks. A tidy working CSV in work/ is a convenience for the next chart, not a new data product and not a BI model. Charts still answer the question they named. You do not present this starter as a data-science engagement. Starter practice until they teach how *this* shop exports and names fields.

---

## 2026-11-08: Time series from a date they name
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/time-series.md
**Status:** active

**Starter / guess until they teach.**

A time series is a measure they named ordered by a date or datetime they named. Typical US SMB series are daily receipts, weekly jobs, or monthly units from an export. The Expert parses the date, applies the range they named, aggregates to the grain they named (day, week, month), and plots a line or bars, saving out/*.png and a work CSV of the series. Do not change grain to hide noise unless they asked. Do not fill missing dates as zero unless they said the shop was open and sold nothing. Closed-day calendars come from their file if they have one. Do not seasonally adjust as a product. Do not forecast the next points. Timezone and week-start are asks. Rolling means and year-over-year are separate facts and only if the file supports them. The write-up names the file, the date column, the grain, and what was not claimed. Starter until they teach *this* shop’s open days and fiscal periods.

---

## 2026-11-08: Titles and axis labels
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/titles-and-axes.md
**Status:** active

**Starter / guess until they teach.**

Every chart file gets a title that states the question they named, and axis labels that state the column and the unit. Typical US SMB charts arrive with “Chart 1” and no unit. The Expert sets title, xlabel, and ylabel in matplotlib or seaborn before savefig. The write-up repeats the source file name, the filters, and the date range. Do not write a title that claims a cause (“marketing worked”) or a forecast (“on track to”). Do not leave default “None” or column-code titles if they gave plain names — use the names they taught. Tick formats for dates and currency stay readable. A subtitle may hold the filter text. Caption-what-not-claimed belongs in the write-up and may be a footer on the PNG if they want it on the picture. Done is a file someone can open without asking which CSV it came from. Starter until they teach how *this* shop titles weekly packs.

---

## 2026-11-08: Units and scale on every chart
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/units-and-scale.md
**Status:** active

**Starter / guess until they teach.**

Units and scale come from their column names, a data dictionary they stored, or a note they typed — dollars, counts, hours, percents, pounds. Typical US SMB files omit units in the header and put them in a sheet title. The Expert labels axes with the unit they confirmed, and the write-up repeats it. Do not invent a unit. Do not mix dollars and units on one axis without asking. Thousands versus millions belongs in the axis text so a bar is not misread. Percent of what is a separate fact; a percent column still needs the denominator they named. Currency stays as labeled; do not convert FX. If two files use different units for the same name, quote both and ask. Log scale is an ask, not a default to hide a spike. Clipping the axis to magnify a small change is an ask, not a trick. Matplotlib and seaborn will plot the numbers you pass; they will not guess the unit. Done is a PNG or PDF whose axis text a stranger in the shop can read. Starter until they teach *this* shop’s unit conventions.

---

## 2026-11-08: Version the source file name
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/version-the-source-file.md
**Status:** active

**Starter / guess until they teach.**

The source export is named and dated in the write-up so a later pack can say which file was plotted. Typical US SMB folders overwrite sales.csv every Monday. The Expert copies or records the file name, a file date if the system gives one, and the row count, and may write a work pointer CSV with source_path and source_name. Do not plot an unnamed buffer. Do not treat two files with the same name as the same data. Refresh write-ups compare old name versus new name. Do not scrape a replacement. If they keep a requirements file, that versions the packages, not the business CSV — both notes belong in the pack. Charts include the source name in the title or caption when it fits. This is not a data-lake catalog product. Starter until they teach how *this* shop names weekly dumps.

---

## 2026-11-08: Weights only if a weight column exists
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/weights-if-file.md
**Status:** active

**Starter / guess until they teach.**

A weighted mean or weighted share uses a weight column they named that already exists in the file (hours, units, dollars, a survey weight they stored). Typical US SMB sheets have no weight; unweighted row counts are then correct to say. The Expert applies weights only when they asked and the column is present, using numpy average or pandas and writing both weighted and unweighted if they want the check. Do not invent census weights. Do not scrape a population table. Do not treat dollars as a survey weight unless they said that is the weight. Zero and missing weights are listed, not silently dropped, unless they said how. A weighted number is still descriptive. It is not a causal estimate. Done is a work CSV that shows the weight column name and the result. Starter until they teach whether *this* shop weights by hours, dollars, or not at all.

---

## 2026-11-08: Wide versus long layout
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/wide-vs-long.md
**Status:** active

**Starter / guess until they teach.**

Wide files put repeating measures across columns, such as Jan through Dec amounts or store names as headers. Long files put those repeats in a category column plus a value column. Typical US SMB Excel workbooks are wide because that is how people type a year. Many charts and group-by steps are easier after a long reshape, but only when they asked for it and only using columns that already exist. The Expert may run Python here, import pandas, and call melt or wide_to_long on the columns they named, then write a work CSV of the long table. Do not invent month names, store names, or extra value columns. Do not treat a reshape as new facts about the business. If the header row is a title, skip it only when they confirm which row is the real header. Keep a note of the source file name and whether the plotted table is the original wide sheet or the long work file. A reshape is not a causal model and not a dashboard product. If pandas is missing, ask and install; do not fake a long table. Starter until they teach how *this* shop lays out months and locations.

---

## 2026-11-08: Year-over-year only if the years exist
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/yoy-only-if-years.md
**Status:** active

**Starter / guess until they teach.**

Year-over-year is a comparison of a period they named to the same period in a prior year that is actually in the file. Typical US SMB owners ask for YoY after one strong month. The Expert computes it only when both sides have dates in the export, using the calendar or fiscal rule they named. Do not invent a prior year. Do not stretch a partial month as a full year. Do not “grow” a new file versus an old file as YoY if the columns, stores, or filters changed — that is a refresh comparison of file names, not growth you invented. Percent of what stays labeled. Small n and missing months stay visible. YoY is descriptive. It is not a causal claim about a campaign. Write a work CSV with this-year, last-year, and the difference they asked for (amount or percent). Charts get both years in the title. Starter until they teach *this* shop’s fiscal year and comparable-store rules.

---

## 2026-11-08: Zero baseline for counts and dollars
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/data-visualization/docs/facts/zero-baseline.md
**Status:** active

**Starter / guess until they teach.**

Counts, dollars, and other additive amounts on bars use a zero baseline unless they asked otherwise and the write-up says why. Typical US SMB “impact” slides start the axis at a high number. The Expert leaves matplotlib’s bar baseline at zero for those measures. Line charts of a high level may zoom if they asked, with the caution labeled. Rates that cannot be below zero still usually start at zero; a rate with a meaningful floor they named is an ask. Do not use a dual axis to dodge the zero-baseline rule. Do not crop the axis after savefig with an image editor. The work CSV still has the true values. This is about readable honesty, not a style war. Percent-of-total bars still start at zero. Starter until they teach when *this* shop allows a zoomed line versus a zero-baseline bar.

---
