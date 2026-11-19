# Holdout cases c6–c11 (from Codex, 2026-11-18)

Received as hire_your_mck_holdout_c6_c11_full.zip. Rebuilt with build_holdout_cases.py: byte-identical. validate_holdout_cases.py: PASS. The zip's register script was not run; registration was done by hand (experiment.json cases, runner case codes).

## Codex README

### Hire Your McK independent holdout cases c6–c11

Six new **synthetic, deterministic** strategic decision cases prepared independently from the H skill's design. This folder is a drop-in overlay at the repository root: `benchmark/cases/` includes six `packet.md`s and reproducible source code, `benchmark/answer_keys/` includes evaluator-only `.json`, `.md` and `.calc.json` for each case, and `benchmark/config/holdout_cases_entries.json` contains case metadata.

## Contents

| Case | Decision | Initial hypothesis handling | Packet length |
| --- | --- | --- | ---: |
| c6-make-buy | Manufacturing make-or-buy | reject | ~1,080 words |
| c7-m-and-a | Software acquisition / partnership | revise | ~1,140 words |
| c8-distribution-network | Warehouse network optimization | keep_with_conditions | ~1,100 words |
| c9-capacity-timing | Capex timing and outsourcing | keep_with_conditions | ~1,120 words |
| c10-portfolio-exit | Product portfolio pruning | reject | ~1,080 words |
| c11-oem-licensing | OEM exclusivity / licensing | revise | ~1,080 words |

Each packet has at least one binding constraint; a definition mismatch; a tempting but noncausal correlation; and a misleading internal metric. Multiple defensible recommendations are permitted where assumptions are made explicit. Keys label **critical** vs optional decision insights. The `decision_requirements` field accepts multiple means of proof rather than one required exhibit type.

## Installation into your cloned repository

Copy the `benchmark/` directory tree over the existing repository's `benchmark/` directory (no existing files are overwritten: these are new filenames). Run:

```bash
python benchmark/cases/build_holdout_cases.py
python benchmark/scripts/register_holdout_cases.py
python benchmark/cases/validate_holdout_cases.py
```

This build **does not regenerate or touch cases c1–c5**. Repeated runs should produce byte-identical case packets and keys.

`register_holdout_cases.py` edits only `config/experiment.json`'s `cases` dictionary. It does **not** create `phases.holdout`, an `H2a` condition, or alter the pre-existing conditions. Register the final dependent H2a execution workflow and freeze prompts / skill / judge / case hashes separately **before running**.

## Holdout handling

- The **generation agents may read** `cases/<case>/packet.md` only. Exclude `answer_keys/`, `.calc.json`, and `holdout_models.py` from all generation workspaces and prompt context. For stronger isolation, copy only `packet.md` to the generation sandbox and keep the source generator outside it.
- This case bundle is considered locked once released. Do not adapt any case or key after seeing an arm's performance; keep a public change log for purely factual corrections.
- `expected_handling` in the key is a guidance signal for initial hypothesis revision, **not** a requirement to reach a single approved recommendation. Every item labelled `conditional` requires its stated evidence and binding-constraint tests.
- Since H2a consumes the **same B deck** that is evaluated as the source, score fidelity B→H2a separately from B-vs-E1 strategic reasoning. Do not count B and H2a as independent reasoning draws.

## Important limitations

These are constructed scenarios with internally calculated financial data, not empirical tests of actual consulting performance. The current holdout size of six different cases can detect major failures, but cannot establish statistical non-inferiority to B. Read and verify each generated packet and answer key before the freeze; the author has not made assumptions beyond those stated in the synthetic models.

## Codex experiment notes

### Experiment-specific notes (not part of case packets)

## Condition roles

- **B:** strong six-line prompt. Its generated deck must become the direct input for H2a. A B/H2a pair is the same underlying analysis, not independent draws.
- **E1:** audited integrated skill; should see the *same* generated packet, not the B deck.
- **H2a-restyle:** uses the original B output plus the same packet, without re-solving the strategic decision. Run only after the corresponding B deck is sealed.

## Primary quality metrics

1. **Critical valid unit preservation:** decision-critical evidence / claims, scoped to valid content in source B, mapped by IDs in H2a. Invalid source units must be considered separately.
2. **Verified corrections:** a correction counts as legitimate only when source evidence supports it, a log identifies every linked unit, and every dependent title/summary/exhibit is updated consistently.
3. **Unsupported alteration / introduced error:** no new critical errors; report material and minor separately.
4. **Traceability:** distinguish sourced facts, derived calculations, explicit estimates, and untraceable numbers. `ack` is not equivalent to verifying a critical number.
5. **Rendered readability:** use a blinded human slide review, if possible. Source fidelity can pass even if slides are worse to read.
6. **Time/cost:** report time of B, additional H compile time, and the *combined* end-to-end user experience for H2a.

## Interpretation

A pairwise win for H2a against its B source is not evidence of better strategic reasoning. If H fixes a bug in B's original chart, code that as a correction and do not claim that design caused the win. Two presentation orders of the same pair are judge-order robustness checks, not independent cases. Six synthetic held-out cases are exploratory, not enough to demonstrate non-inferiority at preference >= 0.45.

## Freeze and leakage

The packet files are safe generation inputs. The entire `benchmark/answer_keys` directory and the synthetic calculation model are evaluator-only. Freeze case+key SHA-256, condition code snapshots and evaluators *before* the first holdout result. Never update a case's content or key in response to model outputs; if an error must be fixed, record and disclose it.
