# Compile a finished analysis into a deck

Use this file when the user hands you an analysis that is already done (a memo, a draft deck, a deck made with
another tool) and wants it as a deck in our format. It replaces Steps 1, 2 and 2b of `SKILL.md`; Steps 3–5 (write
the spec, QA, render) still apply.

**The analysis is the source of truth.** Your job is to carry every decision-relevant piece of it onto slides
without changing what it means. Do not redo the analysis, extend it, or run a decision audit on it. Better design,
clearer titles and editable charts are the value you add; a different argument is not.

## Variant

Set `compile.variant` from the request (ask only if it is unclear; recommend `restyle`, which keeps the source's
meaning more reliably and its length close to the source):

- **`restyle`**: keep the source's slide order and its one-slide-one-point structure. Change layout, chart form,
  styling and wording style. Split a source slide only when it cannot be read at the theme's sizes; never merge two.
- **`restructure`**: keep the content and the conclusion; you may reorder, split and merge slides, and choose new
  exhibits, so that the argument is easier to follow.

## Step C1 · Inventory the decision units (before any slide)

Read the whole source and list in `compile.units` everything a decision maker relies on:

- the answer and each recommendation, with its conditions ("only if", "before the price change", "in the base case");
- each claim that supports them, with the numbers that carry it;
- assumptions and their basis; ranges, base and stress cases;
- the alternatives and why each loses (or how they combine);
- thresholds, decision gates, risks and their triggers;
- the decisions asked of the reader and the next steps.

Each unit gets an `id`, a `type`, its `text` (close to the source's words), `source_loc` (slide or section), and
`critical: true` when the decision, a headline, an executive-summary item or a gate depends on it. After mapping,
each unit lists the `slide_ids` that carry it. Critical units go in the main deck, never only in the appendix.

## Step C2 · Check every number against the evidence

If the user also gave the evidence the analysis was built from, find each number in it or recompute it, and
write data points as usual (Step 2 of `SKILL.md`, rules V-01–V-04):

| The number is | Data point |
|---|---|
| in the evidence | sourced: excerpt from the evidence |
| reproducible from sourced inputs | `derived` with `derived_from`, `formula`, `calc` |
| an assumption the analysis states | `estimate: true` with `assumptions` and a `basis` on the slide |
| not found and not reproducible | sourced from the analysis itself (a `user_provided` source whose `input_id` is the analysis), and listed in `compile.untraceable` |

Never invent a formula to make an untraceable number look checked. In `compile.untraceable`, mark `critical: true`
when the number is in a title, the executive summary, a gate or a recommendation's headline: `check.py` fails a
critical untraceable number until it is acknowledged (`ack`: what the user decided, e.g. "keep as the analysis's
estimate, flagged unverified"). Ask about it at Checkpoint 3 as a multiple-choice question. Acknowledged is not
verified: the number stays marked as the analysis's unverified estimate on its slide and in the delivery note.

**Corrections.** If a number or claim in the source contradicts the evidence or its own arithmetic, do not fix it
silently. A correction is the only kind of change to the analysis you may make, and every one is logged and checked:

1. **Verify before you correct.** Confirm the error from evidence, not from appearance: the same metric, the same
   definition, the same base and the same period. Two numbers that measure different things are not a
   contradiction ("most important risk" is a strategic judgement; "largest swing in the sensitivity table" is a
   number, and the two can differ). If you cannot show the error, it is not one: keep the source's wording, and if a
   reader could misread it, add a footnote saying what each exhibit measures.
2. **Log it** in `compile.corrections` with `unit_id`, `source_loc` (where the source says it), `was`, `now`, `why`,
   `evidence` (the excerpt, the source's own exhibit, or the recomputation that shows the error) and `affects` (the
   id of every slide that carries the unit or depends on it, including `es` for the executive summary).
3. **Re-check every slide in `affects`** after the change: the executive summary, titles and body must say the
   same thing. A correction that leaves the summary and a body slide disagreeing is a new error.

## Step C3 · Map units to slides

- Use an archetype only when every unit on the source slide fits it. Otherwise use the general exhibits:
  `data-table`, `comparison-table`, `line-trend` (several scenarios as series), `multi-chart-panel`,
  `text-columns`. A sensitivity grid or a multi-scenario cash chart stays a grid or a multi-series chart; never
  turn it into a single-number KPI tile or a one-line calculation.
- Density (A-12) is a guide here, not a target. Never drop a unit to fit it: split the slide at a logical break or
  turn prose into a table or chart. The same holds for `render.py`'s shrink warning (body text below 12 pt): tighten
  the wording, split the slide, or move detail to a backup, but keep every unit. Never add filler to reach it (B-06).
- Navigation: no agenda trackers or section dividers unless the source has sections and the deck runs past 15
  content slides; never repeat a contents page.
- Titles follow our style (B-07, A-03) but keep every qualifier: conditions, ranges, hedges, comparisons and the
  ranking of options. If a title cannot be shortened without losing one, keep the qualifier and accept the longer
  title.
- Untraceable non-critical numbers may stay on slides as estimates with a "source not verified" footnote; B-12 does
  not apply to them.

## Rules that keep the meaning

- **Keep the source's numbers as written.** Show the value the source shows ($12.4M stays $12.4M even if your own
  sum of rounded parts gives $12.3M); put the unrounded value in the workbook, not a new rounding on the slide. A
  number changes only through a logged correction.
- **Never re-rank or re-weigh.** If the source says which option, risk or sensitivity matters most, the deck says the
  same, in the same order. If the source's own table seems to disagree with its ranking, first check whether they
  rank the same thing (step 1 of Corrections). Only a verified contradiction is corrected, and then on every slide in
  `affects`; otherwise keep the source's ranking.
- **Test the source against itself.** Before mapping, read each headline claim against the source's own exhibits
  ("the biggest driver" against its bridge, "no upfront cost" against its cost table). A claim its own exhibit
  contradicts is a correction: verify it, log it and state the supported version.
- **Keep every recommendation-level claim.** Upside and positioning claims ("positions us for the next product cycle")
  are units too; rewording them into something narrower drops them.

## Step C4 · Fidelity check (before rendering)

Read the deck against `compile.units`, unit by unit: is each critical unit there, with the same numbers,
conditions, confidence and ranking of options? Then read every correction's `affects` slides together. Record the
result in `compile.check`
(`critical_units`, `preserved`, `notes`). Fix any loss before rendering. Then continue with Steps 3–5 of
`SKILL.md`; skip Step 2b.

In the delivery note, list the corrections and the untraceable numbers.
