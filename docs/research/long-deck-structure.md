# Long-deck structure: how 40+ page McKinsey decks are built

Collected 2026-11-10. Earlier rounds sampled 12–33 pages per deck and tagged single-slide archetypes.
This round outlined **every page** of 6 long decks (529 pages) to learn the section architecture
a generator needs for 30–60 slide decks. Only abstract structure is recorded here; the decks are not
redistributed (links are in `public-deck-sources.md` and `public-deck-sources-round2.md`).

Method: full-text extraction of every page (PyMuPDF), section boundaries and page roles set by hand,
navigation devices confirmed visually on rendered contact sheets (~60 pages).

| id | Deck (source list ref) | Pages | Type |
|---|---|---|---|
| dc3 | DC Transportation & Warehousing sector analysis (R1 #3, 2020) | 40 | Client diagnostic + opportunity scan |
| mgi29 | MGI affordable housing blueprint (R1 #29, 2015) | 49 | Research report, conference version |
| uk9 | UK electricity efficiency potential (R1 #9, 2012) | 129 | Government policy study |
| cap23 | Analyses to support CAP23 (r2-137, 2023) | 113 | Government analytical compendium |
| china27 | China biopharma: path to value creation (r2-027, 2023) | 70 | Research report / industry outlook |
| nhs115 | NHS productivity 2009/10–13/14 (r2-115) | 124 | Client diagnostic + programme design |

Stop TB (R1 #10) was planned but the host returned 403; nhs115 replaced it.

## Section maps (abridged)

- **dc3**: cover · 1 Baseline (5) · 2 Challenges & trends (14) · 3 Opportunities & best practices (9) · appendix (11, 28%).
  No exec summary. The contents slide returns as the divider 4 times with the current item boxed.
  Each section opens with a coded index matrix; every evidence title starts with its cell code ("2a:").
- **mgi29**: cover · 1 Size of challenge (5) · 2 Blueprint overview (4) · 3–7 one section per lever (2–10 each) · thank-you · backup (14, 29%).
  The framework slide replaces the agenda: its 5 boxes map 1:1 to 5 photo dividers whose subtitle states the section's answer.
- **uk9**: approach + scope + exec summary (4) · 5 sections (5–21 pages) · appendix (68, 53%).
  Project phases = contents items = sections = appendix blocks, all 1:1. Barrier section: 11 findings in 4 numbered themes, each theme opened by an "N – key insights" slide, evidence tagged with theme number + finding letter.
- **cap23**: intro note · one deep-dive (12) · appendix of 8 sectors (99). Every sector repeats one template: tracker → headline chart → assumptions → "N measures" index table (codes T1–T5…) → 1–7 evidence pages per measure → optional risks. Atypical ratios (compendium of earlier work).
- **china27**: cover · "Key questions" (4 numbered questions = agenda) · 4 sections (7, 14, 30, 12) · key takeaways · no appendix.
  Each divider repeats its question word for word. Big sections open with a framework whose lens names become title prefixes ("Patient:", "A."); the framework is re-shown, scored, at the section end.
- **nhs115**: summary (6 bullets) · 1 Size of opportunity (10) · 2 Detailing opportunities (67, in sub-sections 36/19/12) · 3 Implications (8) · 4 Making it happen (17) · backup (19, 15%).
  9 tracker appearances (sections, sub-sections, backup). Summary sub-dashes map 1:1 to sub-sections.

## Grammar rules for a generator

- **R1 Front matter is tiny**: 1–4 pages (≤4%): cover, optional context/approach, one exec summary or key-questions slide, agenda.
- **R2 The opener sets the storyline** in one of three forms: exec summary with one bold bullet per section and sub-points per sub-section (uk9, nhs115); numbered key questions that become the dividers (china27); a framework diagram whose boxes become the dividers (mgi29, dc3). Summary bullets map to sections, never to individual slides.
- **R3 Agenda = divider = appendix structure**: the agenda is reused as every section divider with the current item highlighted (5 of 6 decks). Decks over 100 pages use a two-level tracker (section > sub-section). No deck shows a tracker on every content page; the kicker code does that job.
- **R4 Section = divider → lead slide → coded evidence**: the lead slide states the section's answer and an index (numbered levers, matrix, "N measures" table, framework). Evidence titles start with the index code ("2a:", "T1:", "①", "A.", "Patient:"). 6 of 6 decks; 22–54 coded titles per deck.
- **R5 Length**: content sections median ~10 pages (range 2–30). 1–3 evidence slides per index item, up to 7 for the one that matters most. Split sections over ~20 pages into sub-sections with their own tracker and sub-lead.
- **R6 Section close (optional, ~50%)**: implications / risks / "what you would need to believe", a scored recap of the opening framework, a sensitivity check. Diagnostic sections often just stop and the next lead carries the so-what.
- **R7 Storyline order**: context/baseline → size of prize (answer waterfall) → deep dives by lever or segment → implications → how to make it happen. Recommendations come last (except in the exec summary); case examples cluster in opportunity sections.
- **R8 Methodology**: one short slide at the start of the section that needs it; full detail in backup, in main-section order.
- **R9 Appendix**: 15–29% of a typical client deck, 53%+ in assumption-heavy policy studies, none in talks. Opens with its own divider/tracker and mirrors the main section order: assumptions, "(1/3)" continuations, interview guide, extra cases, alternative cuts.
- **R10 End**: "Key takeaways" (5–7 statements in storyline order) or thank-you in research/talk decks; client decks end on recommendations or backup.
- **R11 Sourcing**: source lines on 55–96% of pages. Unsourced pages are dividers, frameworks, methodology and recommendations; evidence charts are nearly always sourced.
- **R12 Continuations**: "(1/2)" pages instead of squeezing an over-long table or case onto one slide.

## By deck type

- **Client diagnostic / programme design** (nhs115, dc3): summary + contents tracker; heavy sizing (answer waterfall, "potential £x if below-median performers close the gap"); ends with make-it-happen (governance, team, 12-month plan) or opportunity one-pagers; backup 15–28%.
- **Government policy / analytics** (uk9, cap23): phases stated up front; prominent methodology and sensitivities; "Key insights" sidebars; very large appendix; modular per-sector templates; answers framed as "what you would need to believe".
- **Research / talk** (mgi29, china27): questions or a framework as agenda; photo dividers; lens prefixes; debate slides; takeaways at the end.

## How this maps to the 7-step process

See `seven-steps.md`. Level-1 branches of the issue tree (step 2) are the sections (R2–R3); the pruned
leaves (step 3) are the lead slide's index and the evidence codes (R4); the workplan (step 4) is the
ghost deck and the backup approach (R8–R9); synthesis (step 6) is the exec summary (R2).
