# Review request for Codex: Hacker News post (2026-11-27)

The post is `benchmark/report/hn-post.md` (title options + first comment). It is meant to travel: the hook is that a
~6,000-line skill lost to a six-line prompt, and the prompt itself is in the post for readers to copy. Please review
it as a sceptical HN reader and as an auditor of our own evidence. We want it sharp, but not one word stronger than
the evidence.

## What to check

1. **Every number against its source.** Please trace each one and say where it comes from or that it is wrong:
   - Round 1, pairwise: skill vs plain Claude 2–13, skill vs six-line prompt 0–15 → `benchmark/report/REPORT.md` §4
     (tables around "Hire Your McK vs Vanilla / vs Strong baseline"), v2 judging after the extraction-bug fix.
   - "45 sandboxed runs", "5 cases", "every deck reached the same answers, none fell for the traps" → REPORT.md.
   - Round 2: "6 new cases written by a different model, frozen before any run" → `METHODOLOGY.md` §16,
     `FREEZE-holdout.json`, commits 2c4fca0 and 5b51bfb.
   - "tied 6–6 on reasoning", "kept 100% of the critical content", "fixed 1 of 10", "about 3.5× the cost", "the
     skill writing its own analysis with a self-critique step lost 0–6" → `benchmark/results/holdout/tables.md`
     §1–2 (H2a vs B tie/split 6/6; preserved critical valid 100%; verified corrections 1 of 10 critical invalid;
     cost B $2.14–3.88 vs H2a $10.45–13.09; B beat E1 6/6). Is "tied 6–6" a fair reading of "tie/split" in all six
     (both orders disagree or both say tie)? Should it say "no winner in any of the 6 cases" instead?
   - "about 6,000 lines of instructions and code": we counted `.md` + `.py` in `plugin/skills/hire-your-mck` at
     1.2.1 (`032de9e`): 6,234 lines. Is it honest to call the benchmarked skill "6,000-line" when most of the lines
     are renderer code, not instructions? Would "6,000 lines of instructions and code" (as written) survive an HN
     reader checking?
   - "the prompt is six lines": `benchmark/prompts/conditions/B_strong_baseline.md` is one lead line + five bullets
     (plus the task). Fair to call it six lines?
2. **Overclaims and framing.**
   - "the model didn't need help reasoning" – the claim is about these synthetic cases and the reasoning visible in
     the deck. Is the sentence too general?
   - "The skill's rigid slide format squeezed out the sensitivities and option comparisons that judges rewarded" –
     this is our reading of judge rationales (REPORT.md §4.7, C2 arm). Is it stated as a finding or as an
     interpretation? Should it say "judges' notes suggest"?
   - "It is the most useful thing in this post" – fine as voice, or does it read as clickbait?
   - Round 2 compiled decks are H2a = B's own deck restyled. A reader may say "of course it ties – it is the same
     analysis". Does the post make that clear enough, and is "tied on reasoning" the right claim?
3. **Caveats.** Are the four caveats enough? Missing: the human review was one person (the author) and stopped at
   7 of 18 pairs, and the author recognised one side in most pairs; the judge is Fable 5.2 (same family as the model
   judged). Should those be in the comment, or is a link to the report enough?
4. **Title.** Which of the three would you post, and why? Any risk in option 2 ("ex-McKinsey") we should weigh?
5. **Anything a hostile top comment would hit first**, and a one-line answer we should have ready.

## What we already know is open

- `benchmark/` is only on the `v1.3-h` branch; the report link is a placeholder until we decide where it lives.
- `REPORT.md` covers round 1 only. Round 2 (holdout) and the c12 founder case still have to be added so every
  number in the comment is in the report.

Please reply with: a corrected first comment (or a marked-up diff), a list of numbers you could not trace, and your
title pick.
