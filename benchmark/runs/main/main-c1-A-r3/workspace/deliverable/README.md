# Onsoo Botanicals: US entry decision, board deck

- `Onsoo_US_entry_board_deck.pptx`: 17 slides (15 main slides plus 2 appendix slides), 16:9. Built only from `evidence/briefing-pack.md`.
- `onsoo_us_entry_model.py`: the cash, payback and margin model behind every number in the deck. Run `python3 onsoo_us_entry_model.py` to reproduce them.

## Answer
Enter the US in 2027 through the Amazon-led route (Option A), with four changes to the plan:
1. Plan on 30–32% ACoS rather than 25%, and fund a $4M peak-cash envelope.
2. Fix the labels and take the listings in-house before scaling.
3. Add retail only once Amazon sales exceed $10M and aided awareness reaches 20% (the CEO's draft says 15%), starting with a door test.
4. Weight off-Amazon marketing toward social media.

Decline the retail-led route (Option B), which fails the cash cap, payback and margin floor on its own numbers. Defer the Japan scale-up (Option J).

## Judgment calls made without the user
- "On the way to $40M by 2030" is read as a credible path to $40M, not $40M in 2030. No option reaches $40M in 2030 within the other limits.
- Inventory is held at four months of landed cost. The yearly increase is a cash outflow, cash flows are pre-tax and undiscounted, and no inventory is released at the end.
- Door counts are treated as in place for the full year. One-time costs are expensed in the year incurred.
- The 32% ACoS benchmark median is used as the realistic downside case.
- The pack gives no working-capital inputs for Option J, so none are modeled.
- Charts are drawn as native PowerPoint shapes, not chart objects. No renderer was available in the sandbox, so layout was checked with a custom preview, not in PowerPoint itself.
