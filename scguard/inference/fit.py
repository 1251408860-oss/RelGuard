"""Fit the current model grammar to bundled native observations."""

from ..models import affine, typed
from ..checks import model as model_check
from ..reference import DATA, ROW, native_records, tasks


def infer_reference(identity, root=DATA):
    """Return a candidate inferred from saved cross-family native executions."""
    sources = tasks("cross_family", root)
    if identity not in sources:
        raise ValueError(
            "Select a cross-family task; writer inference uses learn_writer with an oracle."
        )
    recorded = sources[identity]["model"]
    observations = native_records(root / "cross_family/training" / identity)
    ordered = recorded.get("kind") == "ordered_byte_comparisons"
    data = typed.comparison_dataset() if ordered else affine.dataset()
    values = [observations[ROW.pack(s["x"], s["cfg"], *s["entry"])] for s in data["cases"]]
    if recorded["schema"] == "affine-state-contract-v1":
        candidate = affine.learn(data, values)
    elif ordered:
        candidate = typed.learn_order(data, values)
        model_check.model(candidate)
    else:
        candidate = typed.learn_integer(data, values)
        model_check.model(candidate)
    return {
        "model": candidate,
        "native_observations": len(values),
        "matches_recorded_candidate": candidate == recorded,
        "source_checks_executed": 0,
        "source_admission_performed": False,
    }
