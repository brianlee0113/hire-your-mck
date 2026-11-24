# Where the compile step's time goes (H2a holdout, 2026-11-23)

**Question.** H2a costs about 3.5× B and takes about 3× its API time. The compile step alone takes
22.6–29.1 min wall and $7.7–9.9 per deck. Where does that time go, and would H2b
(B writes a brief + storyline instead of a deck) reduce it?

**Answer.** Most of the extra time is not analysis. The compile step spends it fitting all of B's content onto
slides (render/check loops and self-written measuring scripts) and learning the spec format from the renderer's
source code. H2b changes B's output, not these steps, so it would save little. The skill-side fixes below come first.

## Method
- Transcripts of the six holdout H2a runs (`runs/holdout/holdout-c*-H2a-r1/transcript-attempt1.jsonl.gz`), and the
  six E1 runs for comparison. Main agent only (subagent turns excluded).
- Each model response (stream chunks merged by message id) is classified by its first tool call. Its time is
  generation time (from the previous tool result to the end of the response) plus the run time of the tools it called.
  "Input tok share" sums each response's input context (cache read + write + fresh).
- Script: `scripts/analyse_compile_time.py [H2a|E1]`. Heuristic classes; a response that patches the spec and
  re-renders in one command counts as render/check.

## Results (six runs each)

| Activity | H2a min (share) | H2a calls | H2a input share | E1 min | Difference |
|---|---|---|---|---|---|
| Render/check and fix loop | 48.4 (33%) | 145 | 43% | 24.4 | **+24** |
| Learning skill/renderer code (schema, `check.py`, `pptx_render.py` read with `sed`/`grep`) | 30.3 (21%) | 93 | 13% | 12.9 | **+17** |
| Measure/fit scripts written by the model (`titles.py`, `fit.py`, `tablefit.py`) | 14.7 (10%) | 55 | 18% | 0.7 | **+14** |
| Writing the spec | 17.7 (12%) | 5 | 1% | 12.4 | +5 |
| Other: mostly long planning thought before the first file | 17.1 (12%) | 17 | 5% | 4.6 | +12 |
| Patching the spec | 5.5 (4%) | 15 | 5% | 2.6 | +3 |
| Sources workbook | 4.2 (3%) | 10 | 3% | 7.0 | −3 |
| Inspecting the pptx, reading inputs, final answer | 6.6 | 35 | 10% | 3.0 | +4 |
| Review subagent (main agent waiting) | 1.1 | 5 | 2% | 9.5 | −8 |
| **Total** | **145 (24/run)** | **380** | | **77 (13/run)** | |

Per run, H2a (min): learn / write / patch / measure / render-check / sources / subagent

| Run | learn | write | patch | measure | render-check | sources | subagent |
|---|---|---|---|---|---|---|---|
| c6 | 4.5 | 0.0 | 0.0 | 4.3 | 5.7 | 0.2 | 0.3 |
| c7 | 6.9 | 3.9 | 1.3 | 3.6 | 6.8 | 0.1 | 0.0 |
| c8 | 2.0 | 3.8 | 0.7 | 0.8 | 10.3 | 1.0 | 0.2 |
| c9 | 3.7 | 1.2 | 0.9 | 1.7 | 9.4 | 2.4 | 0.2 |
| c10 | 11.1 | 3.7 | 0.9 | 2.2 | 5.7 | 0.2 | 0.2 |
| c11 | 2.1 | 5.1 | 1.7 | 2.1 | 10.4 | 0.2 | 0.2 |

(c6 wrote its spec through a Bash heredoc, which falls under "other".)

Iterations per H2a run: 4–14 renders and 8–14 `check.py` runs. The first check typically reports 1–9 FAILs and
20–40 WARNs; most later renders print no warnings, and the model re-renders after its own fit measurements.

## Reading
1. **Fitting B's content is the biggest cost (render loop + measure scripts + patches: +41 min over six runs vs
   E1).** Restyle must keep every unit of a dense B deck. The renderer warns only after a render, so in four of six
   runs the model wrote its own scripts that import renderer internals to measure titles, tables and bars before
   rendering.
2. **The skill is learned from its source code (+17 min).** The references are not enough to write a compile spec,
   so the model reads the schema JSON, `check.py` rules and hundreds of lines of `pptx_render.py`. c7 spent its
   first 9 minutes and c10 11 minutes this way.
3. **Cost follows the number of calls.** Each call re-reads a long context, so the loops (render 43%, measure 18%)
   dominate input tokens, not the long writing steps (1%).
4. **H2b would not touch these.** All three drivers sit in the compile step; H2b changes only what B hands over.

## Proposed fixes (skill side), with rough savings per run
| Fix | What | Est. saving |
|---|---|---|
| Fit preflight | e.g. `render.py --fit`: before rendering, print for every title, cell, bullet and chart slot the lines used vs available, from the renderer's own measurements; replaces the ad-hoc `titles.py` / `fit.py` / `tablefit.py` | 3–4 min |
| Spec quick reference | one file with every body kind's fields, limits and a minimal example, so the model reads it instead of the renderer and schema source | 2–3 min |
| Quieter `check.py` in compile mode | first check prints 20–40 WARNs; drop or group those that compile is told to ignore (A-12 density is guidance only) | 2–3 min |

If H2a matched E1 on learning, measuring and looping, the compile step would drop from about 24 to about 15 min and
from about $8.5 to about $5.5 per deck: H2a ≈ 2.3× B instead of 3×. This is an upper bound from the E1 comparison,
not a measurement; it needs a rerun on the dev cases (c2, c5) after the fixes, scored with the same fidelity
checker so that speed does not come at the cost of preservation.
