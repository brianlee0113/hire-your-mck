# Vague-request test: main skill vs v1.3-h on a "here is the material, make a deck" request (frozen 2026-11-26)

**Question.** On a request as vague as the one in the 2026-11-24 real-use test (PLAN.md v3-B8), which went to
`single_slide` and produced one slide in about 10 minutes, does v1.3-h choose a full deck like main does? The
no-mode test (`10-nomode-test.md`) named the decision maker and the decision question, and both skills chose
`deck_deep`; it left this path open.

## Design: two runs, started together

| Arm | Skill snapshot | Request |
|---|---|---|
| **Cv** (main skill, vague request) | `env/plugin-main` (1.2.1) | `V_vague_request.md` |
| **V13v** (v1.3-h, vague request) | `env/plugin-v13` (5f0b04a) | same |

Request (Korean, as the user would write it):
`/hire-your-mck 자료는 ./evidence/briefing-pack.md 에 있어. 이걸로 덱 만들어줘. 결과는 ./deliverable/ 에 저장해줘.`

- No decision maker, no question, no mode, and no "I won't be available" line: the skill asks its checkpoint
  questions as it would with a real user, and the harness answers each with the standard auto-reply ("choose the
  option you recommend and continue"; up to 4 auto-replies).
- Case c3 (Brightwork, AI dispatch assistant), one run per arm. Config `config/vague.json`, phase `vague`, seed
  2036, per-turn timeout 3000 s, no infra retries, `caffeinate` and the stall watchdog. Claude Code 2.1.332.

## Measures
Mode chosen (spec `mode`), slide count, number of auto-replies used, wall time over all turns, cost, `check.py`
of the arm's own skill.

## Reading (fixed before the run)
- **Mode problem** (fix mode selection before merging): V13v chooses `single_slide` or `deck_flow`, or delivers
  fewer than 10 slides, while Cv makes a full deck.
- **Same behaviour**: V13v chooses the same mode as Cv, or a full deck (`deck_detailed` / `deck_deep`) with at
  least 15 slides.
- If **both** fall short of a full deck, the problem is not new in v1.3; it is reported, but it does not block the
  merge.
- Time is reported, not judged: one pair cannot separate a 15% gap from noise.

## Limits
One case, one run per arm: this can show that the problem exists, not that it never happens. The v3-B8 session
was interactive (the user answered the questions); here the auto-reply always picks the recommended option.

## Cost
2 runs, ≈ $15.
