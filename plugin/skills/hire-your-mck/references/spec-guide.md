# Storyline spec: how to write it

The spec is one JSON file (schema: `scripts/storyline.schema.json`, JSON Schema 2020-12). The renderer reads only the spec. Start from a file in `examples/` and change it.

## Top level

```json
{
  "spec_version": "0.1",
  "mode": "deck_detailed | deck_flow | deck_deep | single_slide",
  "meta": {"title": "...", "subtitle": "...", "company_name": "...", "audience": "...", "purpose": "...",
           "date": "YYYY-MM-DD", "language": "en-US", "confidentiality": "...", "theme": "navy"},
  "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "...", "content": "..."}],
  "storyline": {"governing_thought": "...", "exec_summary": [...], "next_steps": [...]},
  "sections": [{"id": "1", "title": "...", "exec_item_id": "1", "tracker_label": "Growth"}],
  "slides": [...],
  "data_points": [...],
  "sources": [...]
}
```

- `exec_summary[]`: `{id, text, supports: [slide ids], sub_points: [{text, slide_id}]}` (2–3 sub_points each). Exec item id = section id.
- `next_steps[]`: `{action, owner, timing}`, 3–5 items. Shown on the end page.
- `meta.theme`: `navy` (default), `crimson`, `forest`, `mono`, `vivid`, `slate`, `terracotta`. `meta.font_pair` overrides the theme's fonts (`georgia-arial` default, `aptos-serif-aptos`, `arial`, `calibri`, `aptos`).
- Never put a firm's name in `company_name`; use the user's company.

### Deep decks (`deck_deep`)

`problem`, `issue_tree` and `sections` are required; `meta.deck_type` is `client_diagnostic` (default), `policy_analysis` or `research_report`.

```json
"problem": {"statement": "Should we launch a mid-market AP product by Q3 2027, and at what price?",
            "decision_maker": "CEO and board", "success_criteria": ["Payback under 18 months"],
            "deadline": "Board meeting, March 2027", "accuracy": "±20%", "out_of_scope": ["Enterprise tier"],
            "one_day_answer": {"situation": "...", "complication": "...", "resolution": "..."}},
"issue_tree": [
  {"id": "n1", "code": "1", "label": "Demand", "hypothesis": "Mid-market firms will pay for AP automation within two years"},
  {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "Invoice volumes grow faster than finance headcount",
   "priority": {"importance": "high", "influence": "medium"},
   "workplan": {"analysis": "Invoice CAGR against headcount CAGR", "exhibit": "line-trend, two lines, 2019–25",
                "sources": ["Census ABS"], "knock_out": true},
   "finding": {"verdict": "confirmed", "note": "..."}},
  {"id": "n5", "label": "Regulation", "hypothesis": "...", "cut_reason": "Timing is set by regulators, not by us"}
],
"sections": [{"id": "1", "title": "Demand", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1"}]
```

