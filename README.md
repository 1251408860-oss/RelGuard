# RelGuard: Source-Checked Relational Guards from Automatic State Contracts

RelGuard is the core research implementation accompanying **Source-Checked Relational Guards from Automatic State Contracts**. It learns state contracts from native executions, checks their connection to C source, and constructs executable relational guards for observation-specific reuse of verification evidence.

The repository is organized around model construction, independent checking, and experimental reproduction. The navigation table maps these parts of the paper to their implementation and reference data.

[中文说明](./README.zh-CN.md)

## Repository Navigation & Artifact Mapping

| Paper Component / Experiment Scope | Description | Directory Link |
| :--- | :--- | :--- |
| Contract models and inference | Writer bit projections, affine state models, bounded integer expressions, ordered comparisons, and active distinguishing queries | [Models](./scguard/models) · [Inference](./scguard/inference) |
| Independent validation | Model and emission checking, elimination-certificate replay, and receipt-bound source-field admission | [Checks](./scguard/checks) |
| Source obligations and guard generation | CRC composition, arithmetic normalization, typed source bridges, paired writer guards, and prefix emission | [Source obligations](./scguard/source) · [Code generation](./scguard/codegen) · [Public API](./scguard/core.py) |
| Writer experiment | Twelve source contracts and eight version transitions, with native references and matched guard-policy results | [Writer data](./scguard/data/writer) |
| Cross-family experiment | Twelve API/version tasks across CRC-32, Adler-32, memory move, and comparison sign, with training observations and relational certificates | [Cross-family data](./scguard/data/cross_family) |
| Paper figures and tables | Two architecture figures, two experiment figures, and two tables, with editable PDF/SVG/TeX outputs | [Figure implementation](./scguard/plotting) · [Rendered assets](./assets) |
| Reproduction and validation records | Unified reproduction entry point, regression tests, file fingerprints, and local validation records | [Reproduction entry](./reproduce.py) · [Tests](./tests) · [Provenance](./provenance) |

## Global Environment Overview

The saved-result reproduction workflow runs on Windows and Ubuntu/Linux with **Python 3.12 or later**. Its Python dependencies are listed in [requirements.txt](./requirements.txt):

- `z3-solver` for symbolic disagreement queries and restricted emission checks;
- `numpy` and `matplotlib` for paper figures and table previews.

The GitHub [Core checks workflow](./.github/workflows/ci.yml) runs the unit tests, saved-result reproduction, candidate inference, and API example on Ubuntu.

New C source verification uses a separate environment with the recorded **CBMC 6.11.0**, **ESBMC 8.6**, and **GCC 13.3** configuration. Source identities, wrapper definitions, generated-header settings, ABI assumptions, and checker flags are supplied in the dataset protocols. The [source-checking guide](./docs/source_checks.md) describes this workflow.

## Bundled Reference Data

The reference data are included in the repository checkout under [scguard/data](./scguard/data). The two experiment cohorts contain models, protocols, request records, native O0/O2 outputs, emitted C guards, saved compiled-guard outputs, and relational systems. The cross-family cohort also contains the original training observations used to reconstruct its candidates.

| Cohort | Valid Requests | SUPPORT | REFUTE |
| :--- | ---: | ---: | ---: |
| Writer, typed policy | 122,880 | 72,162 | 50,718 |
| Cross-family, completed source routes | 49,896 | 13,076 | 36,820 |

The writer guard provides **4.8 times the determinate coverage** of whole-entry identity on the matched catalogue. Cross-family replay checks **2,592 affine certificates** and **648 integer or ordered-return systems**, including the resolution of **17,496 intermediate abstentions** on the same valid requests. Both final cohorts have zero incorrect determinate decisions on their saved catalogues. Intermediate outcomes, comparison-policy errors, and malformed-request controls remain in the data.

Verify the **242 reference files** against [their SHA-256 manifest](./scguard/data/manifest.sha256.json):

```bash
python -m scguard verify-data
```

Record layouts and cohort contents are documented in [docs/data.md](./docs/data.md).

## Quick Installation

Clone the repository and install the Python dependencies:

```bash
git clone https://github.com/1251408860-oss/RelGuard.git
cd RelGuard
python -m pip install -r requirements.txt
```

Run the following commands from the repository root.

### Reproduce the saved experiments and paper figures

```bash
python reproduce.py
```

This command verifies the reference files, replays both experiment cohorts, rebuilds the four figures and two tables, and exports an example CRC guard and checked relational kernel. It uses the bundled execution records.

| Output | Contents |
| :--- | :--- |
| `build/replay.json` | Recomputed results for 172,776 valid requests and the affine-certificate checks |
| `build/figures/` | Four figure sets, two table previews, editable TeX tables, and layout/color checks |
| `build/crc_kernel.json` | CRC relational equations and independently checked elimination certificate |
| `build/crc_guard.c` | Example executable CRC guard |
| `build/reproduction.json` | Reproduction summary |

### Reconstruct candidates and export guards

```bash
python -m scguard infer --task miniz-3.1.0-crc32 --output build/crc-model.json
python -m scguard export --left miniz-3.1.0-adler32 --right miniz-3.1.1-adler32 --output build/adler-guard.c
python -m scguard export --cohort writer --left libgrapheme-2.0.1 --right libgrapheme-2.0.2 --output build/writer-guard.c
python -m examples.quickstart
```

The inference command fits a cross-family candidate from its saved training observations. Writer active inference accepts a native-observation callback through `scguard.inference.active.learn_writer`. Source admission establishes the candidate's connection to C under the recorded call premises.

### Run validation checks

```bash
python -m unittest discover -s tests -v
```

The **28 tests** cover model schemas, invalid requests, active inference, candidate reconstruction, emission mutations, elimination-certificate mutations, exact guard regeneration, and source-field admission.

### Recheck C source obligations

Prepare the specified upstream source files, generated headers, and C verification tools before running new source checks. Generate an obligation with:

```bash
python -m scguard harness --task miniz-3.1.0-crc32 --route crc-step --output build/checks/crc-step.c
```

The [source-checking guide](./docs/source_checks.md) lists the available routes, their premises, source preparation, and raw-result interpretation. New checks retain their execution receipts alongside earlier outcomes.

Detailed API usage, data formats, and source-verification requirements are documented in [the implementation guide](./docs/implementation.md), [the data guide](./docs/data.md), and [the source-checking guide](./docs/source_checks.md). `python -m scguard --help` lists the individual commands.

## Notices

The project's own code currently has no license grant. Third-party font notices are retained in [NOTICE.md](./NOTICE.md) and [third_party](./third_party).
