"""Active disagreement queries for the writer grammar."""

from bisect import bisect_left, bisect_right
import z3
from ..models import writer
from .. import _io as artifacts


def learn_writer(capacities, points, oracle, max_rounds=4):
    """Learn with oracle(capacity, input, entry_byte) -> (return, eight bytes).

    The caller supplies native observations. This function generates queries
    and fits a candidate; source admission is a separate operation.
    """
    artifacts.need(type(max_rounds) is int and max_rounds >= 0, "Nonnegative round budget")
    points = sorted(set(points))
    artifacts.need(
        points and points[0] == 0 and points[-1] == writer.MAX_X,
        "Training includes both domain endpoints",
    )
    observed = {}
    rounds = []

    def query(new_points):
        for capacity in capacities:
            for x in new_points:
                for entry in [0, 255]:
                    observed[capacity, x, entry] = oracle(capacity, x, entry)

    query(points)
    for iteration in range(max_rounds + 1):
        summary = writer.learn(capacities, points, observed)
        additions, record = disagreements(summary, points, observed)
        record["round"] = iteration
        rounds.append(record)
        if not additions:
            return {
                "model": summary,
                "rounds": rounds,
                "ambiguities_closed": True,
                "native_queries": len(observed),
                "source_admission_performed": False,
            }
        artifacts.need(iteration < max_rounds, "Active-query round budget exhausted")
        query(additions)
        points = sorted(set(points) | set(additions))
    raise ValueError("Unreachable inference state")


def symbolic(token, x, initial, bit):
    if token < 2:
        return z3.BitVecVal(token, 32)
    if token < 23:
        return z3.LShR(x, token - 2) & 1
    if token < 44:
        return ~z3.LShR(x, token - 23) & 1
    if token == 44:
        return z3.LShR(initial, bit) & 1
    return ~z3.LShR(initial, bit) & 1


def disagreements(summary, points, obs):
    queries = set()
    witnesses = []
    checked = 0
    for cap in summary["capacities"]:
        for cell in summary["cells"][str(cap)]:
            included = points[bisect_left(points, cell["lo"]) : bisect_right(points, cell["hi"])]
            masks = None
            for x in included:
                _, zero = obs[cap, x, 0]
                _, ones = obs[cap, x, 255]
                current = writer.candidates(x, zero, ones)
                masks = current if masks is None else [a & b for a, b in zip(masks, current)]
            artifacts.need(masks and all(masks), "Training-compatible features")
            x = z3.BitVec("disagreement_x", 32)
            initial = z3.BitVec("disagreement_entry_byte", 32)
            solver = z3.Solver()
            solver.set(timeout=10000)
            solver.add(z3.UGE(x, cell["lo"]), z3.ULE(x, cell["hi"]), z3.ULE(initial, 255))
            for pos, mask in enumerate(masks):
                selected = cell["features"][pos]
                for alt in range(writer.FEATURES):
                    if alt == selected or not mask >> alt & 1:
                        continue
                    solver.push()
                    solver.add(
                        symbolic(selected, x, initial, pos % 8)
                        != symbolic(alt, x, initial, pos % 8)
                    )
                    result = solver.check()
                    checked += 1
                    artifacts.need(result in [z3.sat, z3.unsat], "Disagreement query timeout")
                    if result == z3.sat:
                        for direction in [0, 1]:
                            opt = z3.Optimize()
                            opt.set(timeout=10000)
                            opt.add(
                                z3.UGE(x, cell["lo"]),
                                z3.ULE(x, cell["hi"]),
                                z3.ULE(initial, 255),
                                symbolic(selected, x, initial, pos % 8) == direction,
                                symbolic(alt, x, initial, pos % 8) == 1 - direction,
                            )
                            objective = opt.minimize(z3.BV2Int(x))
                            outcome = opt.check()
                            artifacts.need(
                                outcome in [z3.sat, z3.unsat], "Canonical directed disagreement"
                            )
                            if outcome == z3.unsat:
                                continue
                            q = opt.model().eval(x, model_completion=True).as_long()
                            artifacts.need(
                                opt.lower(objective).as_long()
                                == q
                                == opt.upper(objective).as_long(),
                                "Exact minimum disagreement",
                            )
                            artifacts.need(
                                q not in points,
                                "A disagreement cannot contradict a fitted native sample",
                            )
                            queries.add(q)
                            witnesses.append(
                                {
                                    "cap": cap,
                                    "lo": cell["lo"],
                                    "hi": cell["hi"],
                                    "output_bit": pos,
                                    "chosen": selected,
                                    "alternative": alt,
                                    "direction": direction,
                                    "query_x": q,
                                }
                            )
                    solver.pop()
    return (
        sorted(queries),
        {
            "SMT_feature_comparisons": checked,
            "new_query_inputs": sorted(queries),
            "disagreement_witnesses": witnesses,
        },
    )
