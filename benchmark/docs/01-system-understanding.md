# 1 · What Hire Your McK is, and which parts could change reasoning

Written before any benchmark code, from the repository at commit `e1e6b31` (plugin version 1.2.0).
Its purpose: decide which parts of the product a reasoning benchmark measures, and which it must not
count as reasoning.

## 1.1 What the product is

Hire Your McK is a Claude Skill (`plugin/skills/hire-your-mck/`, built from `skill/`, `renderer/`,
`tools/spec/`, `templates/` by `tools/build_skill.py`). It does not call a model of its own. Claude reads
`SKILL.md` and its references, writes one JSON **storyline spec**, runs `check.py` on it, and runs
`render.py` to produce `<name>.pptx` plus `<name>-sources.xlsx`.

The README pitch is that it produces "a storyline that holds together", not just layouts
("Pretty slides are easy. The logic is the hard part."). It claims three things: a coherent
storyline, a source for every number, and native PowerPoint output. This benchmark tests the first two.
It measures the third only as a separate end-to-end check.

There are four modes: `deck_detailed`, `deck_deep` (30–60 slides, seven-step problem solving), `deck_flow`
(ghost deck) and `single_slide`. The skill recommends a mode from the brief. A decision "with several
open questions behind it (enter a market, launch, invest…) … for a CEO, board or steering committee"
gets `deck_deep`. All five benchmark cases fit that description, so in an unattended run the skill is
expected to choose `deck_deep`. The pilot showed what it actually picked (see `../METHODOLOGY.md` §6).

## 1.2 Components, classified

| Component | File(s) | What it does | Class |
|---|---|---|---|
| Storyline workflow | `SKILL.md` Step 1, Checkpoint 2 | Governing thought → 3–5 exec-summary bullets that become sections → action title per slide; storyline approved before data work | **Reasoning (structure)** |
| Deep-deck workflow | `references/deep-deck.md` | Problem definition worksheet (decision maker, success criteria, deadline, out of scope); 2–3 alternative issue trees, MECE level 1; every node a testable hypothesis; importance × influence pruning; workplan with knock-out analyses first; per-leaf verdict confirmed / revised / refuted; rewrite refuted titles and governing thought from verdicts; close the loop against success criteria | **Reasoning (hypothesis-driven, revision)** |
| B rules judged by the model | `principles.md` B-01, B-02, B-03, B-07, B-11; G-01–G-03 | Title alone carries the point; implication, not readout; one topic per slide; horizontal/vertical logic; MECE | **Reasoning (storyline coherence)**, self-assessed by the same model |
| B/A rules checked by script | `check.py` (≈1,000 lines): B-04, B-05, B-06, B-08, B-10, A-01–A-13 | Every exec item has slides; sidebar does not repeat the chart; title numbers appear on the slide; count words match; estimates have `calc` + assumptions that recompute; title length; connector variety | **Structural compliance.** A few (B-04 coverage, B-08 recompute) touch reasoning hygiene |
| Deep-deck structure checks | `check.py` P-01, T-01–T-04, L-01–L-04 | Worksheet fields non-empty; 3–5 branches mapped to sections; every kept leaf has a slide and a verdict; a refuted leaf's title is no longer its hypothesis | **Structural compliance with reasoning intent.** T-04 checks that a verdict was *recorded and propagated*, not that it is *correct* |
| Evidence discipline | `SKILL.md` Step 2; `spec-guide.md`; schema | A number reaches a slide only as a `data_point` with `source_id` + verbatim `excerpt` + `locator`; derived numbers carry `derived_from`, `formula`, machine-checkable `calc`; estimates carry `estimate: true` + `assumptions`; missing numbers become placeholders | **Factual traceability** (bookkeeping that should reduce unsupported numbers) |
| Source verification | `verify.py`, `grade.py`, V-01–V-06 | Re-opens web pages to find each excerpt; corroboration by a second source; A/B/C/E grades in the workbook | **Factual verification.** Web only: it does nothing for user-provided files. Out of scope offline (see below) |
| Archetype routing, style | `archetypes.md`, `style.md` | Message type → slide type; unit wording; density 600–1,100 chars; conclusion-device variety | **Formatting / presentation** (routing is weakly reasoning-related: "the message picks the chart") |
| Renderer | `renderer/pptx_render.py` (3,700 lines), `measure.py`, `xlsx_render.py`, themes | Native charts, text fitting, source workbook | **Formatting / rendering only** |
| Examples | `examples/*.json` (Cobalt Ledger etc.) | Few-shot shape for the spec | Format template; may also anchor content style |
| Checkpoints | `SKILL.md`, `deep-deck.md` | 3–4 stops for multiple-choice approval | **Human-in-the-loop.** In an unattended benchmark nobody answers them (see 1.4) |

