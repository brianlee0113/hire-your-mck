You are preparing a fidelity checklist. A strategy deck (the SOURCE, below as extracted text) is going to be
re-made in another design. List every decision unit a reader of the SOURCE relies on, so that a checker can later
confirm each one survived the re-make with the same meaning.

Decision units: the answer and each recommendation (with its conditions: "only if", "in the base case", "before
X"); each claim that supports them and the numbers that carry it; assumptions and their basis; ranges, base and
stress cases; the alternatives considered and why each loses or how they combine; thresholds, decision gates,
risks and triggers; decisions asked of the reader; next steps. One unit per distinct point; quote the SOURCE's
words closely and keep every number exactly as written.

For each unit:
- `critical`: true if the decision, a headline, an executive-summary item, a gate or the ranking of options depends
  on it; false for supporting detail.
- `valid`: false if the unit is wrong against the briefing pack or the SOURCE's own arithmetic, or if it appears
  in the KNOWN ERRORS list below (an earlier evaluation of the SOURCE). For an invalid unit, give the correct
  version in `correct_version`. A re-make that fixes an invalid unit is a correction, not a loss.

Do not judge the SOURCE's quality, and do not add units the SOURCE does not contain.

<briefing_pack>
{packet}
</briefing_pack>

<known_errors>
{known_errors}
</known_errors>

<source>
{source}
</source>
