# Feedback log

Each round: what was said → where it went (principle, check.py, renderer, examples, deck only) → how it was verified.
The point is to see whether the same comment comes back in later rounds.

## Round 1 · 2026-11-06 · FreshCart dry-run deck

| # | Feedback (page) | Rule | Principle | check.py | Renderer | Examples |
|---|---|---|---|---|---|---|
| R1 | Title only reads the two charts (p4); sweep all titles | B-07 implication, not readout | new | LLM judgment | — | FreshCart p4, p10 titles |
| R2 | 0.7 pp and 1.5 pp a year have no visible basis; Excel only adds (p3, p8) | B-08 estimates show their basis | new | `calc` recomputed; estimate needs `calc` + `assumptions` + basis on slide (fail) | `basis` strip, `equation` body, row `basis`; Calculations sheet with live formulas and assumptions | FreshCart new p5, p9; all derived numbers in 4 decks got `calc` |
| R3 | Move the 0.7 pp with its formula to the next slide (p3) | B-03 addition | updated | — | `calculation-bridge` archetype | FreshCart p5 |
| R4 | Arrows between parallel panels / Situation→Approach (p4, p7) | B-09 arrows only for cause, interpretation, result | new | — | panels: no arrow unless `connector: "arrow"`; case: only before Impact | all decks (default) |
| R5 | Lever table: no column headers; % and pp unclear; "~$40M each" (p9) | B-10 headers and metric | new | lever numbers without headers / mixed units without metric (fail) | header row; metric line under each number | FreshCart p10, showcase-2 p8 |
| R6 | Sub-bullets too clipped to read alone (p2) | B-11 bullet reads on its own | new | LLM judgment | exec summary fits long text | FreshCart exec summary |
| R7 | 36% = 100% − 64% (p5); box values are plain +/− (p6) | B-05 plain sum/difference is a repeat | updated | warn | — | FreshCart p6, p7; showcase p3–p5 |
| R8 | Key takeaways ≈ exec summary (p10) | B-05 deck level | updated | warn on overlap | end page = next steps only by default | all decks |
| R9 | "points" → "percentage points"; learn unit notation | style.md Units | new section | bare "points" fail; "pp", "Nx", "vs." in sentences warn | — | all decks |
| R10 | Sentences hard to read; learn McKinsey phrasing | style.md Phrasing | new section (18 mckinsey.com pages, patterns only) | — | — | FreshCart governing thought, exec, titles |

**Verified by:** check.py 0 fail / 0 warn on all four example decks; FreshCart re-rendered and reviewed page by page; fresh-agent dry run on a new topic (Northwind Clinics) — result below.

**Dry run (Northwind Clinics, online check-in, 7 content slides, fresh agent with SKILL.md only):** check.py 0 fail / 0 warn on the first run.
- Held: titles state the implication (B-07); both estimates show number cards and assumptions, with live formulas in the Calculations sheet (B-08); no arrows between parallel panels (B-09); exec sub-points read on their own; units written as "percentage points", "3.5 times", "compared with" (B-11, style.md); end page = next steps only (B-05).
- Fixed after the run: an equation card number wrapped ("1,150,000"); exec summary rows overlapped when one item ran long.
- Open (next round): plain-word units ("k", "M", "minutes") are not printed by `fmt()`; numbers written only in text (n = 2,400, "8 clinics") never reach the workbook; D5 matches a value anywhere in the spec, not on that slide; timeline labels can collide; one slide cannot carry two estimate bases; no way to cite an estimate built on an earlier page; example deck repeats data points across slides against the reuse rule.

**Follow-up (same day):** exec summary looked too empty → the renderer now sizes exec text to fill the page (up to 1.3× the base size, shrinking only when it does not fit) and gives each item a row in proportion to its text.

## Round 2 · 2026-11-06 · senior-job-advisor-launch deck (made with the skill on claude.ai)