## 1.3 What the benchmark should and should not credit

- **Credit as reasoning:** whether the governing thought answers the decision; whether the exec summary
  and titles form a hierarchy the evidence supports; whether alternatives and trade-offs are weighed;
  whether numbers are right and claims supported; whether an initial hypothesis is revised when the data
  contradicts it.
- **Do not credit as reasoning:** passing `check.py`, title word counts, unit wording, archetype variety,
  slide count, density, a recorded `finding.verdict`, a source workbook, grades. These are shown separately
  as end-to-end/product metrics.
- **Self-assessment is not evidence.** The LLM-judged rules (B-01, B-07, G-01…) are judged by the same
  model that wrote the deck. The benchmark uses independent judges with an answer key instead.

## 1.4 Mechanisms that could plausibly *improve* reasoning, and ones that could *hurt* it

The list below is a hypothesis, written before seeing any results:

| Could help | Could hurt |
|---|---|
| Explicit hypotheses with knock-out tests, and refuted/revised verdicts (H4) | Long decks (30–60 slides) dilute the argument and penalise concision |
| Problem worksheet: success criteria and constraints are written down and checked at the end (H2) | Heavy formatting instructions (≈50 rules, a 3,200-line schema) consume attention that could go to analysis |
| "No number without a data point" and `calc` recomputation (H3: fewer numerical errors) | Density targets ("600–1,100 characters per slide") can pull in marginal content |
| Pyramid: exec summary items = sections, titles prove items (H1) | Issue-tree commitment early can anchor the story before analysis (the workflow fixes the storyline before data work) |
| Alternatives as competing trees; "what we did not pursue" appendix (H2) | Verdict bookkeeping may become box-ticking (a verdict recorded, but the reasoning behind it is thin) |

Condition B (a strong prompt with the same generic principles: pyramid, MECE, hypotheses, action titles)
separates the effect of the *ideas* from the effect of the *skill's workflow and tooling*.

## 1.5 Constraints of an offline, unattended benchmark

1. **No web research.** The skill's source-verification layer (`verify.py`, V-03 tiers, V-05, V-06
   corroboration) exists for web sources only. With a self-contained evidence packet, all numbers are
   "user provided" and those layers are idle. H3 therefore measures whether numbers are *correctly used
   and derived* from the packet, not whether they are *verified on the web*.
2. **No user at the checkpoints.** The skill is designed to stop 3–4 times for a human. In this benchmark
   a fixed scripted reply ("choose the option you recommend and continue") stands in for the human, for
   all three conditions. This removes the value a real partner adds at the checkpoints. It is a
   limitation of the test, not a property of the skill.
3. **Same tools for everyone.** All conditions get Bash, Read, Write, Edit, Skill and Agent with the same
   Python environment (the skill's own requirements). Only condition C has the skill installed.
4. **Rendering is not reasoning.** The primary comparison uses text extracted from the delivered deck and
   normalised into one storyline format, so visual design cannot influence the reasoning scores.
