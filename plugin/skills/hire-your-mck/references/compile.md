# Compile a finished analysis into a deck

Use this file when the user hands you an analysis that is already done (a memo, a draft deck, a deck made with
another tool) and wants it as a deck in our format. It replaces Steps 1, 2 and 2b of `SKILL.md`; Steps 3–5 (write
the spec, QA, render) still apply.

**The analysis is the source of truth.** Your job is to carry every decision-relevant piece of it onto slides
without changing what it means. Do not redo the analysis, extend it, or run a decision audit on it. Better design,
clearer titles and editable charts are the value you add; a different argument is not.

## Variant

Set `compile.variant` from the request (ask only if it is unclear; recommend `restructure`):

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
estimate, flagged unverified"). Ask about it at Checkpoint 3 as a multiple-choice question.

**Corrections.** If a number or claim in the source contradicts the evidence or its own arithmetic, do not fix it
silently. Use the corrected value and record it in `compile.corrections` (`unit_id`, `was`, `now`, `why`). A
correction is the only kind of change to the analysis you may make, and every one is logged.

## Step C3 · Map units to slides

- Use an archetype only when every unit on the source slide fits it. Otherwise use the general exhibits:
  `data-table`, `comparison-table`, `line-trend` (several scenarios as series), `multi-chart-panel`,
  `text-columns`. A sensitivity grid or a multi-scenario cash chart stays a grid or a multi-series chart; never
  turn it into a single-number KPI tile or a one-line calculation.
- Density (A-12) is a guide here, not a target. Never drop a unit to fit it: split the slide at a logical break or
  turn prose into a table or chart. Never add filler to reach it (B-06).
- Navigation: no agenda trackers or section dividers unless the source has sections and the deck runs past 15
  content slides; never repeat a contents page.
- Titles follow our style (B-07, A-03) but keep every qualifier: conditions, ranges, hedges, comparisons and the
  ranking of options. If a title cannot be shortened without losing one, keep the qualifier and accept the longer
  title.
- Untraceable non-critical numbers may stay on slides as estimates with a "source not verified" footnote; B-12 does
  not apply to them.

## Step C4 · Fidelity check (before rendering)

Read the deck against `compile.units`, unit by unit: is each critical unit there, with the same numbers,
conditions, confidence and ranking of options? Record the result in `compile.check`
(`critical_units`, `preserved`, `notes`). Fix any loss before rendering. Then continue with Steps 3–5 of
`SKILL.md`; skip Step 2b.

In the delivery note, list the corrections and the untraceable numbers.
