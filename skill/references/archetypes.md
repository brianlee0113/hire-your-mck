# Archetypes

First decide **what the title compares** (Zelazny's comparison types plus structure and argument), then pick the archetype. `message_type` and `archetype` go on the slide; the body uses one of the `kind`s below.

## Routing: message → archetype

| The title says | Signal words | First choice | Alternative |
|---|---|---|---|
| A is bigger than B / a ranking | largest, top, higher than, gap | `bar-ranking` | `kpi-big-numbers` (≤ 3 items) |
| Changed over time (many points) | grew, fell, trend, since 20xx | `line-trend` | `column-time-series` (≤ 8 periods) |
| Mix changed over time | share rose, mix shift | `stacked-column` | `stacked-100` |
| What adds up to the total / bridge A → B | drivers, contribution, gap | `waterfall-bridge` | `stacked-100` (one point in time) |
| Two things move together | the more…, correlates | `scatter-bubble` (Tier 2) | — |
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
- `bar-ranking` → `bar`: sorted desc, the named bar highlighted, benchmark (e.g. market average) as a dashed last bar.
- `column-time-series` → `column`; `line-trend` → `line` (end-of-line labels, no axis); `stacked-column` → `stacked_column`; `stacked-100` → `stacked_100`; `waterfall-bridge` → `waterfall` (first and last = totals, steps between; `sort: "none"`).
- Fill: `layout.variant: "takeaway_sidebar"`. Sidebar = big number (only if not already on the chart) or a header, then 2–4 **bold lead-in bullets** that read the chart (one per highlighted bar, segment or period), then optional `rows` with numbers **derived** from the chart (share of total, gap, change). Never chart values again (B-05), never unrelated metrics (B-06).

**KPI** (`kind: "kpi"`, `items[]` with `point`, `caption`, `relation`, `drivers[]`) — 2–4 tiles on top; under each, 2–4 driver lines (or what data is missing).

**Panels** (`kind: "panels"`, 2–4 `panels[]` with a takeaway `header`, `unit_line`, `delta`, `body` = chart or kpi) — every panel proves the same title.

**Tables** (`kind: "table"`, `table_type`, `columns`, `rows[]` with `label`, `cells[]`, `highlight`, `badge`)
- `harvey-ball-table` → `harvey`: cells with `rating` 0–4; add a numeric column (cells with `point`) and a last **Verdict** column (text cells). The recommended row gets `highlight: true`. Verdicts live inside the table so rows stay aligned.
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
- `statement` → `text`, `style: "statement"` (`statement.support`, `emphasis` words of the title). At most 2–3 per deck.

**Navigation** (no body): `cover`, `exec_summary`, `end_page`. The end page shows the exec summary with proof points plus `storyline.next_steps`.

## Conclusion devices (pick one per slide, and vary them)

| Device | Spec | Use when |
|---|---|---|
| None | — | Default. The title is the conclusion and the body fills the space |
| Takeaway sidebar | `layout.variant: "takeaway_sidebar"` | Chart slides |
| Callout | `callout: {target, header, detail}` | The title points at one element: a column, table row, process step, framework item or lever (`target` = its header, label, id or code) |
| Dark bar | `so_what` | A synthesis slide you want to nail down |
| Light line | `so_what` + `so_what_style: "line"` | Closing a section |
