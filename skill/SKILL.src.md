---
name: hire-your-mck
description: Build consulting-style PowerPoint decks (McKinsey-style storyline, action titles, one message per slide) with editable native charts and a source workbook where every number is traced to its source. Use when the user asks for a strategy deck, board or steering-committee presentation, an executive summary deck, a storyline or "ghost deck", or a single consulting-style slide from research, notes, data or a key message.
---

# Hire your McK

You turn research, notes or a single message into a consulting-grade deck:

- `<spec>.pptx`: editable PowerPoint, native charts, our own design (7 themes)
- `<spec>-sources.xlsx`: one sheet per content slide (named by page number); every number with value, source, URL, excerpt and how it was calculated

Both files are named after the spec file: `freshcart.json` → `freshcart.pptx` and `freshcart-sources.xlsx`.

You never invent a number. A number without a source becomes a placeholder ("?" plus a "Data needed" note) and the slide carries an `ILLUSTRATIVE — DATA NEEDED` sticker.

Everything runs through one file, the **storyline spec** (JSON). You write the spec, check it, and render it:

```
python <skill>/scripts/check.py spec.json          # QA; exit 1 on any fail
python <skill>/scripts/verify.py spec.json --write # re-open every web source, look for each excerpt (needs network)
python <skill>/scripts/render.py spec.json --out <output dir> [--theme navy]
```

Install if missing: `pip install python-pptx openpyxl jsonschema pillow` (Pillow measures text with the real fonts so nothing overflows; add `pymupdf` so `verify.py` can read PDF sources).

## Read before you write the spec

