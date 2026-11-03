"""Reproduce the saved results and paper figures from the repository root."""

import argparse
from pathlib import Path
from scguard import core, replay
from scguard._io import write
from scguard.reference import tasks, verify_manifest


def reproduce(output):
    """Replay both cohorts and regenerate the current figures and example guard."""
    from scguard.plotting.figures import render

    output = Path(output)
    root = Path(__file__).resolve().parent
    resolved = output.resolve()
    protected = [root] + [
        root / name
        for name in [
            "scguard",
            "tests",
            "docs",
            "examples",
            "assets",
            "provenance",
            "third_party",
            ".github",
        ]
    ]
    if resolved == root or any(resolved == p or p in resolved.parents for p in protected[1:]):
        raise ValueError("Choose an output directory separate from source and reference files")
    integrity = verify_manifest()
    print("Reference hashes verified.", flush=True)
    results = {
        "reference_integrity": integrity,
        "writer": replay.writer(),
        "cross_family": replay.cross_family(),
        "source_checker_jobs_executed": 0,
    }
    write(output / "replay.json", results)
    print("Both saved-result cohorts replayed.", flush=True)
    figures = render(output / "figures")
    catalogue = tasks("cross_family")
    left = catalogue["miniz-3.1.0-crc32"]["model"]
    right = catalogue["miniz-3.1.1-crc32"]["model"]
    write(output / "crc_kernel.json", core.build_kernel(left, right, 8, 8, "return"))
    (output / "crc_guard.c").write_text(core.export_mixed_guard(left, right), encoding="utf-8")
    write(
        output / "reproduction.json",
        {
            "all_checks_passed": True,
            "valid_requests_replayed": results["writer"]["valid_requests"]
            + results["cross_family"]["valid_requests"],
            "affine_certificates_replayed": results["cross_family"][
                "independently_replayed_affine_certificates"
            ],
            "figure_sets": figures["figure_sets"],
            "table_sets": figures["table_sets"],
            "source_checker_jobs_executed": 0,
        },
    )
    print(
        "Figures, tables, example guard and reproduction report written to " + str(output),
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("build"))
    reproduce(parser.parse_args().output)
