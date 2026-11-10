# McKinsey 7-step problem solving: sourced definition

Collected 2026-11-10. Goal: build the process into a `deck_deep` mode (30–60 slides).

## Authority

Treat **Conn & McLean, *Bulletproof Problem Solving* (Wiley, 2018/2019; "BPS")** and McKinsey's own
podcast "How to master the seven-step problem-solving process" (Sep 2019, Conn / Sarrazin) as authoritative.
Dominic Barton's foreword says Conn wrote the original internal McKinsey deck
"7 Easy Steps to Bulletproof Problem Solving". Umbrex pages and infographics are unattributed rewrites:
they split hypotheses into separate steps and drop the workplan step, which is the one that produces the ghost deck.

| Source | Steps |
|---|---|
| BPS / McKinsey podcast (primary) | Define · Disaggregate · Prioritize (prune) · Workplan · Analyses · Synthesize · Communicate |
| Umbrex "McKinsey approach" | Problem definition · Structure · Prioritize · Plan analyses · Conduct analyses · Synthesize · Craft recommendations |
| Umbrex infographic | Define · Break down · Prioritize · Develop hypotheses · Test hypotheses · Synthesize · Develop recommendations (+ iterate) |

The process is an iterative cycle ("like an accordion"): a one-day answer first, then refine as data
comes in. Treating it as one-off is a named pitfall.

## The steps

| # | Step | Tools | Artifact | Failure modes |
|---|---|---|---|---|
| 1 | Define the problem | Problem definition worksheet; "porpoising" between statement, hypotheses and data; test against a counterfactual | One-sentence problem statement + worksheet (decision maker, success criteria, time frame, accuracy needed, boundaries / off-limits) | Vague statement, no action implied, no time frame, scope too narrow, solving for a sub-unit instead of the highest level |
| 2 | Disaggregate | Component/lever trees → hypothesis and decision trees; profit/ROIC trees; MECE; 2–3 alternative "cleaving frames" | Issue or hypothesis tree, iterated | Not MECE; vague labels; stuck at component level instead of testable hypotheses |
| 3 | Prioritize (prune) | 2×2: importance of the lever × can our efforts move it; prioritization worksheet | Pruned tree = critical path | Debating branches that are unimportant or that nobody can change |
| 4 | Workplan | Per branch: issue, hypothesis, analysis, data source, owner, end product, timing. "Dummy the chart" first; knock-out analyses first; 2–3 week chunks + rough Gantt | Workplan, dummied charts, one-day answer (situation · observation/complication · resolution) | 50-page, 3-month plans; confirmation bias from early hypotheses |
| 5 | Conduct analyses | Heuristics first (order of magnitude min/likely/max, 80:20, compound growth, expected value, root cause), then "big guns" (regression, experiments, ML) | One chart with a message per hypothesis | Jumping to complex models; analysis not tied to a hypothesis |
| 6 | Synthesize | Draw findings onto the revised tree; one-day answer → pyramid | Governing thought + storyline pyramid | "Anxious parade of knowledge"; assuming the analysis is the answer |
| 7 | Communicate | Answer first (or a revealed decision tree for hostile audiences); storyboard with headlines across the top; horizontal logic; state certainty | The deck | Conclusions not linked to a storyline for action |

## Checks a tool can enforce

- **Problem statement**: outcome-focused, specific and measurable, time-bound, names the decision maker's criteria and boundaries (including accuracy needed), set at the highest level.
- **Tree**: MECE; branches are hypotheses or questions, not labels; alternative cuts considered.
- **Prioritization**: every leaf scored on impact and ability to influence; big but unmovable levers cut explicitly.
- **Workplan**: every analysis has a hypothesis, dummied output, data source and end product; knock-out analyses first.
- **One-day answer**: exactly three parts, not a bullet dump.
- **Analysis**: an order-of-magnitude pass before any model.
- **Synthesis / story**: has the problem evolved? are success criteria and boundaries honored? is every pyramid point supported by data? do headlines read across as a story? is uncertainty stated?

## Mapping to a 30–60 slide deck

| Step | Slides |
|---|---|
| 1 | "The question we were asked" / context slide; closing check against the worksheet |
| 2 | Level-1 branches = 3–5 sections = agenda; optional issue-tree slide |
| 3 | Section lead slides (the index of pruned leaves, whose codes prefix evidence titles); "what we did not pursue and why" |
| 4 | Ghost deck (dummied charts with hypothesis titles); backup: approach, sources, workplan |
| 5 | Evidence slides: one analysis = one chart, title states the finding |
| 6 | Executive summary (governing thought + supporting arguments) |
| 7 | Storyline order, recommendations, next steps, risks and uncertainty |

Loop: one-day answer → pyramid → ghost deck → data → rewrite titles where hypotheses failed → re-prune.

## Related methods

- MECE, Pyramid Principle, SCQ(A): Barbara Minto (ex-McKinsey), *The Pyramid Principle*. BPS credits her for the pyramid and uses situation–observation–resolution for one-day answers.
- Day-1 hypothesis, elevator test, 80/20: Rasiel, *The McKinsey Way* (1999); Rasiel & Friga, *The McKinsey Mind* (2001). Not re-verified in this round.
- Charts: Zelazny, *Say It with Charts*.
- "Ghost deck" is consulting slang; BPS says "storyboard" and "dummy".

## Sources

Primary
- McKinsey Podcast transcript (Sep 2019): https://cdn.ksrinc.com/mckinseysurvey/How-to-master-the-seven-step-problem-solving-process.pdf
  (article: https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/how-to-master-the-seven-step-problem-solving-process)
- McKinsey, "Want better strategies? Become a bulletproof problem solver" (Aug 2019): https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/want-better-strategies-become-a-bulletproof-problem-solver
- Conn & McLean, *Bulletproof Problem Solving*, Wiley: https://www.oreilly.com/library/view/bulletproof-problem-solving/9781119553021/ (front matter sample: https://content.e-bookshelf.de/media/reading/L-12338825-f56a47234f.pdf)

Secondary
- Umbrex: https://umbrex.com/resources/mckinsey-problem-solving/ · https://umbrex.com/resources/frameworks/problem-solving-frameworks/mckinsey-7-step-problem-solving-process/
- Leadership Now summary: https://www.leadershipnow.com/leadingblog/2019/10/7_steps_to_bulletproof_problem.html

Gaps: the exact labels of BPS Exhibit 1.1 and the fields of the Exhibit 2.1 worksheet are images and were not read.
