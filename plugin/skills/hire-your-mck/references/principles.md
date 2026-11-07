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

## G · General practice

- **G-01 Horizontal logic.** The titles alone, in order, tell the story. QA (LLM): find the logic gaps.
- **G-02 Vertical logic.** Every element on a slide proves its title; drop what does not.
- **G-03 MECE.** Framework items, tree branches and levers do not overlap and leave nothing out.
- **G-04 Pyramid.** Exec summary (answer) → titles (arguments) → bodies (evidence).
- **G-05 One chart, one message.** The message picks the chart type, not the shape of the data.
