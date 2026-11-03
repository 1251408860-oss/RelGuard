"""Recompute saved observer decisions and replay independently checked certificates."""

from collections import Counter
import json
from . import core
from .reference import DATA, read, tasks, native_records, unpack_state

NAMES = ["UNKNOWN", "SUPPORT", "REFUTE"]


def cross_family(root=DATA):
    sources = tasks("cross_family", root)
    native = {}
    predictions = {}
    for identity, task in sources.items():
        core.validate_model(task["model"])
        rows = native_records(root / "cross_family/native" / identity)
        native[identity] = rows
        predicted = {key: core.model_value(task["model"], unpack_state(key, "cfg")) for key in rows}
        if predicted != rows:
            raise ValueError("Model/native disagreement for " + identity)
        predictions[identity] = predicted
    final = Counter()
    prior = Counter()
    invalid = certificates = typed = resolved = 0
    pairs = []
    for folder in sorted((root / "cross_family/guards").iterdir()):
        if not folder.is_dir():
            continue
        binding = read(folder / "binding.json")
        left, right = binding["left"]["id"], binding["right"]["id"]
        a, b = sources[left]["model"], sources[right]["model"]
        systems = read(folder / "systems.json")
        before = read(folder / "intermediate/systems.json")
        if len(systems) != 405 or len(before) != 405:
            raise ValueError("Complete configuration/observer cover required")
        for i, system in enumerate(systems):
            ca, cb, obs = system["ca"], system["cb"], system["observer"]
            if (ca * 9 + cb) * 5 + core.OBSERVERS.index(obs) != i or system["admitted"] is not True:
                raise ValueError("Unexpected system identity or admission")
            if system["method"] == "GF2_certified_relation":
                pa, pb = core.affine_projection(a, obs), core.affine_projection(b, obs)
                original = core.affine.equations(pa, pb, ca, cb, obs)
                if original != system["original_rows"]:
                    raise ValueError("Source-model projection disagrees with certificate")
                core.certificate.check_reduction(original, system["system"])
                certificates += 1
            else:
                if (
                    core.affine_projection(a, obs) is not None
                    and core.affine_projection(b, obs) is not None
                ):
                    raise ValueError("Affine projection unexpectedly lost its certificate")
                typed += 1
        payload = (folder / "requests.bin").read_bytes()
        recorded = (folder / "compiled_guard.stdout.bin").read_bytes()
        earlier = (folder / "intermediate/compiled_guard.stdout.bin").read_bytes()
        if len(payload) % 36 or len(recorded) != len(earlier) or len(payload) != 36 * len(recorded):
            raise ValueError("Incomplete request/consumer stream")
        pair_counts = Counter()
        for i, (got, old) in enumerate(zip(recorded, earlier)):
            chunk = payload[i * 36 : (i + 1) * 36]
            ca, cb = int.from_bytes(chunk[4:8], "little"), int.from_bytes(chunk[20:24], "little")
            obs = int.from_bytes(chunk[32:36], "little")
            if ca > 8 or cb > 8 or obs > 4:
                if got != 0 or old != 0:
                    raise ValueError("Invalid control must abstain")
                invalid += 1
                continue
            av, bv = native[left][chunk[:16]], native[right][chunk[16:32]]
            fields = core.FIELDS[core.OBSERVERS[obs]]
            gold = 1 if all(av[j] == bv[j] for j in fields) else 2
            if got != gold:
                raise ValueError("Saved compiled guard/native disagreement")
            previous = before[(ca * 9 + cb) * 5 + obs]
            expected_old = gold if previous["admitted"] else 0
            if old != expected_old:
                raise ValueError("Intermediate field-admission result changed")
            final[NAMES[got]] += 1
            prior[NAMES[old]] += 1
            pair_counts[NAMES[got]] += 1
            resolved += old == 0
        pairs.append(
            {"pair": folder.name, "valid": sum(pair_counts.values()), "counts": dict(pair_counts)}
        )
    expected = read(root / "cross_family/analysis.json")
    if (
        dict(final) != expected["counts"]
        or sum(final.values()) != expected["requests"]
        or invalid != expected["invalid_requests"]
        or certificates != expected["GF2_certificates"]
        or resolved != expected["previous_unknown_requests_newly_decided"]
        or typed != expected["integer_or_order_return_systems_without_GF2_rank"]
    ):
        raise ValueError("Cross-family totals disagree with original analysis")
    return {
        "valid_requests": sum(final.values()),
        "qualified": dict(final),
        "intermediate": dict(prior),
        "resolved_prior_unknowns": resolved,
        "invalid_controls_unknown": invalid,
        "independently_replayed_affine_certificates": certificates,
        "typed_other_systems": typed,
        "pairs": pairs,
        "all_checks_passed": True,
    }


