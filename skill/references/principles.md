# Slide principles

If principles conflict: **B > A > G**.

- **B** = the author's own rules from years as a McKinsey consultant. They always win.
- **A** = rules measured on 203 public McKinsey decks (3,257 pages, newer decks weighted more).
- **G** = widely known consulting practice (Minto, Zelazny).

`QA` says how `check.py` tests the rule; *LLM* means you judge it yourself before rendering.

## B · The author's rules

**B-01 · The title alone gives the slide's point.** A reader who reads only the action title must get the full message. The body proves the title; it does not complete it.
QA (LLM): cover the body. Can you state the slide's conclusion from the title alone? Is there a conclusion in the body that the title lacks?

**B-02 · Reading order, and each region leads with its point.** Lay out top to bottom, left to right. Every panel, column or box opens with its own takeaway, then the detail.
QA (LLM): box and panel headers are takeaway sentences, not labels. Cause → effect, now → future, problem → solution run left to right. A takeaway sidebar sits to the right of its chart.

**B-03 · One slide, one topic.** Going deep on one point with several pieces of evidence is fine. Mixing different points is not.
QA (LLM): every element supports the same title. Panels of a multi-chart slide prove the same claim. If a number needs its own explanation (how it was calculated, what it assumes), move it to the next slide with its formula.

**B-04 · The executive summary alone tells the whole story.** It is the deck's lead messages in order.
QA: every exec item has supporting slides; every non-backup content slide belongs to exactly one exec item (spec ids).

**B-05 · Never show the same information twice on a slide.** A sidebar, callout, row or bottom line must add a new insight or a new data point. Restating what the chart or table shows wastes the space and reads as padding.
A plain sum, difference or remainder of numbers the exhibit shows (100% − 64%, 31% − 26%) is also a repeat: use the space for expected impact (with its basis), a driver, or a quote. The end page does not restate the executive summary: next steps only, unless `key_takeaways` say something new.
QA: fail if a sidebar or callout reuses a data_ref the body shows; warn if it is a plain sum/difference/remainder of body numbers, or if key takeaways overlap exec items. LLM: hide the body; does the sidebar sentence still tell you something new?

**B-06 · Never add unrelated information to fill space.** Everything beside the exhibit explains that exhibit: why the pattern happens, what drives each highlighted element, what it means for the decision. A metric that belongs on another chart breaks B-03 and B-01.
Numbers beside the exhibit are computed from it, but not as a plain sum or difference (B-05): shares and expected impact. QA: warn if a sidebar or callout number is not derived from body values. LLM: reading only the sidebar, is it obvious which part of the chart it explains?

**B-07 · The title gives the implication, not a readout.** State what the evidence means for the decision ("so it is our strongest profit lever", "so we should start now"). Reading the numbers off the chart is the reader's job.
QA (LLM): take the numbers out of the title. Is what remains a judgment (opportunity, risk, action)? If it only lists chart values, rewrite. Sweep every title in the deck.

**B-08 · Every estimate shows its basis, on the slide and in the workbook.** (1) An input from a source names the source on the slide. (2) A number we estimated shows its formula on the slide: number cards joined by operators (`basis` strip or `equation` body) or a `basis` line under a sidebar row. The workbook's Calculations sheet lists every assumption and holds a live Excel formula built from `calc`, not a pasted value.
QA: fail if `calc` does not recompute the value, if an `estimate` lacks `calc` or `assumptions`, or if a slide shows an estimate without its basis. Warn on derived numbers that read like estimates (projected, uplift) but are not marked.

**B-09 · Arrows only for cause → effect, exhibit → interpretation, steps → result.** Parallel evidence gets no arrow: two panels proving one claim, situation next to approach.
Renderer: no arrow between panels unless `connector: "arrow"`; case-example draws one only before Impact; the chart → takeaway sidebar chevron stays.

**B-10 · Every column has a header; every number says what it measures.** Lever and table columns carry headers (`headers: ["Move", "Why it matters"]`); a number in different units carries a `metric` line ("of shoppers say it is hard to find"). In sentences, name the subject: not "~$40M each" but "each of the two peers invested about $40M".
QA: fail if lever numbers have no headers, or mixed units have no metric. LLM: does every "each", "it", "this" point at something obvious?

