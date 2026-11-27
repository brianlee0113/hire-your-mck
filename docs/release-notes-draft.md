# Release notes draft — 1.4.0 (branch `v1.3-h`, not released)

Version: 1.4.0 rather than 1.3.1, because it adds slide types and a rule that can fail specs made with 1.3.0.

---

**New: calculations that show how a number is built (B-13).** Reviewers found box-style formulas (A ÷ B = C) too simple to trust. `check.py` now fails an equation slide with one operation or only additions and subtractions; an equation shows 3 or more inputs, and the storyline keeps one equation slide (others go on their chart as a basis strip, or to the appendix).

**New slide type: estimate model.** For an estimate built on 3 or more inputs: a driver table (value, basis, low–high range) beside a tornado of the result at each driver's low and high. Ranges sit on the data points; the renderer recomputes the result through `calc`, and the sources workbook lists the ranges.

**New slide type: bar-table.** A few rows compared on several measures, with a small bar in each cell, one scale per column and a grey benchmark row. Used in 43 of the 203 public decks we studied.

**Slide composition.** Two exhibits side by side can now mix chart, table and text, with relative widths (`widths: [2, 1]`). A takeaway about part of a chart can point at it: a dashed outline or numbered dots on the bars, matched to numbered sidebar bullets.

**Less sameness.** Sidebars alternate between a tinted box and an open column with a rule on top, and verdict cells can show a green, amber or red chip (Pass / Watch / Fail, or your own words).

**Readability.** `render.py` warns when body text only fits below 12 pt (captions below 10 pt) and says about how much to cut. Numbers below 1 keep their decimals (0.864, not 0.9), ranges match decimals (3.0–3.7) and write the unit once, and k / M / B print after the number. Table row labels no longer break inside a word.

**Heads-up**
- A spec made with 1.3.0 fails `check.py` if it has an equation slide with one operation or only + and − (B-13). Show the drivers, or move the calculation to a basis strip on the chart slide.
- Sidebars without a `style` now alternate box and open, so a re-rendered deck looks different. Set `sidebar.style: "box"` to keep the old look.

---

Before release (checklist):
- [ ] Decide 1.4.0 vs 1.3.1
- [ ] Bump `plugin/.claude-plugin/plugin.json` and the PyPI version; rebuild plugin and zip
- [ ] Merge product files to `main` only (not `benchmark/`), as for 1.3.0
- [ ] GitHub Release + Claude.ai zip, PyPI, directory repo (after the 1.3.0 listing is published; no push during review)
- [ ] Re-check every example spec and render (0 fail, 0 render warnings) from the installed package
