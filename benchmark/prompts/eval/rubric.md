# Scoring rubric (frozen before the main benchmark)

Score the **reasoning** of the document, not its look. Do not reward slide count, length, visual polish,
consulting vocabulary, frameworks named but not used, or compliance with any template or style guide. A short
document can score 5; a long one can score 1. Alternative conclusions that meet the answer key's criteria for a
defensible conclusion are as good as the key's preferred one.

Each dimension is scored 1–5. Anchors are given for 1, 3 and 5; use 2 and 4 for documents between anchors.

**Use the whole scale.** A 5 means the document could go to the decision maker as it is: nothing material to fix on
that dimension. A 4 is strong work with at least one material flaw (one unsupported claim that matters, one missed
critical item, one gap in the logic). Competent work with several such flaws is a 3. In particular, evidence and
reasoning cannot score 5 if the document contains a material numerical error, a material unsupported claim, or
misses a critical evidence item; strategic judgment cannot score 5 if it falls into one of the key's traps or
ignores evidence that cuts against its recommendation; clarity and concision cannot score 5 if the document is
substantially longer than the decision needs.

## Dimensions and weights

| Dimension | Weight |
|---|---:|
| Problem framing | 15% |
| Storyline coherence | 25% |
| Evidence and reasoning | 25% |
| Strategic judgment | 25% |
| Clarity and concision | 10% |

Weighted score = 0.15·framing + 0.25·coherence + 0.25·evidence + 0.25·judgment + 0.10·clarity (range 1–5).

### 1 · Problem framing (15%)
Does the document frame the decision the decision maker actually faces?
- **1** — Answers a different or vaguer question; ignores the stated objectives and constraints; no sense of what the decision turns on.
- **3** — States the question and some objectives or constraints, but uses them only partly as decision criteria, or misses an important one (e.g. treats a "which route" decision as yes/no, or ignores a binding constraint).
- **5** — Frames the decision exactly as posed; uses the stated objectives and constraints explicitly as criteria; identifies early the few issues the answer turns on.

### 2 · Storyline coherence (25%)
Do the governing thought, executive summary, slide titles and evidence form one consistent logical hierarchy?
- **1** — No clear overall answer; slides are a sequence of topics or data dumps; the summary (if any) does not match the body; the argument contradicts itself.
- **3** — A clear answer and sensible sections; most titles carry a message; but some slides do not support their parent point, there are gaps or jumps, or redundancy.
- **5** — The governing thought answers the question; the summary points are the sections; every title is a claim that its slide's evidence supports; reading the titles alone gives the argument; no gaps, contradictions or redundancy.

### 3 · Evidence and reasoning (25%)
Are numbers right, calculations done, inferences valid and claims supported by the briefing pack?
- **1** — Key numbers wrong or misread; important claims not supported by the pack; required calculations missing or wrong; evidence cherry-picked.
- **3** — Mostly accurate; some required calculations done; a few unsupported or overstated claims; some critical evidence missed or misread.
- **5** — Numbers correct and derivations transparent; the required calculations are done; critical evidence is used, including evidence that cuts against the answer; claims are calibrated to the evidence; causal claims are justified.

### 4 · Strategic judgment (25%)
Is the recommendation defensible and decision-useful?
- **1** — Recommendation missing or not defensible given the evidence; no real alternatives; trade-offs ignored; falls into the main reasoning traps.
- **3** — Defensible but generic or under-qualified; alternatives named but not genuinely compared; some trade-offs; uncertainty handled only partly.
- **5** — A clear recommendation that follows from the analysis; alternatives compared on the decision criteria; the key trade-offs explicit; says what would change the answer (conditions, gates, kill criteria); actionable next steps; avoids the traps.

### 5 · Clarity and concision (10%)
Can the decision maker get the answer and the reasons quickly?
- **1** — Answer buried or absent; padded, repetitive or jargon-heavy; far longer than the decision needs, or too thin to act on.
- **3** — Answer findable early; some padding, repetition or jargon; length somewhat out of proportion to the decision.
- **5** — Answer in the opening pages; every slide earns its place; plain, precise language; length proportional to the decision's complexity.

## Error and coverage measures (counted, not scored)

- **Unsupported claim:** an assertion of fact or a number about the company, market, customers or competitors, presented as true, that is neither in the briefing pack nor validly derived from it. Includes invented figures and facts, overstated certainty ("will", "proves") without basis, and causal claims the evidence does not support. Excludes clearly labelled assumptions or estimates with a stated basis, and recommendations or opinions presented as such. List each with a short quote.
- **Numerical error:** a number that contradicts the pack, or a calculation that is wrong beyond rounding (more than about 2% relative, or the wrong sign). List each with the correct value.
- **Material logical contradiction:** two statements in the document that cannot both be true, or a recommendation that contradicts the document's own analysis.
- **Critical evidence coverage:** for each answer-key evidence item marked critical, whether the document uses it (yes / partial / no).
- **Key insights, calculations, trade-offs, traps:** per answer-key item, whether the document reaches it / does it correctly / identifies it / falls into it.
- **Recommendation defensibility:** yes / partial / no, against the key's defensibility criteria (not against its preferred answer).
- **Hypothesis handling:** how the document treats the initial hypothesis stated in the pack, and whether that treatment is appropriate given the evidence (the key gives the expected handling and why). Reward updating that the evidence supports; do **not** reward contrarianism: rejecting a hypothesis the evidence supports is as wrong as keeping one it refutes.