def writer(root=DATA):
    sources = tasks("writer", root)
    native = {}
    for identity, task in sources.items():
        core.writer.validate(task["model"])
        if any(task.get(k) != "SUPPORT" for k in ["source_status", "CBMC", "ESBMC"]):
            raise ValueError("Recorded writer admission is incomplete")
        rows = native_records(root / "writer/native" / identity, signed=True)
        for key, value in rows.items():
            if core.model_value(task["model"], unpack_state(key, "cap")) != value:
                raise ValueError("Independent writer model/native disagreement")
        native[identity] = rows
    policies = {key: Counter() for key in ["typed", "whole_entry", "return_for_all", "drop_frame"]}
    wrong = Counter()
    valid = invalid = 0
    for folder in sorted((root / "writer/guards").iterdir()):
        if not folder.is_dir():
            continue
        binding = read(folder / "binding.json")
        left, right = [s["id"] for s in binding["source_contracts"]]
        a, b = sources[left]["model"], sources[right]["model"]
        data = (folder / "requests.bin").read_bytes()
        output = (folder / "compiled_guard.stdout.bin").read_bytes()
        if len(data) != len(output) * 36:
            raise ValueError("Complete writer records required")
        for i, recorded in enumerate(output):
            chunk = data[i * 36 : (i + 1) * 36]
            sa, sb = unpack_state(chunk[:16], "cap"), unpack_state(chunk[16:32], "cap")
            mask = int.from_bytes(chunk[32:36], "little")
            if (
                not 1 <= mask <= 511
                or not core.writer.valid_input(sa, a["capacities"])
                or not core.writer.valid_input(sb, b["capacities"])
            ):
                if recorded != 0:
                    raise ValueError("Invalid writer control must abstain")
                invalid += 1
                continue
            observer = next((o for o, m in core.MASKS.items() if m == mask), None)
            if observer is None:
                raise ValueError("Unexpected catalogue projection")
            av, bv = native[left][chunk[:16]], native[right][chunk[16:32]]
            fields = core.FIELDS[observer]
            gold = "SUPPORT" if all(av[j] == bv[j] for j in fields) else "REFUTE"
            if NAMES[recorded] != gold:
                raise ValueError("Writer compiled guard/native disagreement")
            valid += 1
            for name, counts in policies.items():
                answer = core.writer.decide(a, b, sa, sb, observer, admitted=True, policy=name)[
                    "status"
                ]
                counts[answer] += 1
                wrong[name] += answer != "UNKNOWN" and answer != gold
    table = read(root / "figures/table_data.json")["writer_policy_rows"]
    for (name, counts), row in zip(policies.items(), table):
        expected = [int(str(v).replace(",", "")) for v in row[1:]]
        actual = [counts["SUPPORT"], counts["REFUTE"], counts["UNKNOWN"], wrong[name]]
        if actual != expected:
            raise ValueError("Writer policy totals changed: " + name)
    return {
        "valid_requests": valid,
        "invalid_controls_unknown": invalid,
        "policies": {
            name: {**dict(counts), "wrong_determinate": wrong[name]}
            for name, counts in policies.items()
        },
        "identity_coverage_ratio": valid
        / sum(policies["whole_entry"][k] for k in ["SUPPORT", "REFUTE"]),
        "all_checks_passed": True,
    }