**B-11 · A bullet reads on its own.** One sentence carries who or what, the metric, the value with its period, and the comparison: "Private label makes up 18% of our sales, against a US grocery average of 26%", not "18% vs. 26%". Lists use parallel grammar. Phrasing and units follow `style.md`.
QA (LLM): read one bullet alone; are subject, metric and comparison clear? check.py tests the unit words.

**B-12 · A full deck leaves no "?" on the slides.** In `deck_detailed`, a placeholder is the last resort: ask the user as multiple choice with a recommended value and its basis first (benchmark, peer, or a calculation from sourced inputs shown as an estimate, B-08), then upload/paste, then a wider search. A target only the user can set is still a choice of 2–3 concrete values.
QA: warn when a `deck_detailed` spec still has placeholders.

## A · Measured on public decks

- **A-01** Numbers in the title appear on the slide (a total bar, highlighted bar, callout or sidebar). QA: title numbers are declared in `lead_message.numbers` with a data_ref shown in the body or sidebar.
- **A-02** Highlight only what the title names; everything else stays neutral. QA: chart `highlight` = title `highlights`; callout and statement emphasis must be words of the title.
- **A-03** Titles: 2 lines recommended; warn at 22–25 words or 3 lines; fail above 25 words. (Median 14 words; 90% ≤ 20.)
- **A-04** A count word in the title equals the number of elements ("three levers" = 3 rows).
- **A-05** A two-clause title ("X rose, while Y fell") gets a two-panel slide.
- **A-06** Chart slides carry a unit line: "**Metric**, unit, period".
- **A-07** Every number links to a source row. Derived numbers list their inputs and formula.
- **A-08** Exec summary numbering = section numbering; the tracker is generated from sections.
- **A-09** Successive titles connect ("However", "As a result") so the titles read as one story.
- **A-10** Reuse the same exhibit across parallel slides and move only the highlight.
- **A-11** The takeaway sidebar is the default for quantitative charts.
- **A-12** Density, matched to 2020+ decks: title 25 pt, body 14 pt, 0.6 in side margins, content down to 91% of the slide; 600–1,100 characters per content slide (charts ≥ 300); boxes 3–5 bullets; KPI tiles with 2–4 driver lines. Conclusion devices are chosen per slide (none 72% of reference pages, sidebar 17%, callout 7%, bottom bar 4%) and varied. QA warns on thin slides, lone charts, thin sidebars, one device on > 40% of slides or three in a row, callout tables without row notes, end pages without next steps. Sidebar value rows (label + number + bar) appear on at most a third of content slides and never on two in a row; QA warns otherwise.

## V · Source verification

A number is only as good as the line it was copied from. These rules make the source workbook something a reader can audit.

- **V-01 The value is in its excerpt.** Every web number carries a verbatim `excerpt`, and the value (or its rounding, with "billion", "%" and "percent" converted) appears in it. A value you computed from the excerpt is a derived number with `calc`, not a copied one. User numbers need an `excerpt` or a `locator` (sheet, row, page). QA: fail when a web number has no excerpt or does not match it; warn when the excerpt has no figure, or user numbers have neither excerpt nor locator.
- **V-02 Same definition.** The excerpt measures the same thing as the label: same currency, period, geography and population. A number in another currency is converted as a derived number (rate and date in `assumptions`). Use `period`, `geography` and `definition` when the label could mean more than one thing. QA: fail on a foreign-currency excerpt behind a `$` unit; warn when the excerpt names years and none is the data point's period. LLM: same population (all firms vs. employer firms), nominal vs. real, calendar vs. fiscal year.
- **V-03 Tier the source, cite the primary.** Every web source has a `tier`. **T1** primary: official statistics, regulators, filings, peer-reviewed papers, a company's own disclosures about itself. **T2** established research firms, industry bodies, reputable surveys. **T3** reporting on someone else's number (news, summaries, other decks): open the primary and cite it instead; if you cannot reach it, name it in `cites`. **T4** not citable for numbers: blogs, vendor marketing about a market, SEO statistics pages, AI-generated pages. QA: fail on a web source without tier or a number from T4; warn on T3 without `cites`, and on title or exec summary numbers that rest on T3.
- **V-04 Use the latest edition.** A web source has a `published` date; one published 4 or more years ago needs a newer edition or a `recency_ok` reason ("latest census; it runs every 5 years"). QA: warn.
- **V-05 Re-check the page before rendering.** `verify.py` opens every web source again and looks for each excerpt (verbatim, near-verbatim with every figure intact, or for spreadsheets the row whose labels and column hold the value). It records `verified` {result: match, not_found or unreachable}. A person or an independent verifier who reads the page may override it (`by: "verifier"`). QA: warn on not_found and unreachable; in `deck_deep`, warn on web numbers never re-checked.
- **V-06 Two sources for the numbers the reader takes away.** In `deck_deep`, title and exec summary numbers get a second, independent source in `corroboration` (another publisher that does not cite the first). If the values differ by more than 2%, a note says which one is used and why. QA: fail when the second source is missing from sources, is the same source, or its value is not in its excerpt; warn on a dependent second source, a difference without a note, and (deck_deep) key numbers with one source.
- **Grades** (source workbook, column Grade): **A** T1/T2, re-checked, key numbers corroborated · **B** excerpt matches, not yet re-checked or one source · **C** T3, not found or unreachable on re-check, or sources disagree without a note; C numbers get a footnote on the slide · **E** our estimate (B-08).

