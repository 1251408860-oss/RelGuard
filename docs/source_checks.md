# Source checks

The package includes current obligation generators and source-result admission code. Rechecking a C implementation requires the specified upstream sources, generated headers, and external verifiers.

## Recorded configuration

`scguard/data/writer/source_protocol.json` and `scguard/data/cross_family/source_protocol.json` contain the target identities, URLs, assumptions and verifier flags. Target wrappers are in the corresponding `source_tasks.json`.

The recorded environment uses CBMC 6.11.0, ESBMC 8.6 and GCC 13.3, with the specified 64-bit little-endian C11 model. Match the recorded safety, pointer, overflow and unwinding checks when reconstructing a source obligation.

Place upstream files in `source/` relative to the generated harness, and generated headers in `generated/`. The emitted includes specify the required source units. The miniz protocol records its export-header content and disabled features; the musl wrapper records the memory profiles.

## Generate obligations

```sh
python -m scguard harness --task miniz-3.1.0-crc32 --route crc-step --output build/checks/crc-step.c
python -m scguard harness --task miniz-3.1.0-crc32 --route crc-stream --output build/checks/crc-stream.c
python -m scguard harness --task miniz-3.1.0-crc32 --route crc-dfcc-step --output build/checks/crc-dfcc.c
python -m scguard harness --task miniz-3.1.0-adler32 --route adler-ranges --output build/checks/adler-ranges.c
python -m scguard harness --task miniz-3.1.0-adler32 --route integer-prefix --output build/checks/adler-prefix.c
python -m scguard harness --task musl-1.2.4-memcmp_sign --route typed-bridge --output build/checks/memcmp-bridge.c
python -m scguard harness --task libgrapheme-2.0.1 --cohort writer --output build/checks/writer.c
```

The other routes are `direct`, `crc-frame` and `typed-conditional`. A completed compositional route requires all its recorded premises.

## Source normalization

For Adler source preparation, use `scguard.source.arithmetic.instrument`, `reduce_source` and `translation_check`. The independent translation check verifies that only the recognized operations change. Source ranges and the unsigned remainder identity must be established before the reduced source check is composed with the original.

For ordered comparisons, `scguard.models.typed.normalize_return` creates the normalized copy. `scguard.checks.model.normalization` checks the recognized complete typed function and exact transformation. The bridge obligation connects the two implementations.

## Read source results

```sh
python -m scguard read-fields --folder path/to/result --label CBMC --engine cbmc
```

The reader expects `CBMC.stdout.bin`, `CBMC.stderr.txt` and `CBMC.execution.json` in this example. The receipt binds raw stream hashes and completion status. The independent field reader checks the nine expected return/byte targets and all auxiliary properties. The tests include accepted, refuted-return, unsafe, and incomplete records.

New checks add evidence. Original failed checks and UNKNOWN results remain unchanged. Saved-result replay and candidate reconstruction launch no C source-checker jobs.
