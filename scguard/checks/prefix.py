"""Independent checked interpretation of prefix arithmetic."""

import re
from . import model as base


def check(s, code):
    base.model(s)
    base.need(
        set(s)
        == {"schema", "kind", "input_bits", "configurations", "features", "cells", "post_bytes"}
        and s["kind"] == "bounded_uint32_integer_affine",
        "Exact integer model schema",
    )
    base.need(
        s["features"] == ["uint32_parameter"] + ["byte" + str(i) for i in range(8)],
        "Fixed independent feature interpretation",
    )
    lines = code.splitlines()
    base.need(
        lines[:2]
        == ["static uint32_t rf_summary(uint32_t x,unsigned cfg,unsigned char*b){", "(void)x;"],
        "Exact checked interface",
    )
    pos = 2
    bounds = []

    def maximum(v):
        return v[0] + v[1] * (2**32 - 1) + 255 * sum(v[2:])

    def safe(v):
        return len(v) == 10 and all(type(x) is int and x >= 0 for x in v) and maximum(v) < 65536

    for cfg in range(9):
        base.need(lines[pos] == "if(cfg==" + str(cfg) + "U){", "Exhaustive checked configurations")
        pos += 1
        q = re.fullmatch(r"uint32_t lo=(\d+)U,hi=(\d+)U;", lines[pos])
        base.need(q is not None, "Typed literal initialization")
        pos += 1
        values = {"lo": [int(q[1])] + [0] * 9, "hi": [int(q[2])] + [0] * 9}
        base.need(
            all(safe(v) for v in values.values()),
            "Initial lane ranges, including zero-update cells",
        )
        while lines[pos] != "return (hi<<16U)|lo;}":
            q = re.fullmatch(
                r"(lo|hi)\+=(\(uint32_t\)b\[([0-7])\]|(?:(\d+)U\*)?(lo|hi));", lines[pos]
            )
            base.need(q is not None, "Restricted typed addition")
            if q[3] is not None:
                term = [0] * 10
                term[2 + int(q[3])] = 1
            else:
                factor = int(q[4] or 1)
                base.need(0 < factor <= 2**32 - 1, "Unsigned 32-bit coefficient literal")
                term = [factor * x for x in values[q[5]]]
            values[q[1]] = [a + b for a, b in zip(values[q[1]], term)]
            pos += 1
            base.need(all(safe(v) for v in values.values()), "Every intermediate lane range")
        base.need(all(safe(v) for v in values.values()), "Final lane bounds before disjoint OR")
        v = [a + 65536 * b for a, b in zip(values["lo"], values["hi"])]
        cell = s["cells"][str(cfg)]
        base.need(
            v == [cell["base"]] + cell["coefficients"],
            "Exact independent coefficient reconstruction",
        )
        bounds.append(
            {
                "cfg": cfg,
                "low_maximum": maximum(values["lo"]),
                "high_maximum": maximum(values["hi"]),
            }
        )
        pos += 1
    base.need(lines[pos:] == ["return 0U;}"], "No unchecked instructions")
    return {
        "all_checks_passed": True,
        "method": "independent integer coefficient and complete range interpretation",
        "initial_intermediate_and_final_ranges": True,
        "fixed_unsigned_literal_types": True,
        "lane_bounds": bounds,
        "new_SMT_or_C_jobs": 0,
    }
