# Benchmark: does Hire Your McK improve strategic reasoning?

A reproducible experiment that compares three conditions on five synthetic strategy cases, using the same model
(`claude-opus-5-5`, effort high) in fresh, isolated Claude Code sessions:

- **A · Vanilla Claude:** a plain request to build the deck
- **B · Strong baseline:** the same request plus generic method instructions (hypothesis-driven, pyramid, MECE, action titles)
- **C · Hire Your McK:** the same request through the real skill (`/hire-your-mck`)
- **C2 · Hire Your McK, full-deck mode** (exploratory, added after the main results; `METHODOLOGY.md` §12): the same as
  C with the skill's `deck_detailed` mode named in the request

Outputs are normalised into one storyline format, anonymised, and scored by independent Claude judges against
hidden answer keys. A human-review package is included. See [`METHODOLOGY.md`](METHODOLOGY.md) for the
pre-registered design and [`report/REPORT.md`](report/REPORT.md) for the results.

**All case data is synthetic.** The companies, people and numbers are fictional.

## Layout

| Path | What |
|---|---|
| `METHODOLOGY.md`, `FREEZE.json` | Pre-registered design; SHA-256 of every design file at freeze time |
| `FREEZE-explore-c2.json` | Hashes recorded before the exploratory C2 arm ran |
| `docs/01-system-understanding.md` | What in the product could affect reasoning vs formatting vs verification |
| `config/experiment.json` | Models, effort, tools, limits, seeds, cases, phases |
| `cases/models.py`, `cases/build_cases.py` | Synthetic data models and the packet/answer-key builder |
| `cases/<case>/packet.md` | Evidence packet: the only input a generation session gets |
| `answer_keys/` | Hidden evaluator keys (`.md`, `.json`) and every computed number (`.calc.json`) |
| `prompts/conditions/` | Common task, condition prompts, the fixed auto-reply |
| `prompts/eval/`, `schemas/` | Normaliser, rubric, judge prompts, JSON schemas |
| `scripts/` | Generation runner, audit, extraction, normalisation/blinding/judging, e2e metrics, analysis, human package |
| `runs/<phase>/<run_id>/` | Per run: `meta.json` (prompt, model, tokens, cost, time, attempts), gzipped transcripts, workspace, extraction, normalised storyline, audit, e2e metrics |
| `eval/<phase>/` | Blinding key, blind documents, automated judgments, pairwise judgments, human package and scores |
| `results/<phase>/` | `per_doc.csv`, `summary.json`, `tables.md`, `figures/` |
| `report/` | Write-up and Hacker News post |

## Reproduce

Requirements: macOS or Linux, [Claude Code](https://claude.com/claude-code) logged in (`claude` on PATH; a
subscription or API key with access to `claude-opus-5-5`, `claude-fable-5-2` and `claude-sonnet-5-5`), Python 3.12+,
and [`uv`](https://docs.astral.sh/uv/).

```bash
benchmark/run_all.sh pilot     # 6 runs: validates the pipeline
benchmark/run_all.sh main      # 45 runs, then audit, extraction, normalisation, judging, analysis
```

`HYM_BENCH_WORK` sets where the isolated workspaces live (default `~/hym-bench-work`; must be outside this
repository). Steps are idempotent: an existing output is never regenerated, so an interrupted run resumes where it
stopped. To start a phase from scratch, delete `runs/<phase>/` and `eval/<phase>/`.

Individual steps:

```bash
python3 benchmark/cases/build_cases.py                           # packets + answer keys (deterministic)
python3 benchmark/scripts/run_generation.py --phase main --dry-run   # show the seeded run order
python3 benchmark/scripts/run_generation.py --phase main         # generation (hours)
benchmark/.venv/bin/python benchmark/scripts/audit_runs.py   --phase main
benchmark/.venv/bin/python benchmark/scripts/extract_deck.py --phase main
benchmark/.venv/bin/python benchmark/scripts/e2e_metrics.py  --phase main
benchmark/.venv/bin/python benchmark/scripts/evaluate.py all --phase main
benchmark/.venv/bin/python benchmark/scripts/make_human_eval.py --phase main
benchmark/.venv/bin/python benchmark/scripts/analyze.py      --phase main
# exploratory arm C2 (after main): generation, audit/extract/e2e with --phase explore-c2, then
benchmark/.venv/bin/python benchmark/scripts/explore_c2.py all     # results/explore-c2/tables.md
```

## Human review

Open `eval/main/human/index.html` in a browser (it works offline), enter a reviewer id (R1, R2, R3), score each
document, and export the JSON. Import with
`benchmark/.venv/bin/python benchmark/scripts/make_human_eval.py --phase main --import human-scores-R1.json ...`,
then rerun `analyze.py`. Instructions: `eval/main/human/INSTRUCTIONS.md`.

## Isolation, in short

Each run happens in a fresh directory that holds only `evidence/briefing-pack.md`. No user settings, CLAUDE.md,
memory, MCP servers or plugins are loaded except the skill for condition C (from a frozen copy of `plugin/`). The Bash
sandbox has no network and cannot read this repository, `~/.claude` or other runs. The Read, Edit and Write tools are
denied the same paths, and web tools are denied. `audit_runs.py` checks every transcript for breaches.

## What is not committed

`.pptx`, `.xlsx` and images that runs produce are git-ignored to keep the repository small. Their SHA-256 hashes
are in each run's `meta.json`; text extractions and normalised storylines are committed. Full transcripts contain
base64 slide previews the agents rendered; the committed `transcript-*.slim.jsonl.gz` copies replace that image data
with its SHA-256 (`scripts/slim_transcripts.py`). Everything else in a transcript is unchanged.
