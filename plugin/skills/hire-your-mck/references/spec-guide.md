# Storyline spec: how to write it

The spec is one JSON file (schema: `scripts/storyline.schema.json`, JSON Schema 2020-12). The renderer reads only the spec. Start from a file in `examples/` and change it.

## Top level

```json
{
  "spec_version": "0.1",
  "mode": "deck_detailed | deck_flow | single_slide",
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

- `role`: `cover`, `exec_summary`, `content`, `backup` (needs `backup_of`; title prefix `"BACKUP:"`), `end_page`.
- `message_type`: `item`, `component`, `time-series`, `frequency`, `correlation`, `structure`, `argument`, `navigation`.
- `lead_message.highlights` must equal the chart `highlight` (A-02). Declare every number in the title in `numbers` with a data_ref (A-01); years are not numbers.
- `clauses: 2` needs `layout.variant: "split_2"` or a panels body.

### Status

| status | Has | Rendered as |
|---|---|---|
| `ghost` | title, archetype, `data_requirements`; optional body skeleton with **only placeholders**; `so_what` = the takeaway to prove | the real exhibit with "?" values + "Takeaway to prove" + "Data needed" |
| `drafted` | body with some placeholders | finished slide, dashed "?" where data is missing, sticker |
| `filled` | every point has a sourced data_ref | finished slide |

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
- `excerpt` is verbatim from the source. It is what makes the source workbook trustworthy.
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
  "note": "Next: confirm spend data before the steering committee"}}
```

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
| A-12 sidebar value rows on more than a third of content slides or on two in a row; B-12 placeholders left in a full deck | warn |
| A-12 density: thin slide, lone chart, thin sidebar, boxes < 3 bullets, KPI without drivers, one conclusion device > 40% or 3 in a row, table callout without row notes, end page without next steps | warn |