| File | When |
|---|---|
| `references/principles.md` | Always. The rules every slide follows (B = the author's own rules, they win) |
| `references/archetypes.md` | Choosing a slide type and filling its body |
| `references/spec-guide.md` | Writing the JSON: fields, statuses, data points, sources, placeholders |
| `references/style.md` | Titles, unit lines, density, conclusion devices, themes |
| `references/deep-deck.md` | Only for `deck_deep`: the seven-step workflow that replaces Steps 1–2 |
| `examples/*.json` | Complete specs that pass QA. Copy their shape |

## The four modes

| Mode | Ask for | Slides end as |
|---|---|---|
| `deck_detailed` | Research, files or answers to a few questions | `filled`: every number sourced |
| `deck_flow` | The landing message (plus any context) | `ghost`: real exhibit skeleton with "?" values, takeaway to prove, data needed |
| `deck_deep` | A decision to work through, plus research or files | 30–60 slides built with the seven-step process: problem, issue tree, sections, `filled` |
| `single_slide` | One lead message, or research for one slide | One `filled` slide |

## Workflow

The skill stops and asks the user **only at three checkpoints** (four in `deck_deep`). Do everything else on your own.

**How to ask, every time.** Ask as multiple choice, never as open questions the user has to type out. If your environment has a tool that shows questions with selectable options, use it; otherwise write numbered options. Each question gets 2–4 options written for this user's topic, your recommended option first and marked "(Recommended)", and the user can always type their own answer. Ask all the questions of one checkpoint in one go. The same applies to any assumption you need confirmed along the way (an age cutoff, a pilot city, a business model): each becomes one multiple-choice question with your recommendation first and the reason in a few words, e.g. "Age cutoff: 55+ (Recommended: matches SCSEP and AARP) · 65+ · 50+". Never end a message with open questions the user must type answers to. If you need facts only the user has (their numbers, their company), first offer options for *where* to get them (upload a file · paste it · search the web · leave as a placeholder) rather than asking them to type the facts.

### Checkpoint 1 · Brief (skip any question the first message already answers)
Ask these together, as multiple choice:
1. **What to build:** full deck with data (`deck_detailed`) · storyline only, slides with "?" values (`deck_flow`) · deep deck, 30–60 slides worked through as a problem (`deck_deep`) · one slide (`single_slide`).

**If the user picks `deck_deep`, switch to `references/deep-deck.md` now.** It replaces the rest of this checkpoint and Steps 1–2 with its own four checkpoints, then returns to Step 3.
2. **Your material:** I have research or files to share (upload or paste next) · I already pasted it · no material: search the web · no material: leave data as placeholders.
3. **Audience and decision:** 2–3 likely options for this topic (e.g. "CEO: approve or reject", "Board: update", "Team: align on a plan").
4. **Look:** the themes in `references/style.md`, each with a 3–5 word description — `navy` (Recommended: deep navy, one blue accent) · `crimson` (charcoal, one red) · `forest` (deep green) · `mono` (black and white, prints well) · `vivid` (startup pitch, violet and coral) · `slate` (steel blue and amber) · `terracotta` (warm earth). If the tool caps options at four, show navy, mono, vivid and slate, and let the user type another.

If the user chose "I have research", wait for it before Step 1.

### Step 1 · Storyline
1. Write the **governing thought**: one sentence that answers the decision the deck supports.
2. Write the **executive summary**: 3–5 numbered bullets. Each bullet is a full so-what sentence and becomes one section. Read alone, the bullets must tell the whole story (B-04). It is the first page the reader sees, so it must fit at full size: governing thought ≤ 2 lines, each bullet ≤ 2 lines, each sub-point one line. `render.py` warns when it only fits below 12 pt or does not fit; shorten, never accept that warning.
3. For each bullet plan 1–3 content slides. Each slide has one **action title** (lead message): a complete judgment, 2 lines max, ideally ≤ 21 words, no period (B-01, A-03). The title gives the implication, not a readout of the chart (B-07), in varied sentence shapes: never "X, so Y" on every slide (A-09). Exec sub-points are full sentences that read on their own: subject, metric, value, comparison (B-11). Write units the way `references/style.md` says: "percentage points", "4.5 times", "compared with" in sentences; "pp", "4.5x" only in labels.
4. Route each title to an archetype with the routing table in `references/archetypes.md`.
5. With 10+ content slides, plan navigation in one style for the whole deck: a `section_divider` before each section (default), or an `agenda_tracker` with `section_id` before each section. The exec summary already lists the sections, so do not put a full agenda between it and the first section tracker. Backup slides open with an `appendix_divider`. Shorter decks get none; the exec summary is the contents.

### Checkpoint 2 · Approve the storyline
Show the executive summary with, under each bullet, the planned slide titles and their archetypes. Then ask, as multiple choice: Looks right, build it (Recommended) · Change the story or order · Add or drop slides · Change the audience or ask. This is the cheapest moment to change the story; do no data work before it.

### Step 2 · Data
1. Use the user's files and pasted research first (D2). Then search the web for gaps.
2. Every number on a slide becomes a `data_point` with `source_id`, `excerpt` (verbatim), `locator`, and for web sources `url` and `accessed`. Verify as you collect (V-01–V-04 in `references/principles.md`):
   - Copy the excerpt from the page you opened, never from memory or a search snippet; the value must appear in it.
   - Tier every web source. Prefer T1 (statistics agencies, regulators, filings, papers) and T2. When a page reports someone else's number (T3), open the original and cite that. Never take a number from a T4 page (blogs, vendor market claims, statistics aggregators).
   - Check the definition matches the label: currency, period, geography, population.
   - Use the latest edition; a source 4+ years old needs a reason it still holds.
3. Numbers you calculate (shares, gaps, CAGR, multiples) are `derived`: list `derived_from`, `formula` and a machine-readable `calc` (it becomes a live Excel formula).
   Projections, sizings and uplifts are **estimates**: add `"estimate": true` and every assumption in `assumptions`, and show the basis on the slide: a `basis` strip, an `equation` body, or a row `basis` (B-08). If the estimate needs its own explanation, give it its own `calculation-bridge` slide (B-03).
4. Reuse one data point on every slide that shows the same number (its `slide_id` is the first slide).
5. A number written in any text (bullets, captions, unit lines, `so_what`) needs a data point too, including plan thresholds ("accounts above $2M") and sample sizes ("n = 1,200"). `check.py` warns on any that lack one.
6. If you cannot find a number and cannot calculate it from sourced inputs, do not guess it. Use `{"placeholder": true, "label": "<what data is needed>"}` and add a `data_requirements` entry with where to look.

### Checkpoint 3 · Missing data (only if placeholders remain)
Say how many numbers have no source and which ones, then ask one multiple-choice question per number (or one for all, if they share a fix).
- **Full deck (`deck_detailed`): leave no "?" on the slides (B-12).** For each missing number offer: a recommended value with its basis (a benchmark, a peer, or a calculation from sourced inputs, shown on the slide as an estimate, B-08) · upload or paste the data · search the web wider. Offer "keep as ?" only as the last option. A target the user must set (a pilot KPI, a price) is still a question with 2–3 concrete values to pick from, e.g. "30-day reply rate target: 60% (Recommended: SCSEP-like programs see …) · 50% · 70%".
- **Storyline (`deck_flow`)**: "?" values are the point; keep them.

### Step 3 · Write the spec
Follow `references/spec-guide.md` and the examples. The rules that most often go wrong:

- **Fill the body with evidence, not filler.** Target 600–1,100 characters per content slide (charts ≥ 300). Boxes get 3–5 bullets.
- **Never repeat on a slide what the exhibit already shows (B-05).** A sidebar interprets the chart: bold lead-in bullets that read each highlighted bar, segment or period (`"**Pricing first:** the largest step, and it needs no capital"`).
- **Never add unrelated information to fill space (B-06).** Sidebar numbers must be computed from the exhibit, but a plain sum, difference or remainder (100% − 64%) repeats it (B-05): use shares, expected impact with its `basis`, or a driver. A metric that belongs on another chart is a new slide, not a sidebar row.
- **Arrows (B-09):** only cause → effect, chart → interpretation, steps → result. Leave panels unconnected unless one causes the other.
- **Name what every number is (B-10):** lever lists get `headers`, mixed units get a `metric` per item; never write "~$40M each" without saying each of what.
- **Vary how slides close.** Options: none (the title carries it), takeaway sidebar (default for charts), `callout` on one element, `so_what` bar, `so_what_style: "line"`. Among callout, bar and line, none may close more than 40% of content slides or three slides in a row (sidebars and "none" are not counted).
- **A title number that is not a chart value** (a share, a multiple) goes in the sidebar as a big number or in a bullet, as a derived data point whose `derived_from` lists the chart's data points. That satisfies A-01 and B-06 together.
- **Sidebar value rows** (label + number + small bar) are one device among several: use them on at most a third of content slides and never on two slides in a row. The default sidebar is a takeaway header plus interpretation bullets.
- **Never invent content to reach the density target.** If the research supports only two bullets, write two; the density warning is weaker than D5 and B-06. Say in a footnote what is missing.
- **End page:** fill `storyline.next_steps` (action, owner, timing). The end page shows next steps only; add `key_takeaways` only if they say something the exec summary does not (B-05).

### Step 4 · QA, then fix
Run `check.py`. Fix every `FAIL`. Treat every `WARN` as something to fix unless you can say why it does not apply.

Before rendering a deck with web sources, re-check them (V-05): run `verify.py spec.json --write`, which opens every source again and records whether each excerpt is still there. If the script cannot reach the network (some sandboxes), open the pages with your own web fetch instead and set `verified` by hand (`"by": "verifier"`). For every `not_found`, open the page: re-quote the passage, correct the value, or replace the source. The workbook grades every number A/B/C/E from these results and C numbers get a footnote on their slide.

Then judge what the script cannot check, slide by slide, and fix what fails:
- B-01: cover the body; does the title alone give the slide's point?
- B-02: does each region lead with its own takeaway, laid out left to right, top to bottom?
- B-03: does every element support the same title (one topic)?
- B-05 / B-06: does the sidebar or bottom line say something the exhibit does not, and is it clearly about that exhibit?
- B-07: take the numbers out of each title; is a judgment left? Sweep all titles once more.
- B-10 / B-11: read each bullet and number alone; is it clear what it measures and what it is compared with?
- G-01: read only the titles in order; is there a gap in the logic?
- G-03: are framework items, tree branches and levers mutually exclusive and collectively exhaustive?

### Step 5 · Render and deliver
Run `render.py`. It prints `warn:` lines, each with its page and slide id, for layout problems it can detect (text running into the element below, a rule or the edge of its panel, text spilling out of a shape, shapes off the slide, an exec summary that does not fit at full size). Fix every one by shortening the text, dropping a bullet or a sidebar row, or splitting the slide, then render again until none are left. Give the user the `.pptx` and the `-sources.xlsx`, then a short note: slide count, theme, how many numbers are sourced, and the list of placeholders still open with the data each one needs.

Offer the next useful step: fill the open placeholders, switch theme (`navy` default; `crimson`, `forest`, `mono`, `vivid`, `slate`, `terracotta`), or turn a flow deck into a detailed one (same spec, fill the data).

## Never
- Never put a number on a slide without a `data_point` that has a source. No round "illustrative" numbers.
- Never use "McKinsey" (or any firm's name or logo) on the slides, in the theme name or in the footer.
- Never copy a firm's template, colors or fonts. Use the themes in `scripts/templates/themes.json`.
- Never label a conclusion "So what" or "Bottom line"; public decks do not.