## D · Deep decks (`deck_deep`)

A 30–60 slide deck is built with the seven-step process (Conn & McLean, *Bulletproof Problem Solving*) and laid out with the grammar of long public decks.

- **P-01 Define the problem first.** One sentence: outcome-focused, measurable, time-bound, at the highest level the decision maker owns. The worksheet names the decision maker, success criteria, deadline, accuracy needed and what is out of scope. The one-day answer has exactly three parts: situation, complication, resolution. QA: fail on an empty decision maker, success criteria, deadline or answer part; warn when the statement has no time frame or number.
- **T-01 Level-1 branches are the sections.** 3–5 kept branches, each a testable hypothesis, not a label; each maps to exactly one section, and each section to one exec summary item. Sections without a branch are context or how to make it happen. QA: fail on a branch count outside 3–5 or a branch without exactly one section; warn on label-like hypotheses or a section count that differs from the exec summary.
- **T-02 Prune on purpose, code what stays.** Every leaf is scored on importance × ability to influence. Big but unmovable branches get a `cut_reason` and appear on the appendix slide "what we did not pursue". Every kept node has a code ("2a"); evidence titles start with it. QA: fail on a missing or duplicate code, a title prefix that is not its code, or a slide that proves a pruned or non-leaf node; warn on unscored or low-scoring leaves and on pruned nodes missing from the appendix.
- **T-03 Every leaf is proven.** Each kept leaf has a workplan (analysis, dummied exhibit, candidate sources, knock-out first) and at least one evidence slide. QA: fail on a leaf without a slide; warn on a missing workplan or an evidence slide without `tree_node`.
- **T-04 The data rewrites the titles.** After the analysis, every leaf gets a verdict: confirmed, revised or refuted. A refuted or revised hypothesis never survives as a title; the governing thought and exec summary are rewritten from the verdicts. QA: fail when a refuted or revised leaf's slide still carries the hypothesis as its title; warn on filled leaves without a verdict or a verdict without a note.
- **L-01 Front matter is tiny; every section opens the same way.** At most 4 slides before the first section (cover, context, exec summary, agenda). Each section starts with the repeated agenda (or a divider), then a lead slide that states the section's answer and indexes its leaves, then coded evidence. QA: fail on more front matter, a section without a divider or a tree section without a lead slide; warn when the lead slide is not first or the deck is outside 30–60 slides.
- **L-02 Split long sections.** A section over ~20 slides gets sub-sections (`parent_id`) with their own tracker and lead slide. QA: warn.
- **L-03 The appendix mirrors the body.** 15–30% of a client diagnostic (up to 55% for a policy analysis, optional for a research report), in the order of the main sections: what we did not pursue, methodology, assumptions, "(1/2)" continuations. QA: warn.
- **L-04 Make it happen comes last.** Plan, owners and next steps are the last body section; a client diagnostic always has one. QA: warn.

## G · General practice

- **G-01 Horizontal logic.** The titles alone, in order, tell the story. QA (LLM): find the logic gaps.
- **G-02 Vertical logic.** Every element on a slide proves its title; drop what does not.
- **G-03 MECE.** Framework items, tree branches and levers do not overlap and leave nothing out.
- **G-04 Pyramid.** Exec summary (answer) → titles (arguments) → bodies (evidence).
- **G-05 One chart, one message.** The message picks the chart type, not the shape of the data.
