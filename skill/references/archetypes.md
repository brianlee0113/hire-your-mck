# Archetypes

First decide **what the title compares** (Zelazny's comparison types plus structure and argument), then pick the archetype. `message_type` and `archetype` go on the slide; the body uses one of the `kind`s below.

## Routing: message → archetype

| The title says | Signal words | First choice | Alternative |
|---|---|---|---|
| A is bigger than B / a ranking | largest, top, higher than, gap | `bar-ranking` | `kpi-big-numbers` (≤ 3 items) |
| Changed over time (many points) | grew, fell, trend, since 20xx | `line-trend` | `column-time-series` (≤ 8 periods) |
| Mix changed over time | share rose, mix shift | `stacked-column` | `stacked-100` |
| What adds up to the total / bridge A → B | drivers, contribution, gap | `waterfall-bridge` | `stacked-100` (one point in time) |
| Two things move together | the more…, correlates, goes with | `scatter-bubble` | `matrix-2x2` (judged positions, no data) |
| Many items on several measures | trails on, scorecard, across measures, vs. the median | `heatmap` | `data-table` |
| What people told us | customers say, interviews, in their words | `quote-interview` | `bullet-argument` |
| How respondents answered | n% of respondents | `survey-bars` | `bar-ranking` |
| Made of N elements or pillars | three factors, four pillars | `framework-pillars` | `text-columns` |
| Happens in steps | phases, steps, value chain | `process-flow` | `timeline-roadmap` (with dates) |
| Options compared on the same criteria | option A vs B | `comparison-table` | `harvey-ball-table` (qualitative ratings) |
| N things to do | levers, initiatives, must | `numbered-levers` | — |
| Worked elsewhere | case, benchmark, peer | `case-example` | — |
| One claim, 2–4 pieces of evidence | two clauses in the title | `multi-chart-panel` | — |
| Qualitative argument | unlikely, because | `bullet-argument` | `text-columns` (contrast) |
| Priority on two dimensions | where to play, prioritize | `matrix-2x2` | — |
| Breaks down into causes or parts | breaks down into, drivers of | `issue-tree` | — |
| A section opener or thesis | — | `statement` | `section-divider` |
| Our own estimate, and how it is built | would add, uplift, worth, at today's pace | `calculation-bridge` | `basis` strip on the chart slide |

Rules: two clauses in the title → two panels; no arrow between them unless one causes the other (B-09). A count word ("three") → exactly that many elements. A question title → the answer goes in a callout or sidebar.

## Body kinds and how to fill them

Each line: archetype → `body.kind` (key fields) — how a full slide looks.

- `calculation-bridge` → `equation` (`terms` with `op`, `assumptions_header`, `assumptions`) — 3–5 number cards joined by × + = with the result card dark, then the assumptions under a takeaway header (B-08).

**Charts** (`kind: "chart"`, `chart_type`, `categories`, `series[].points`, `highlight`, `sort`, `value_format`, optional `benchmark`)
- `scatter-bubble` → `scatter`: `categories` name the points; `series[0]` = x values, `series[1]` = y values, optional `series[2]` = sizes (bubbles). `x_label` / `y_label` as `"**Metric**, unit"`, `x_format` / `value_format`. Dashed average lines split the plot by default; name the areas with `quadrant_labels` (TL, TR, BL, BR) and accent one with `focus_quadrant`. `highlight` = the points the title names. `trendline: true` only when few labels sit near the line. Pair with a sidebar that reads the outliers.
- `bar-ranking` → `bar`: sorted desc, the named bar highlighted, benchmark (e.g. market average) as a dashed last bar.
- `column-time-series` → `column`; `line-trend` → `line` (end-of-line labels, no axis); `stacked-column` → `stacked_column`; `stacked-100` → `stacked_100`; `waterfall-bridge` → `waterfall` (first and last = totals, steps between; `sort: "none"`).
- Fill: `layout.variant: "takeaway_sidebar"`. Sidebar = big number (only if not already on the chart) or a header, then 2–4 **bold lead-in bullets** that read the chart (one per highlighted bar, segment or period), then optional `rows` with numbers **derived** from the chart (share of total, gap, change). Never chart values again (B-05), never unrelated metrics (B-06).

**KPI** (`kind: "kpi"`, `items[]` with `point`, `caption`, `relation`, `drivers[]`) — 2–4 tiles on top; under each, 2–4 driver lines (or what data is missing).

**Panels** (`kind: "panels"`, 2–4 `panels[]` with a takeaway `header`, `unit_line`, `delta`, `body` = chart or kpi) — every panel proves the same title.

**Tables** (`kind: "table"`, `table_type`, `columns`, `rows[]` with `label`, `cells[]`, `highlight`, `badge`)
- `harvey-ball-table` → `harvey`: cells with `rating` 0–4; add a numeric column (cells with `point`) and a last **Verdict** column (text cells). The recommended row gets `highlight: true`. Verdicts live inside the table so rows stay aligned.
- `heatmap` → `heatmap`: rows = items, columns = measures, every cell a `point`. Each column is shaded by rank (darker = higher; list columns where lower is better in `low_is_better`, and darker then means better). A reference row (`benchmark: true`, e.g. network median) goes first and stays unshaded. The row the title names gets `highlight: true` (outlined); add row `note`s for a verdict column.
- `comparison-table` → `comparison`; `data-table` → `data`.

**Structure**
- `framework-pillars` → `framework` (`shape`: pillars / house / tiles, `roof`, `foundation`, `items[]` with `header`, `detail[]`, optional `point` + `point_caption`, `footer`, `emphasis`).
- `process-flow` → `process` (`steps[]` titled items; `emphasis` on the decisive step; `footer` for each step's gate; `from_to: true` for a From → To table using `detail[0]`, `detail[1]`).
- `timeline-roadmap` → `timeline` (`periods`, `rows[]` with `bars[]` `start`/`end`/`label`/`emphasis`, `milestones[]`).
- `matrix-2x2` → `matrix` (`x_axis`, `y_axis` with `label`/`low`/`high`, `quadrant_labels` TL, TR, BL, BR, `focus_quadrant`, `items[]` with `x`, `y` in 0–1 and optional `size`). Pair with a sidebar of kind `reasons` (numbered reasons, each with an optional point).
- `issue-tree` → `tree` (`root` with `label`, `point`, `operator`, `children` up to 3 levels, `mece_note`).

**Text**
- `text-columns` → `text`, `style: "columns"` (2–4 columns; header = takeaway; 3–5 bullets; optional `point`, `point_caption`, `footer`, `emphasis` on the answer).
- `bullet-argument` → `text`, `style: "bullets"`.
- `numbered-levers` → `levers` (`items[]` with `code`, `text`, `point`; `total`).
- `case-example` → `case` (`subject`, `situation[]`, `approach[]` with 3–4 bullets each, `impact[]` with 2–3 big numbers).
- `quote-interview` → `text`, `style: "quotes"` (2–6 `quotes[]` with verbatim `text`, `speaker` = role and type of organization, never a private name, `header` = the takeaway the quote proves, `source_id` = the interview notes or survey, `emphasis` on the card the title points at). Mark the words the title rests on with `**…**`. Quotes are evidence, so they need a source like numbers do; a quote you do not have yet is `placeholder: true` (spec-guide.md).
- `statement` → `text`, `style: "statement"` (`statement.support`, `emphasis` words of the title). At most 2–3 per deck.

**Navigation** (no body): `cover`, `exec_summary`, `agenda_tracker`, `section_divider`, `end_page`. The end page shows `storyline.next_steps`.
- `agenda_tracker`: contents page built from `sections` (section name and first page). Without `section_id` it is the agenda; with `section_id` it is repeated before that section with the section emphasised.
- `section_divider` (`section_id` required): section number and name on a dark panel, the section's exec item as the claim beside it (`lead_message.text` overrides it).
- Use navigation only in decks with **10+ content slides**; in a shorter deck the exec summary is the contents. Pick **one** style for the whole deck:
  - **Section dividers** (default): a `section_divider` before each section. No agenda page; the exec summary already lists the sections, and each divider shows where the reader is.
  - **Agenda tracker**: an `agenda_tracker` after the exec summary, then the same page with `section_id` before each section.
- The agenda lists section names and pages only; the claims stay on the exec summary (B-05).

## Conclusion devices (pick one per slide, and vary them)

| Device | Spec | Use when |
|---|---|---|
| None | — | Default. The title is the conclusion and the body fills the space |
| Takeaway sidebar | `layout.variant: "takeaway_sidebar"` | Chart slides |
| Callout | `callout: {target, header, detail}` | The title points at one element: a column, table row, process step, framework item or lever (`target` = its header, label, id or code) |
| Dark bar | `so_what` | A synthesis slide you want to nail down |
| Light line | `so_what` + `so_what_style: "line"` | Closing a section |
