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
| A market split two ways, each by share | segment × player, mix by size | `marimekko` | `stacked-100` (equal widths) |
| A share of a whole, one to four of them | of firms, share of, one in four | `donut` | `kpi-big-numbers` |
| Who plays where | players, landscape, ecosystem | `landscape` | `comparison-table` |
| What changes | from … to, shift, move from | `from-to` | `comparison-table` |
| Where several conditions meet | sweet spot, overlap, where … meet | `venn` | `framework-pillars` |
| Where it is, by country or US state | across states, regions, countries, where | `map` | `bar-ranking` (when the ranking matters more than the place) |
| Measures ranked by cost, each with its own volume | cost curve, cheapest first, abate, save at, below the price | `cost-curve` | `bar-ranking` (no volumes) |
| Who does what in the organization | report to, owns, runs, governance, new unit | `org-chart` | `process-flow` (hand-offs, not reporting lines) |
| One initiative in detail, one of a series | 1a:, initiative, how we would, owner | `initiative-one-pager` | `case-example` (something that worked elsewhere) |
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
- `marimekko` → `marimekko`: `rows` (labelled once at the left, no legend), `columns[]` with `label`, `width` (point: the column's share) and `cells` (one point per row, shares of the column summing to 100%); `highlight` outlines cells; `width_label` says what widths measure. No y axis; drawn as shapes. Most reference marimekkos sit beside a takeaway sidebar.
- `donut` → `donut`: 1–4 `items` (`label`, `sub`, `point` as a share, `emphasis` for the primary colour, `detail` of 2–3 short lines on what drives the share). Equal sizes even when bases differ; the share runs from 12 o'clock clockwise, the rest grey, the value in the centre; the group sits in the vertical middle. Pies are not offered.
- `landscape` → `landscape`: `segments[]` (`label`, `items` of names, 12 at most), `marked` names outlined and bold with `marked_label` saying why, `us` filled, `hedge` ("Examples, not exhaustive"), a `note` line under each column saying what the segment shows. The key (outline / fill and their meaning) sits top right. Names only, never logos. A grid alone does not say anything: add a takeaway sidebar or column notes.
- `from-to` → `from_to`: `from_label`, `to_label`, 3–7 `rows` (`from`, `to`, optional `label` for a dimension column, optional `to_detail` or `from_detail` line). The To side is the strong one; one arrow between the headers.
- `venn` → `venn`: 2–3 `sets`, `centre` (what sits where they all meet) and `notes`, drawn as a full-height panel beside the circles; other overlaps stay unlabelled. Translucent circles of one hue.
- `map` → `map`: `geo` `world` (ISO 3166 alpha-3 codes) or `us_states` (USPS codes, Alaska and Hawaii as insets); `style` `choropleth` (`regions[]` with a point each, `breaks` for 4–6 classes of one hue, round edges such as 15/20/25/30%; missing regions show as No data), `highlight` (1–3 `groups` of codes in accent colours on grey) or `bubble` (`regions[]` with points; circle area = value; a size key with round values). `callouts[]` (header, text, optional point) sit in aligned edge columns with elbow leaders; `extent` crops a world map to `europe`, `americas` or `asia`. Drawn from Natural Earth outlines (public domain) as one editable shape per region. Reference maps: no Antarctica, light grey land, white hairline borders, legend in empty sea; pair a choropleth with a takeaway sidebar.
- `cost-curve` → `cost_curve`: `items[]` with `label`, `width` (volume: kt, hours, customers) and `height` (unit cost; negative = saves money) as points, optional `group` (max 4, shown as a legend in shades of one hue). The renderer sorts cheapest first, draws bars edge to edge with the zero line, labels every bar up to 15 with staggered leader lines, and keeps the y title horizontal at top left. `price_line` (dashed, e.g. a carbon price), `bracket` (brace with a pill value over a run of bars; it must carry the title number), `tail` (grey "no measure yet" block), `highlight` (bars the title names). Drawn as editable shapes because native charts cannot vary bar width.
- `org-chart` → `org`: `nodes[]` (`id`, `label` of 6 words at most, `sub` one short line, `parent`, `status` `new`/`changed`, `count` for stacked copies such as one per region, `dotted` for advisory lines). Same-size boxes per level, elbow connectors, a legend when anything is new or changed. Committees outside the hierarchy go in `side` (oval beside the node they advise). Role text never goes in the boxes: put 1–3 `roles` callouts ("Key roles"); they stack in a right-hand column and the chart takes the full height. Boxes and type grow to fill the space, so a small chart is not left floating in white space. At most 6 boxes on a level.
- `initiative-one-pager` → `initiative`, one `template` per series (the one-pagers of one section): `actions_impact` (band with the aim and the impact pill, label column + key actions, and a result per row in a right-hand column via `rows[].impact` {point, text}, owner and timing), `description_case` (description 1/3, case example 2/3 with an impact box), `pros_prereqs` (description, benefits and concerns with vertical labels, prerequisites with check marks). The title starts with the initiative's code (`prefix` "1a:", or `tree_node` in deep decks). Impact is a point, pulled out of the text; use "~" or a range in the label when it is an estimate.
- `statement` → `text`, `style: "statement"` (`statement.support`, `emphasis` words of the title). Rare: 1% of reference pages, mostly keynotes and vision documents. Not in client diagnostics or policy analyses; at most one in a talk.

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
