# Code guide

All implementation modules live in `scguard/` and use package-relative imports.

## Models and inference

`models/writer.py` implements the writer bit-feature grammar and piecewise inference. `inference/active.py` generates distinguishing queries and exposes the active loop as an oracle-based API:

```python
from scguard.inference.active import learn_writer
from scguard.models.writer import MAX_X


def oracle(capacity, x, entry_byte):
    # Replace this body with observations from the desired native program.
    return 1, [128 | (x & 63)] + [entry_byte] * 7


result = learn_writer([8], [0, 256, 65536, MAX_X], oracle)
candidate = result["model"]
```

`models/affine.py` learns the affine state representation from origin/basis observations and constructs relational systems. `models/typed.py` handles bounded integer and ordered-byte candidates.

`inference/fit.py` reconstructs the current cross-family candidates from the bundled training streams. It uses each grammar's recorded deterministic dataset. Candidate reconstruction is checked against the recorded model, while source admission remains a separate step.

## Independent checks and source obligations

`checks/affine.py` contains the current exact polynomial emission interpreter and the independent row-operation checker in one module. It does not import the affine generator. `checks/writer.py` independently interprets writer emission, and `checks/model.py` and `checks/prefix.py` check the typed and prefix representations.

`checks/evidence.py` checks raw-stream receipt hashes, terminal results, target counts and auxiliary safety properties. It admits each observation field only when the corresponding requirements complete.

`source/crc.py` supplies step, streaming, frame, and enforced-step obligations. `source/arithmetic.py` supplies range obligations and the checked arithmetic source transformation. `codegen/prefix.py` emits the checked integer-prefix representation.

## Public API

`core.py` exposes `validate_model`, `model_value`, `decide_model`, `build_kernel`, `export_guard` and `source_harness`. `export_guard` selects the writer or cross-family emitter. Model equality is evaluated under the supplied model; using it as a C-source contract additionally needs the recorded source-admission evidence and call premises.

`reference.py` reads and verifies saved data. `replay.py` recomputes native/model agreement, certificate checks and comparison-policy totals. `reproduce.py` combines this replay with figure generation and an example guard/kernel export.

## Figures

`plotting/figures.py` contains the current author-adjusted drawing functions. `plotting/style.py` contains shared plot primitives. Render with `python -m scguard figures --output build/figures`. The plotting implementation writes only to its requested output folder.