| # | Feedback | Cause | Fix |
|---|---|---|---|
| F1 | Mid-flow questions (age cutoff, pilot city, business model) had to be typed | multiple-choice rule covered checkpoints only | SKILL.md: every assumption to confirm is one multiple-choice question, recommendation first with a reason; never end on open questions |
| F2 | First questions missed "do you have research?" and theme | Checkpoint 1 asked mode only | SKILL.md: Checkpoint 1 asks what to build, material, audience and theme together |
| F3 | Sidebar value rows (label + number + bar) on 3, 4, 6, 7p | SKILL.md recommended rows for derived numbers; no variety check | A-12: rows on ≤ 1/3 of content slides, never two in a row (check.py warn); default sidebar = header + interpretation bullets |
| F4 | 10p verdict as boxes beside the table (old design) | only Harvey tables had the verdict column | renderer: notes and callout go into the table's last column for every table |
| F5 | "?" values in a full deck (13p) | placeholders were the default when data was missing | B-12: full deck leaves no "?"; ask with a recommended value and its basis first (check.py warn) |
| F6 | Sidebar box overflows (3, 4, 6p) | row heights fixed; 2-line labels not counted | renderer: row heights from the text, rows anchored to the sidebar bottom, bullets sized conservatively |
| F7 | 8p Harvey balls off their rows, legend over the last row; 10p last row over the note | PowerPoint grew rows on its own; overlays used the planned height | renderer: row heights computed from text (font shrinks to fit), overlays placed on those heights |
| F8 | Misalignment in general | nothing checked layout after drawing | renderer `layout_check`: warns on text running into the element below, text spilling out of a shape, shapes off the slide; SKILL.md: fix every warning and re-render. Timeline milestone labels now take a second line instead of colliding; bar labels shrink to fit |

**Verified by:** check.py 0 fail / 0 warn and layout_check 0 warnings on all four example decks and the Northwind deck; table and timeline slides re-rendered and reviewed.

**Follow-up (Harbor dry-run deck review):** remaining overlaps (4p gap above the big number, 5p bullet into the rows, 7p "$4.6M" wrapping and a caption leaving its card, 8p highlight stroke thinner under the header) all came from guessing text width as "characters × average width". New `renderer/measure.py` wraps text with the real font files (Pillow; Arial/Georgia, or metric-compatible Liberation/Gelasio on Linux). Every layout height (sidebar, exec summary, tables, equation cards, tree nodes, timelines) and the post-render `layout_check` now use it. Outlines are drawn after header fills so strokes keep one width. All example decks, Northwind and Harbor: 0 layout warnings, checked visually.

## Round 3 · 2026-11-27 · box equations look too simple (author's blind slide reviews, 11-17 and 11-21/23) · open

Repeat of R7 (Round 1): the same comment came back in 6 of 13 reviewed pairs, across both review rounds.

| Review | Pair · deck flagged | Comment (summary) |
|---|---|---|
| 11-17 (c2, c5) | P1 · C2 (skill 1.2.0, full deck) | box-drawn calculations lower trust; lead only lists the slide content |
| | P2 · C (skill 1.2) | over-simplified box calculations lower trust, and repeating them makes it worse |
| | P3 · C (skill 1.2) | box lists make the content look too simple |
| 11-21/23 (holdout) | P2 · B (6-line prompt) | box +, −, ×, ÷ formulas are easy to read but too simple, which lowers trust |
| | P4 · E1 (skill + self-check), c10 | "the simple formula" was the biggest minus (reason for the verdict) |
| | P6 · H2a (B analysis → skill), c7 | a backup made of a simple calculation is rare in consulting; needs work |

**Cause.** R2/R3 asked to show the basis of every estimate; the answer was the `equation` body and the `calculation-bridge` archetype (3–5 number cards joined by × + =). It is used for every estimate, including two-term sums and differences, and it is the only form a backup calculation can take. The c10 E1 deck has 4 of them. The basis is now visible, but it reads as arithmetic rather than analysis. B decks (no skill) do the same, so the habit is not only the skill's, but the skill makes it a template.

