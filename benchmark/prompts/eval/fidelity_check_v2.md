You are checking whether a re-made strategy deck (the REMAKE, below as extracted text) preserves the meaning of
the deck it was made from. You have the list of decision units taken from the original, the briefing pack, and the
REMAKE's own correction log (the changes it says it made on purpose, with its evidence). Judge meaning, not
wording: a reworded title that keeps the numbers, conditions, confidence and the ranking of options preserves the
unit. Look everywhere in the REMAKE, main slides and appendix.

For each unit give one status:
- `preserved`: the unit is valid and the REMAKE keeps its meaning (numbers as written, conditions, hedges, causal
  direction, confidence, ranking of options, risks or sensitivities).
- `verified_correction`: the REMAKE changes the unit, and the change is right: the briefing pack or the original's
  own exhibits show the original was wrong, comparing the same metric, definition, base and period. The change is in
  the correction log, and every place in the REMAKE that carries the unit (executive summary, titles, body) says the
  corrected version. A unit marked invalid that the REMAKE states correctly counts here too.
- `unsupported_alteration`: the REMAKE changes the meaning without that proof: a number differs (including a new
  rounding of a number the original showed), a condition or hedge is dropped or added, a range became a point,
  confidence went up or down, a ranking changed, or a correction is applied in one place but contradicted in
  another. A change that treats two different measures as one (for example a strategic ranking of risks rewritten
  to follow the size of a sensitivity) is unsupported. Say exactly what changed and why it is not proven.
- `missing`: not in the REMAKE.
- `inherited_error`: the unit was marked invalid, and the REMAKE repeats the error.
Also give `location`: where in the REMAKE (slide number or title), or "none".

Then list `new_errors`: statements in the REMAKE that are not in the original's units and are wrong against the
briefing pack, or that change what the original concluded, including a summary and a body slide that now disagree.
Classify each: `critical` (would change the decision or a binding-constraint verdict), `material` (changes budget,
sequencing or the reading of a risk, not the decision), `minor` (wording or a small number with no effect on the
decision). Do not list differences in design, order or length.

<briefing_pack>
{packet}
</briefing_pack>

<units>
{units}
</units>

<correction_log>
{corrections}
</correction_log>

<remake>
{remake}
</remake>
