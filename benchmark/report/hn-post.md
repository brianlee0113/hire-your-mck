# HN submission draft (v2, 2026-11-27)

Status: draft for Codex review (`benchmark/docs/12-hn-post-review-for-codex.md`). Not posted.

## Title (pick one)

1. **Show HN: My 6,000-line Claude Skill for strategy decks lost to a 6-line prompt** (recommended)
2. Show HN: I'm an ex-McKinsey consultant. My deck-building AI lost to a 6-line prompt
3. Show HN: I benchmarked my Claude Skill for strategy decks – a 6-line prompt reasoned better

Notes: (1) puts the contrast in the title and makes no brand claim. (2) has the strongest hook but puts the firm's
name in the title; the README already says "Built by an ex-McKinsey consultant" and disclaims affiliation, so this is
a judgement call. Avoid "McKinsey-style" in the title either way.

**URL:** the repository (README first screen), with the benchmark report linked in the first comment.

## First comment

I built hire-your-mck, a Claude Skill that turns a brief into a consulting-style deck: a
storyline, an action title on every slide, editable PowerPoint charts, and an Excel workbook with a source for every
number. About 6,000 lines of instructions and code. I claimed it made Claude's reasoning better.

Then I benchmarked it. It lost to this:

```
- Work hypothesis-driven. State an initial answer early, write down what would have to be true for it to hold,
  test each of those against the evidence, and change the answer if the evidence does not support it.
- Build the storyline with the pyramid principle: one governing thought that answers the question, an executive
  summary up front whose points become the sections, and the supporting arguments and evidence beneath each point.
- Keep every grouping MECE (mutually exclusive, collectively exhaustive).
- Give every slide an action title: a full-sentence takeaway that the slide's content proves.
- Base the recommendation on evidence. Quantify where the data allows and show the calculations, weigh the
  alternatives and their trade-offs, and state the key assumptions, risks and uncertainties.
```

Paste that under any "make me a deck" request. It is the most useful thing in this post.

What happened:

- **Round 1** – 5 strategy cases with planted traps, 45 sandboxed runs, judged blind against hidden answer keys.
  Plain Claude beat the skill 13–2 in pairwise judging. The six-line prompt beat it 15–0. Every deck reached the same
  answers and fell for none of the traps: the model didn't need help reasoning. The skill's rigid slide format
  squeezed out the sensitivities and option comparisons that judges rewarded.
- **So I changed the skill's job.** The prompt does the thinking; the skill only "compiles" the finished analysis
  into the deck: same numbers, same conclusions, plus sources, native charts and a checker.
- **Round 2** – 6 new cases written by a different model and frozen before any run. Compiled decks tied the
  prompt-only decks 6–6 on reasoning and kept 100% of the critical content. They also inherited the analysis's
  mistakes: they fixed 1 of 10, at about 3.5× the cost. A skill that writes its own analysis, even with a
  self-critique step, still lost to the prompt 0–6.

What a skill like this is good for, then, is the deliverable, not the thinking: every number traceable to a
source, charts you can edit, and a checker that fails a deck on what a reviewer would send back. Version 1.4.0
came out of my own blind review of the slides: box-style formulas looked too simple to trust, the text was too small,
and every slide was the same grey box.

Caveats: small n, synthetic cases, Claude judged Claude, and the only human reviewer so far is me.

Cases, answer keys, prompts, transcripts, judgments and a one-command rerun: [benchmark report link]

## Before posting (checklist)

- [ ] Codex review done and resolved (`benchmark/docs/12-hn-post-review-for-codex.md`)
- [ ] Decide where `benchmark/` lives publicly (branch link vs merge to main) and fill in the report link
- [ ] `benchmark/report/REPORT.md` updated with the holdout (round 2) and the c12 founder case, so every number in
      the comment is in the report
- [ ] README: heading on line 49 and gallery/demo images decided at the same time
- [ ] Post Tue–Thu, 8–10 am US Eastern; stay to answer comments for the first two hours
