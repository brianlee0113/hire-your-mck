# hire-your-mck

**Brief it like a partner. Get the deck in minutes.**

McKinsey-style decks from your research — built by an ex-McKinsey consultant.
Reverse-engineered from publicly available McKinsey decks: action titles, storylines,
editable charts, and a source for every number.

*Not affiliated with or endorsed by McKinsey & Company.*

> 🚧 v2 in progress — being rebuilt as a **Claude Skill**.

Give it your research (or just the messages you want to land) and it builds a
consulting-style deck: an Executive Summary whose bullets become each slide's
action title, every slide backed by data, **editable native PowerPoint charts**,
and an Excel workbook listing the source of every number.

Three modes:

1. **Full deck (detailed)**: storyline and data filled in
2. **Full deck (flow only)**: storyline and recommended exhibit type for each slide (ghost deck)
3. **Single slide**

Rule: no number goes on a slide without a source. If there is no source, the tool leaves a placeholder.

## Build the skill (v2 preview)

```
python tools/build_skill.py      # -> dist/hire-your-mck/ and dist/hire-your-mck.zip
```

- **Claude.ai:** upload `dist/hire-your-mck.zip` as a skill.
- **Claude Code:** copy `dist/hire-your-mck/` into `~/.claude/skills/`.

The skill writes a storyline spec (JSON), checks it with `scripts/check.py`, and renders it with `scripts/render.py`.


## License

MIT. See [LICENSE](LICENSE).
