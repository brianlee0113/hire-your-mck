# Deep decks (`deck_deep`): the seven-step workflow

Use this file instead of Steps 1–2 of `SKILL.md` when the user picks a deep deck (30–60 slides). Steps 3–5 of `SKILL.md` (write the spec, QA, render) still apply. The process follows Conn & McLean, *Bulletproof Problem Solving* (define · disaggregate · prioritize · workplan · analyze · synthesize · communicate), and the layout follows long public decks (rules P, T and L in `principles.md`, section D).

A deep deck stops at **four checkpoints**, one more than the other modes: a wrong problem or tree costs 50 slides, so both are confirmed before any data work. Ask every checkpoint as multiple choice, recommendation first (see "How to ask" in `SKILL.md`).

Everything you decide goes into the spec as you go: `problem`, `issue_tree`, `sections`, then slides. Write and check one section at a time; a 50-slide spec written in one pass is hard to fix.

## Step 1 · Define the problem → Checkpoint 1

Draft the problem definition worksheet from the user's request and material (`problem` in the spec):
- **statement**: one question, outcome-focused, measurable, time-bound, at the highest level the decision maker owns. "Should we launch a mid-market AP product by Q3 2027, and at what price?", not "Mid-market AP market".
- **decision_maker**, **success_criteria** (how they judge the answer), **deadline**, **accuracy** needed, **out_of_scope**.

Checkpoint 1 asks, in one go (skip what the first message answers):
1. **Problem statement:** 2–3 drafts that differ in scope or level, the recommended one first.
2. **Out of scope:** the boundaries you assumed, to confirm or change.
3. **Deck type** (`meta.deck_type`): client diagnostic (Recommended for a company decision: summary, sizing, ends on how to make it happen) · policy analysis (methodology and sensitivities, large appendix) · research report (key questions as the agenda, ends on takeaways).
4. **Length:** 30–40 slides (Recommended) · 40–60 slides.
5. **Material and look:** as in Checkpoint 1 of `SKILL.md`.

## Step 2 · Disaggregate