| # | Task | Where | How to check |
|---|---|---|---|
| T1 | A plain sum or difference never gets its own equation slide: an `equation` of 2–3 terms with only + / − fails (B-05, today warn only) and goes into a `basis` strip on the chart slide instead | check.py, SKILL.md, archetypes.md | check.py fails a 2-term +/− equation; example decks still 0 fail |
| T2 | At most one `calculation-bridge` in the main storyline, and never two in a row; further estimates go to the appendix | check.py warn (like A-12), deep-deck.md | warn on the c10 E1 spec (4 bridges) |
| T3 | Backup calculations look like a model, not a box equation: a driver table (driver, value, unit, source or assumption, low/high range) with the result, plus a sensitivity view (low/base/high or tornado) when an assumption is uncertain | new archetype (e.g. `estimate-model`), renderer, spec-guide.md, schema | renders editable; the workbook's Calculations sheet ties to the table |
| T4 | When an equation stays in the main storyline, the cards carry more than the number: unit, source or assumption tag, and the range of each driver; the result card shows the range too | renderer `equation`, schema | layout_check 0 warnings; side-by-side with the old card |
| T5 | Re-test: rebuild c10 E1 and c7 H2a with T1–T4, then blind-review the old and new decks (pairs on the equation and backup slides) | benchmark | the author no longer flags "simple formula" on those slides |

**T1 done (2026-11-27), wider than planned.** In the holdout E1 decks most box equations were one operation of any kind (A ÷ B = C), not only + and −, so rule B-13 fails an `equation` body (content or backup) with two inputs, or with only + and −. It flags 7 slides in 6 holdout E1 decks. Two examples rewritten to show their drivers: FreshCart 2b (38% − 29% = 9 pp × 8% = 0.7 pp), Cobalt Ledger deep L4 (20 engineers × $194.3K = $3.9M ÷ $414.2K a month = 9.4 months). All example decks 0 fail; both slides rendered and checked in PowerPoint.

**T3 done (2026-11-27).** Layout and scope chosen by the author: driver table + tornado; for estimates built on 3 or more inputs, with B-13 equations still allowed in the storyline. New archetype `estimate-model` → `model` body: drivers (value, basis, range) beside a tornado of the result at each driver's low and high, widest swing first. Ranges live on the data points (`range: {low, high, basis}`) and the renderer recomputes the result through `calc`; the Calculations sheet lists Low, High and why. check.py fails a driver outside the result's calc, a value outside its range, or fewer than two ranged drivers; it warns, in decks with an appendix, when an estimate on 3+ inputs has no model slide (FreshCart has no appendix, so it is not flagged). Cobalt Ledger deep gains b8 (payback) and b9 (AI cost share); L4's build cost now reads loaded cost per engineer-year, so its calc matches the cards. All example decks 0 fail; both slides rendered and checked in PowerPoint.

**T2 done (2026-11-27).** check.py warns when the storyline has more than one `equation` slide (holdout E1: c10 and c7 each have two). Cobalt Ledger deep had two (L4 payback, 4b1 AI cost); 4b1 could not move to the appendix because it is the evidence slide of issue-tree leaf n4b (T-03), so it became a bar chart (uplift vs AI cost) with the build as a `basis` strip. Units of the AI cost numbers changed from "$ per year" to "$" (the unit line says per year) so the strip cards fit. 0 fail; rendered and checked.

**T1 follow-up (open, 2026-11-27).** The author reviewed T1 and finds it needs more work; what exactly is still to be decided.

**T4 dropped (2026-11-27).** The `estimate-model` slide already shows unit, basis and range for each driver, so the equation cards stay as they are.

Open questions: whether T3 replaces `calculation-bridge` in the appendix entirely, or only for estimates with 3 or more drivers; whether T1 should be a fail or a strong warn while T3 does not exist yet.

## Round 4 · 2026-11-27 · font too small (author's blind holdout review, 2026-11-23) · in progress

Comments: "the font is too small, so the content does not come across at a glance" (holdout P1, P2, P4, P5; P2 is the skill-rendered c8 H2a deck, the others are B decks), "limited formats make the content look monotonous" (P1, c7 E1).

**Measured.** Skill decks already use larger type than B decks (median 12–14 pt vs 10–11 pt; B decks put 60–87% of their text below 12 pt, skill decks 23–43%). Text below 10 pt is footnotes and source lines. In c8 H2a the small body text comes from the renderer shrinking crowded text to fit, without a warning: tables to 11.5 pt, sidebar bullets to 10.5–11.5 pt, basis-strip captions to 9 pt.

**Fix 1 (done).** `fit_size` and the table sizer now warn when body text only fits below 12 pt, or captions and labels below 10 pt, with about how much to cut. The size still shrinks so nothing overflows; SKILL.md Step 5 lists the warning with the others to fix, and compile mode resolves it by tightening, splitting or moving detail to a backup, never by dropping a unit. Small equation cards got less padding. On the reviewed decks: 15 warnings in c8 H2a, 4 in c7 E1. Example decks trimmed to 0 warnings (FreshCart 4 lost one sidebar bullet; other cuts are wording only).