- A node without `parent` is a level-1 branch (= one section). A node nobody names as parent is a leaf. `cut_reason` prunes the node and everything under it.
- Evidence slides set `"tree_node": "n1a"`; the renderer writes the code ("1a:") before the title, so leave `prefix` out. Continuation pages of a long table add "(1/2)" to the title (R12). The lead slide (first content slide after the section's agenda) has no `tree_node`.
- Each section gets a `question` (deck_deep): the Key questions page lists them under the problem statement.
- Front matter: a `problem_statement` slide (`{"id": "q", "role": "problem_statement", "status": "filled"}`) shows the problem worksheet; it is not a content slide and belongs to no exec item.
- The appendix opens with `{"id": "app", "role": "appendix_divider", "status": "filled"}` (any deck with backup slides and navigation); the agenda then ends with an Appendix row.
- The appendix slide "What we did not pursue" is a `backup` with `"tree_node": ["n5"]` instead of `backup_of`.
- Sections without `tree_node` are context or how to make it happen (last). Sub-sections set `parent_id` and share the parent's `exec_item_id`.

## Slides

Order: `cover`, `exec_summary`, content and backup slides by section, `end_page`.

```json
{
  "id": "3", "role": "content", "section_id": "2", "status": "filled",
  "lead_message": {"text": "...", "numbers": [{"text": "$40M", "data_ref": "gap"}], "highlights": ["Pricing"],
                   "count_word": 3, "clauses": 1},
  "message_type": "component", "archetype": "waterfall-bridge",
  "rationale": "What adds up to the gap -> waterfall",
  "unit_line": "**Operating margin**, $ millions, 2026 to 2027 target",
  "layout": {"variant": "takeaway_sidebar", "sidebar": {...}},
  "body": {...},
  "so_what": "...", "so_what_style": "bar | line",
  "callout": {"target": "Pilot", "header": "Decision point", "detail": "..."},
  "footnotes": ["..."],
  "data_requirements": [...]
}
```

- `role`: `cover`, `exec_summary`, `agenda_tracker`, `section_divider`, `content`, `backup` (needs `backup_of`; title prefix `"BACKUP:"`), `end_page`.
- Navigation slides need only `id`, `role`, `status` (+ `section_id` for a divider, or for an agenda that emphasises a section): `{"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"}`. Their text comes from `sections` and the exec summary.
- `message_type`: `item`, `component`, `time-series`, `frequency`, `correlation`, `structure`, `argument`, `navigation`.
- `lead_message.highlights` must equal the chart `highlight` (A-02). Declare every number in the title in `numbers` with a data_ref (A-01); years are not numbers.
- `clauses: 2` needs `layout.variant: "split_2"` or a panels body.

### Status

| status | Has | Rendered as |
|---|---|---|
| `ghost` | title, archetype, `data_requirements`; optional body skeleton with **only placeholders**; `so_what` = the takeaway to prove | the real exhibit with "?" values + "Takeaway to prove" + "Data needed" |
| `drafted` | body with some placeholders | finished slide, dashed "?" where data is missing, sticker |
| `filled` | every point has a sourced data_ref | finished slide |

On a ghost slide the right third is the "Takeaway to prove / Data needed" panel, so the exhibit is narrower: use at most 3 text columns, short table headers, and put the exhibit you recommend in the **first** data requirement's `recommended_exhibit` (it is the "Exhibit:" line).

## Points: the only way a number gets onto a slide

```json
{"data_ref": "d1-3"}
{"placeholder": true, "label": "mid-market freight spend by region, $B"}
```

Always give a placeholder a `label` that says what data is needed; it is shown to the reader.

## Data points and sources

```json
{"id": "d1-3", "slide_id": "1", "label": "E-commerce SMB volume CAGR", "value": 0.047, "unit": "%",
 "period": "2021–25", "source_id": "s2", "excerpt": "Small e-commerce shippers: 4.7% CAGR",
 "locator": "Table 3", "used_in": "bar: E-commerce SMB"}
{"id": "gap", "slide_id": "1", "label": "Margin gap to target", "value": 40, "unit": "$M", "period": "2027E",
 "source_id": "s3", "derived_from": ["m26", "m27"], "formula": "160 − 120"}
```

- Units: `%` (store fractions: 0.047 = 4.7%), `pp`, `x`, `$M`, `$B`, `$K`, `$`, `k`, or a plain word (`accounts`, `index points`, `months`, `years`).
- Signs: values show their own sign ("−8 pp"); store a gap as a negative number if it is a shortfall. Panel `delta` pills add "+" to positive changes (not to multiples).
- Ranges: `"value": 4, "value_high": 5, "unit": "years"` → "4–5 years".
- One number, one data point: reuse it on every slide that shows it; `slide_id` is the first slide.
- Sources: `{"id", "kind": "user_provided | web | derived", "name", "publisher", "url", "accessed", "published", "input_id"}`. User material beats web (D2). `derived` = your own calculation; it must list `derived_from` and `formula`.
- `excerpt` is verbatim from the source, and the value must appear in it (V-01): `"value": 1.2, "unit": "$B"` matches "$1.23 billion"; `0.047` with `%` matches "4.7 percent". If you computed the value from figures in the excerpt, it is a `derived` number with `calc`. User numbers carry an `excerpt` or at least a `locator` ("P&L export, Margin tab, row 14").
- A number read from a spreadsheet or table cell gets an excerpt in this form, so `verify.py` can find the row: the row labels in quotes, then the column and the cell as shown: `Q7 "did this business use AI in any of its business functions?", answer "Yes"; column 202524 = "17.3%"`.
- `verified` is written by `verify.py --write` (`{"result": "match", "at": "2026-11-10", "by": "verify.py"}`); set `"by": "verifier"` when you or an independent reviewer confirmed the page by reading it.
- `corroboration` (deck_deep: every title and exec summary number): `[{"source_id": "s7", "value": 0.18, "excerpt": "...", "note": "BTOS used: larger sample"}]`. The second source is another publisher that does not cite the first; a value more than 2% off needs the note.
- Web sources carry a `tier` (V-03): `T1` primary (official statistics, regulators, filings, peer-reviewed papers, a company about itself) · `T2` research firms, industry bodies, reputable surveys · `T3` reporting on another source: cite the primary instead, or name it in `"cites"` · `T4` never for numbers (blogs, vendor market claims, statistics aggregators, AI-generated pages). Give `published`; a source 4+ years old needs `"recency_ok": "<why it still holds>"` (V-04).
- When a label could mean more than one thing, pin it down (V-02): `"geography": "US"`, `"definition": "employer firms only; share of firms, not of employees"`. A number in another currency becomes a derived number converted with a dated rate in `assumptions`.
- **Calculated numbers carry `calc` (B-08):** a formula over data point ids with `+ - * /` and spaces around `-`, e.g. `"calc": "(pl1 - us1) * 100"`. check.py recomputes it; the workbook turns it into a live Excel formula on the Calculations sheet.
- **Estimates** (projections, sizings, uplifts) also carry `"estimate": true` and `"assumptions": ["...", "..."]`, and the slide that shows them must show their basis (next section).

## Showing the basis of an estimate (B-08)

Pick one:
- **`basis` strip** under the exhibit, for a chart built on an estimate: `"basis": {"header": "How we projected it", "terms": [{"point": {...}, "caption": "share of sales, 2025 actual"}, {"op": "+", "point": {...}, "caption": "added in 2026–31: 1.5 pp a year from current co-manufacturers (supplier review) × 6 years"}, {"op": "=", "point": {...}, "caption": "share in 2031"}]}`. Siblings built from the same inputs (every bar of one projection) are covered.
- **`equation` body** (archetype `calculation-bridge`) when the estimate is the slide's point: `{"kind": "equation", "terms": [...], "assumptions_header": "The estimate rests on four assumptions", "assumptions": [...]}`. Use it when a number would need its own explanation on another slide (B-03).
- **Row `basis`** in a sidebar: `{"label": "Expected impact if snacks and frozen reach 26%", "basis": "16% of sales × 26% share", "point": {...}}`.

Captions name the source of any input that is not ours.

## Data requirements

```json
{"id": "r2", "description": "Current vs. target operating margin, mid-market accounts, $M",
 "recommended_exhibit": "Waterfall: current margin → 3 levers → target; pricing highlighted",
 "candidate_sources": ["User: account P&L export", "10-K segment note"], "status": "needed"}
```

`status`: `needed`, `found_user`, `found_web`, `not_found`.

## Tables

Row `note`s and a slide `callout` on a table render as the table's **last column** ("Verdict", or `body.verdict_header`), inside the table; the callout row is highlighted and shows the callout header and detail. Row heights come from the text, so keep cells to 2–3 lines.

## Scatter

```json
{"kind": "chart", "chart_type": "scatter", "categories": ["Riverside", "Oak Park", "..."],
 "series": [{"name": "Visits booked online", "points": [...]}, {"name": "No-show rate", "points": [...]}],
 "x_label": "**Visits booked online**, % of visits", "y_label": "**No-show rate**, % of booked visits",
 "x_format": "0%", "value_format": "0%", "highlight": ["Riverside", "Oak Park"],
 "quadrant_labels": ["Low online, high no-shows", "", "", "High online, low no-shows"], "focus_quadrant": "top-left"}
```

A third series makes bubbles (sizes). `reference_lines: "none"` drops the average lines; `trendline: true` adds a dashed linear trend; `label_points: "highlight"` names only highlighted points (default when there are more than 14).

## Heatmap

`table_type: "heatmap"`, every measure cell a `point`. `low_is_better: ["Wait time, minutes"]` inverts that column's shading so darker always means better. A reference row `{"label": "Network median", "benchmark": true, "cells": [...]}` goes first and is not shaded. The row the title names gets `highlight: true`; a slide `callout` on it fills the verdict column.

## Quotes

```json
{"kind": "text", "style": "quotes", "quotes": [
  {"header": "Phone booking loses patients before the visit",
   "text": "I called three times and gave up. **By the time someone answered, I had to get back to work.**",
   "speaker": "Patient, 40s, Riverside", "source_id": "s2", "emphasis": true}]}
```

Quotes are verbatim; never polish or invent them. Without the user's notes yet (flow mode, or drafted), write the quote you need as a placeholder: `{"placeholder": true, "header": "Escalation is the condition for referring", "text": "a physician on what must happen when a patient at home gets worse", "speaker": "Emergency physician, listening session"}`. It renders as a dashed "Quote needed" card, never as a quote.

At most 3 quotes fit with headers on one slide in one row; 4–6 go in two rows of compact cards, so keep them to 1–2 sentences. `speaker` is a role, never a private person's name. `source_id` points at the interview notes or survey (its name appears in the Source line). Put the sample size in the source name ("Patient interviews, n = 18").

## Values the user chose

A target, split or threshold the user picked at a checkpoint is a data point like any other: add an input `{"id": "in-2", "kind": "qa_answer", "label": "Budget split chosen at storyline review", "content": "40/30/20/10"}`, a source `{"id": "s9", "kind": "user_provided", "name": "Budget split chosen by the exec team at storyline review", "input_id": "in-2"}`, and point the data point at it.

## Levers

`body.headers: ["Move", "Why it matters"]` is required when items carry numbers (B-10). If the numbers differ in unit, each item also gets `"metric": "of shoppers say it is hard to find"`, shown under the number.

## Arrows (B-09)

Panels: `"connector": "arrow"` only when the left panel causes the right one; default none. Case: `"connector": "impact_only"` (default) or `"all"`.

## End page

Shows `next_steps` (action, owner, timing). Add `storyline.key_takeaways` only if they say something the exec summary does not (B-05).

## Case example headers

`case` columns default to "Situation" and "Approach". Prefer takeaway headers (B-02): `"situation_header": "Annual tenders locked in rates"`, `"approach_header": "Index pricing, rolled out in a year"`.

## Benchmarks

`body.benchmark: {"label": "US grocery average", "point": {...}}` draws a dashed extra bar on `bar` charts and a dashed horizontal line on `column`, `stacked_column` and `line` charts.

## Sidebar

```json
{"variant": "takeaway_sidebar", "sidebar": {
  "kind": "big_number | bullets | reasons",
  "header": "Digital took share from both other channels",
  "big_number": {"data_ref": "gap"}, "caption": "margin gap to the 2027 target",
  "bullets": ["**Digital:** rose in every period, fastest after self-serve quoting launched",
              "**Broker:** still large on legacy lanes, but lost share every period"],
  "rows": [{"label": "Digital share gain, 2021–25", "point": {"data_ref": "gain"}, "highlight": true}],
  "reasons": [{"header": "Largest prize", "detail": "...", "point": {...}}],
  "note": "Next: confirm spend data before the steering committee",
  "implication": "Start with bank feeds and the close, then extend to invoicing in the same package"}}
```

`implication` is what the exhibit means for us, drawn in its own box at the foot of the sidebar. Use it instead of a last bullet that starts "For us:".

`rows` and `big_number` must be **derived from the exhibit** (B-05, B-06), but not as a plain sum or difference: use shares or expected impact. `check.py` fails a repeat and warns on an unrelated number or a plain difference.

## QA (`check.py`)

| Rule | Level |
|---|---|
| schema, unique ids, ghost bodies hold placeholders only, callout target exists | fail |
| B-04 exec summary ↔ slides | fail |
| A-01 title numbers, A-02 highlights, A-04 count word, A-06 unit line, A-07 sources, L3 sticker on placeholders, status `filled` without placeholders | fail |
| B-05 sidebar or callout repeats the body | fail |
| B-08 calc does not recompute, estimate without calc/assumptions, estimate shown without basis | fail |
| B-10 lever numbers without headers, mixed units without metric | fail |
| units: bare "points" after a number | fail |
| units: "pp", "Nx" or "vs." in a sentence | warn |
| B-05 plain sum/difference in a sidebar, key takeaways repeating the exec summary | warn |
| A-03 title length, A-05 two clauses, D8 title period | warn |
| B-06 unrelated sidebar number | warn |
| S3 section divider without an existing section; quote citing an unknown source; scatter without x and y series; heatmap `low_is_better` naming no column | fail |
| A-07 quote without `source_id` | warn |
| V-01 web number without excerpt or not matching it; V-02 foreign-currency excerpt behind a `$` unit; V-03 web source without tier, number from a T4 source | fail |
| V-06 second source missing from sources, the same source, or its value not in its excerpt | fail |
| V-05 excerpt not found or page unreachable on re-check, web numbers not re-checked (`deck_deep`); V-06 dependent second source, values differ without a note, key numbers with one source (`deck_deep`) | warn |
| V-01 excerpt with no figure, user numbers with neither excerpt nor locator; V-02 period not in the excerpt; V-03 T3 without `cites`, title or exec numbers on T3; V-04 source without `published` or 4+ years old | warn |
| P-01 empty decision maker, success criteria, deadline or one-day answer part; T-01 level-1 branches outside 3–5 or not one section each; T-02 missing or duplicate code, prefix that is not its code, slide on a pruned node; T-03 leaf without an evidence slide; T-04 refuted or revised leaf still titled with its hypothesis; L-01 front matter over 4, section without divider or lead slide (`deck_deep`) | fail |
| S3 full agenda straight before the first section tracker; L-03 backup without an appendix divider; A-09 one title shape on over a quarter of titles (", so" over a tenth) or three in a row; A-13 one archetype over 30% or tables over 40% of a 15+ slide deck | warn |
| P-01 statement without time frame; T-01 label-like hypothesis; T-02 unscored or low leaf, pruned node not in the appendix; T-03 no workplan; T-04 no verdict; L-01 outside 30–60 slides; L-02 section over 20; L-03 appendix share or order; L-04 make it happen not last (`deck_deep`) | warn |
| S3 navigation in a deck with fewer than 10 content slides; section dividers and agenda trackers mixed in one deck | warn |
| A-12 sidebar value rows on more than a third of content slides or on two in a row; B-12 placeholders left in a full deck | warn |
| A-12 density: thin slide, lone chart, thin sidebar, boxes < 3 bullets, KPI without drivers, one conclusion device > 40% or 3 in a row, table callout without row notes, end page without next steps | warn |