Build the issue tree (`issue_tree`). Draft 2–3 trees that cut the problem differently (by customer and product, by value driver, by the decision's conditions) and recommend one.
- Level 1: 3–5 branches, mutually exclusive and collectively exhaustive. Each becomes one section.
- Every node is a testable **hypothesis sentence**, never a label: "Mid-market firms will pay for AP automation within two years", not "Demand".
- Leaves are specific enough that one analysis can confirm or kill them.

## Step 3 · Prioritize → Checkpoint 2

Score every leaf on **importance** (how much the answer depends on it) and **influence** (can the decision maker move it): high · medium · low. Cut big branches nobody can move, and small ones, with a `cut_reason`; they go to the appendix slide "What we did not pursue". Give every kept node a code: "2" for a branch, "2a" for its leaf.

Checkpoint 2 shows the recommended tree as an indented list (code, hypothesis, scores, kept or cut with the reason) and the alternative cuts in one line each. Ask: build on this tree (Recommended) · use alternative cut B · change branches · keep a cut branch. The approved level-1 branches are the sections.

## Step 4 · Workplan and ghost deck → Checkpoint 3

For each kept leaf write the `workplan`: the analysis that would prove or kill it, the dummied exhibit (archetype and axes), candidate sources, and `knock_out: true` for analyses that could end a branch on their own. Run those first.

Write the **one-day answer** in three parts (`problem.one_day_answer`): situation, complication, resolution. It is the first draft of the governing thought.

Then lay out the ghost deck with the long-deck grammar (all slides `ghost`):
- **Front matter, 3–4 slides:** cover, "Key questions" (`{"id": "q", "role": "problem_statement", "status": "filled"}`: the problem statement and one numbered question per section, from `sections[].question`; it needs no exec item), exec summary. No separate full agenda: the exec summary lists the sections, and the tracker before section 1 is the first contents page.
- **Per section:** the agenda again with the section highlighted (`agenda_tracker` with `section_id`), then a **lead slide** that states the section's answer and indexes its leaves (`numbered-levers` with headers such as ["Finding", "Evidence"], `framework-pillars` or `comparison-table`, codes "2a", "2b"), then 1–3 evidence slides per leaf (up to 7 for the one that matters most). Evidence slides set `tree_node`; the renderer puts the code ("2a:") before the title. Methodology a section needs gets one short slide there; full detail goes in the appendix.
- **Storyline order:** context and baseline → size of the prize → deep dives by branch → implications → how to make it happen (last, `deck_type` client diagnostic).
- **Sections over ~20 slides** split into sub-sections (`parent_id`), each with its own tracker and lead slide.
- **Appendix (15–30%)** opens with an `appendix_divider` (it lists the backup pages; the agenda gains an Appendix row), then follows the order of the main sections: what we did not pursue, methodology, assumptions, extra cases, "(1/2)" continuations of long tables.
- Ghost titles are the hypotheses, written as conclusions to prove, in varied sentence shapes (A-09).
- **Pick slide types from the whole catalog (A-13).** Before defaulting to a bar chart or a table, check each leaf against the routing rows for `scatter-bubble` (two measures move together), `heatmap` (many items × several measures), `statement` (a section's turning point) and `framework-pillars`. A 40-slide deck that uses none of them is a warning sign. Put "what it means for us" in the sidebar `implication`, not in a bullet.

Run `check.py`. Checkpoint 3 shows the ghost deck as a list per section (code, title, archetype) with the slide count and the appendix share. Ask: build it (Recommended) · change the order or emphasis · add or drop slides.

## Step 5 · Analyze

When you hand research to subagents, tell them to copy each excerpt from the page text itself, not from a reader's markdown table or a shortened quote, and to give the population, period and base of every survey number; the independent verifier will check exactly that. Collect data leaf by leaf as in Step 2 of `SKILL.md` (sources first from the user, then the web; V-01–V-04). Order of work: knock-out analyses first, then by importance. Do an order-of-magnitude pass (a quick min / likely / max) before any detailed model.

After each leaf, record the `finding`: **confirmed**, **revised** (true with a different size, segment or timing) or **refuted**, with a one-line `note`. A refuted knock-out kills its branch: go back to Step 2 for that branch (re-cut or prune) instead of filling slides that no longer hold.

## Step 6 · Synthesize → Checkpoint 4

Redraw the tree with the verdicts. Rewrite every refuted or revised title to what the data shows (T-04 fails if a title still states a refuted hypothesis). Then rewrite the governing thought and the exec summary from the verdicts: one bold bullet per section, 2–3 sub-points per bullet.

Checkpoint 4 shows which hypotheses flipped and the new governing thought, together with the open placeholders (Checkpoint 3 of `SKILL.md`). Ask: accept the new answer (Recommended) · change the emphasis · and, per open number, the usual choices.

## Step 7 · Communicate

Continue with Steps 3–5 of `SKILL.md`: write the bodies, run `check.py` until every fail is fixed, judge the LLM checks, render. Before rendering, close the loop against the worksheet: does the answer meet the success criteria, respect the out-of-scope list and the accuracy agreed? Say so on the last body slide or in the next steps.

### Source check, second pass (before rendering)

1. **Corroborate the key numbers (V-06).** For every number in a title or the exec summary, search for a second, independent source (another publisher that does not cite the first) and add it to `corroboration` with its own excerpt. If the values differ by more than 2%, keep the better source and say why in `note`. Where no second source exists, leave it: the number stays grade B and `check.py` lists it.
2. **Re-check the pages (V-05).** Run `verify.py spec.json --write`. Without network access, open each source with your own web fetch and record `verified` by hand. Resolve every `not_found`.
3. **Independent verifier.** Someone who did not write the deck re-traces the numbers. In Claude Code, start a subagent with only the spec path and this brief: "For every title and exec summary number, and 10 other numbers picked at random, open the source URL, find the value, and report: id, value found, match or not, and what differs. Read the slide's footnotes first: a newer value left out on purpose, with the reason footnoted, is not stale. Do not edit the spec." In claude.ai (no subagents), do it as a separate pass: put the deck aside, then go through the same list source by source. Judge each finding before applying it (the verifier sees less context than you), fix what holds, and set `verified.by` to `"verifier"` for the numbers it confirmed.
4. Run `check.py` again, then render. The workbook shows every number's grade; grade C numbers get a footnote on their slide.

In the delivery note, add the tree verdicts (how many leaves confirmed, revised, refuted) and the grade count (A/B/C/E) next to the sourced-number count.
