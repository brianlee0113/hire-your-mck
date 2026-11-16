# HN submission draft

**Title:** Can a Claude Skill improve strategic reasoning? We tested ours and it didn't

**URL:** link to `benchmark/report/REPORT.md` in the repository

---

**Text (for a Show HN, or as the first comment):**

I built Hire Your McK, a Claude Skill that turns a brief into a consulting-style deck. Its pitch is that it gets the
*logic* right, not just the slides: pyramid storyline, action titles, and a hypothesis-driven "deep deck" workflow
with an issue tree. I wanted to know whether that claim holds, so I benchmarked it against the same model without
the skill.

Setup:

- Five synthetic strategy cases. Each one plants a misleading initial hypothesis, plus traps: a definitional
  inconsistency, a correlation sold as causation, and a margin figure that leaves out a cost.
- Three conditions:
  - plain Claude;
  - Claude plus a six-line methodology prompt (hypothesis-driven, pyramid, MECE, action titles);
  - the skill.
- Same model (Opus 5.5, effort high), three runs each, 45 runs in total. Every run was sandboxed with no network,
  and the run order was randomised.
- Each deck was extracted to text, normalised into a common storyline format, anonymised, and judged against a
  hidden answer key. Fable 5.2 scored every deck and compared them in pairs, showing each pair in both orders.
  Sonnet 5.5 gave a second set of scores.

Results:

- **The skill did not improve reasoning. It scored slightly lower.** In pairwise judging, plain Claude beat it in
  13 of 15 matched pairs, and the methodology prompt beat it in 15 of 15.
- **All 45 decks reached the same, defensible answers.** They revised (or rejected) the initial hypothesis exactly
  where the evidence said to, and fell for none of the traps. On these cases the model does not need help with the
  reasoning.
- **The skill's decks were 2.7× longer** (45 slides against 17–20) and cost about twice as much to make. Judges
  mostly penalised repetition, such as section summaries restating their own slides. Without the concision
  dimension the gap shrinks to borderline against plain Claude, but it remains against the methodology prompt.
- **Making the skill's decks short did not help.** After seeing these results I added a follow-up arm (labelled
  exploratory, design written down before it ran): the skill in its default full-deck mode. Its decks came down to
  baseline length (22 slides) and its clarity score recovered. It still lost all 45 of its pairwise comparisons,
  including 15 of 15 against the skill's own long deck. The judges usually called it the leaner deck, then preferred
  the other one for its sensitivities, option comparisons and downside cases. The skill's compact slide format
  seems to squeeze out exactly that material.
- **The six-line methodology prompt was the best condition** (13–1 against plain Claude, pairwise).
- **What the skill does add is product, not reasoning:** a source workbook for every number, editable charts, and a
  QA pass.

Caveats:

- n = 5 cases, so no case-level test can reach p < 0.05.
- The cases and answer keys are synthetic and written by me.
- Claude judged Claude, and there is no human review yet (the package is in the repo).
- The skill ran unattended. Left to itself it always chose its longest mode; the short mode was tested only in the
  post-hoc follow-up.
- We also caught a bug in our own extraction that had made the skill look worse. We fixed it and re-judged
  everything. The gap shrank, but the direction held. The report keeps both versions.

Everything is in the repo: cases, answer keys, prompts, transcripts, judgments, and a one-command rerun.
