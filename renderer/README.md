# Renderer v0.4 (density v2, all Tier 1 kinds + scatter, heatmap, quotes, agenda, divider)

Storyline spec → `deck.pptx` (native, editable charts and shapes) + `deck-sources.xlsx`.

```
python tools/spec/check.py docs/spec/examples/example-deck.json   # QA first
python -m renderer docs/spec/examples/example-deck.json --out output [--theme crimson] [--font-pair arial]
```

- Theme and fonts: `meta.theme` / `meta.font_pair` in the spec, or the flags. Values live in `templates/themes.json`; tokens in `renderer/tokens.py`.
- Every number comes from `data_points` via `data_ref`. Placeholders render as a dashed “?” and add the `ILLUSTRATIVE — DATA NEEDED` sticker (D5, L3).
- The source workbook has an Index sheet, one sheet per content slide (sourced rows, then MISSING rows), and a Sources sheet.
- `examples/showcase.json`, `examples/showcase-2.json` and `examples/showcase-3.json` (10 content slides with section dividers; scatter, heatmap, quotes): one slide per drawn kind, all pass `check.py`.

## Density (A-12)

Tokens in `renderer/tokens.py` match 2020+ public decks (28 decks, 577 content pages): title 25 pt, body 14 pt,
side margins 0.6 in, content down to 91% of the slide height. Every element stretches to the body area; a so-what
bar is one of several conclusion devices, chosen per slide: none (title carries it), takeaway sidebar, `callout` on one element, `so_what` as a dark bar, or `so_what_style: line`. check.py warns when one device covers over 40% of content slides or three in a row. Measured on the example decks: title, body size,
margins and bottom extent match the references; median text is ~520 chars per slide vs ~800 in the references
(chart slides pull it down), and dark ink covers less of the body (0.26 vs 0.45) because v2 uses tinted panels.

## What v0.2 draws

| Spec | Status |
|---|---|
| cover, exec_summary, end_page | drawn |
| content / backup: tracker, title, unit line, sticker, footnotes, source line, page number | drawn |
| ghost slides (flow mode): real exhibit skeleton with “?” values, takeaway to prove, data needed | drawn |
| `chart`: bar (sorted, highlight, benchmark), column, stacked_column, stacked_100, line (end labels), waterfall (invisible base series) | drawn, native charts |
| `kpi`, `matrix` (2x2), `table` (comparison, harvey with shape-based balls, data), `text` (bullets, columns, statement) | drawn |
| layout `takeaway_sidebar` (big number, bullets or numbered reasons; chevron) and `so_what` bar | drawn |
| `panels` (2–4 panels, takeaway header, unit line, delta pill, chart or KPI inside) | drawn |
| `framework` (pillars / house / tiles, roof and foundation bars, numbered headers, optional impact line) | drawn |
| `process` (chevrons darkening left to right, step bullets, optional impact line; `from_to: true` = rows of header · from → to, using `detail[0]` and `detail[1]`) | drawn |
| `timeline` (period header, milestone diamonds, workstream rows with bars; emphasis bars in the highlight color) | drawn |
| `tree` (left-to-right boxes, elbow connectors, operator between siblings, values or “?”, MECE note) | drawn |
| `levers` (code badge, lever, share bar, value, total row) | drawn |
| `case` (subject, situation → approach → dark impact block with 2–3 big numbers) | drawn |
| chart `scatter` (native XY or bubble chart, dashed average lines, area names, labeled points, optional trendline) | drawn |
| table `heatmap` (each column shaded by rank, `low_is_better` inverts, benchmark row unshaded, outlined target row, shading legend) | drawn |
| text `quotes` (2–6 quote cards: takeaway header, quotation mark, verbatim quote with accented phrase, speaker role; source in the Source line) | drawn |
| roles `agenda_tracker` (section names and pages, current section emphasised) and `section_divider` (dark number panel, section tracker, claim) | drawn |

Sidebar value rows draw comparison bars only when all rows share a unit. Statement and support text sit together as one centered block.

Text that would overflow a box shrinks (one size per slide, never below 11 pt).

Checked by exporting through Microsoft PowerPoint to PDF. macOS Quick Look does not render chart formatting and is not a reliable preview.