**Open.** Format monotony (c7 E1: chart + sidebar + basis strip on most slides) needs a design pass first.

**Fix 2 (done, monotony).** Compared with the B decks the review called varied, skill decks use as many slide types but put almost every explanation in the same grey box. Mock-ups in Figma (file xve9JsL0BllnkfBzqztLYV, page "09 Variety (2026-11-27)", real RouteSprout content): 0 now, A split exhibits, B open column, C status chips, D notes on the chart. The author chose B + C first. B: `sidebar.style` `box | open`; unset sidebars alternate in deck order (open = no panel, heavy rule on top). C: table cells take `status: pass | watch | fail` (+ `status_label`) and draw a green / amber / red chip before a short reason, from the existing good / caution / alert tokens. Example: showcase slide 4 verdict column. All example decks 0 fail, 0 render warnings; showcase and FreshCart checked in PowerPoint. Next candidates: A (split exhibits, planned as v3-3) and D (chart annotations).

## Round 5 · 2026-11-27 · slide composition (author's tip) · step 1 done

Tip: slides split horizontally in 3 or 2, or vertically in 2; the left or top part sets what goes right or below; a conclusion about the whole part is a box or bullets, one about a specific area uses its own devices. Checked against the 3,257 tagged public-deck pages (`docs/research/composition.md`): split pages are over half the body; 66:33 is exhibit + whole-exhibit takeaway (35% sidebar or box, 11% bullets); 50:50 and 3-column are several exhibits for one claim; specific-area marks (brackets and outlines 18–25%, one accented element 10–16%, callouts 4–9%) appear in every split. The tags have no vertical-split value, so the vertical case is unconfirmed.

**Step 1 (done).** `panels` now takes table and text bodies and `widths` (e.g. `[2, 1]`), so a chart can sit beside the table behind it. Table row labels no longer break inside a word: the label column grows to the longest label word (up to 45%), with a warning beyond. Example: showcase-2 slide 1b (chart + table, 2:1). Next: specific-area marks linked to sidebar text; vertical two-exhibit split after a sample check.

**Step 2 (done).** Specific-area emphasis on single-series bar and column charts: `outline` (dashed box around adjacent bars, optional number and label) and `marks` (numbered dots), matched to numbered sidebar bullets (`sidebar.markers`). The plot area is pinned (manual layout) so bar positions are computed, not guessed; checked in PowerPoint on bars (FreshCart 4) and columns inside panels. Example: FreshCart 4 (Snacks and Frozen outlined as 1, Dairy marked 2).

**Step 3 (mock only).** New type candidate counted from the tags: a table with a small bar in each cell ("bar-table"), 51 pages in 43 decks (33 since 2020); Gantt (87) is already `timeline`; stacked area (24) and dumbbell/range dots (21) next. Mock: Figma page "09 Variety", frame E. Build after the author reviews it.

**Step 3 (built).** `bar-table` → `bartable`: rows aligned across measures, a bar per cell, one scale per column (benchmark row grey and out of the scale), one number of decimals per column, the named row tinted. check.py: one cell per column, bar cells need a point; density rules no longer read its columns as bullet boxes. Example: showcase-5 slide 4b. Built from the Figma mock (frame E) before the author's review; adjust after it.

**Mock D (built).** `marks[].note`: a few words drawn beside the numbered dot, so a chart without a sidebar explains itself; horizontal bars keep a notes column on the right so the longest bar still has room, and a note with no room warns. Checked in PowerPoint on FreshCart 4 without its sidebar.

**Second new type (built): `dumbbell`.** Next most frequent form in the tags after bar-table and stacked area: 21 pages in 20 decks (11 since 2020). Two dots per row on one axis, sorted by the gap; the change column shows its own derived data point (D5), and check.py warns when that point is not derived from the row's two values. Mock: Figma frame F. Example: showcase-5 slide 6b.

**Chart type (built): `stacked_area`.** 24 pages in 19 decks: a mix over many periods. Native stacked area, axis pinned to the first and last points, each layer named at its right end with its last value (no legend, no computed total, per D5); a layer too thin for its label warns. Checked in PowerPoint on a test copy of showcase-2.
