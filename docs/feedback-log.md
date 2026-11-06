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
