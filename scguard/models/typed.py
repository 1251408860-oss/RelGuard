"""Bounded integer and ordered-byte models."""

import itertools
import random
from . import affine

MAX = 2**32 - 1

SCHEMA = "bounded-observation-model-v1"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def learn_integer(data, values):
    cells = {}
    for cfg, ids in data["basis_case_ids"].items():
        base = values[ids[0]][0]
        coeff = [values[ids[1]][0] - base] + [
            values[ids[1 + 32 + 8 * j]][0] - base for j in range(8)
        ]
        need(all((v >= 0 for v in coeff)), "Nonnegative bounded integer grammar")
        maximum = base + coeff[0] * MAX + 255 * sum(coeff[1:])
        need(0 <= base <= maximum <= MAX, "No wrapping in integer candidate")
        cells[cfg] = {"base": base, "coefficients": coeff, "minimum": base, "maximum": maximum}
    return {
        "schema": SCHEMA,
        "kind": "bounded_uint32_integer_affine",
        "input_bits": 96,
        "configurations": list(range(9)),
        "features": ["uint32_parameter"] + ["byte" + str(j) for j in range(8)],
        "cells": cells,
        "post_bytes": "identity",
    }


def comparison_dataset():
    rng = random.Random(2026110207)
    cases = []
    fit = []
    held = []
    for cfg in range(9):
        for entry in itertools.product([0, 1, 255], repeat=8):
            fit.append(len(cases))
            cases.append({"x": rng.getrandbits(32), "cfg": cfg, "entry": list(entry)})
    for cfg in range(9):
        for _ in range(512):
            held.append(len(cases))
            cases.append(
                {
                    "x": rng.getrandbits(32),
                    "cfg": cfg,
                    "entry": [rng.randrange(256) for j in range(8)],
                }
            )
    return {
        "cases": cases,
        "fit_ids": fit,
        "held_out_ids": held,
        "seed": 2026110207,
        "fit_alphabet": [0, 1, 255],
        "held_out_full_byte_cube_sample_only": True,
    }


def sign(a, b):
    return MAX if a < b else 1 if a > b else 0


def learn_order(data, values):
    cells = {}
    for cfg in range(9):
        rows = [
            (data["cases"][i]["entry"], values[i][0])
            for i in data["fit_ids"]
            if data["cases"][i]["cfg"] == cfg
        ]
        chain = []
        while any((v for b, v in rows)):
            choices = []
            for i in range(8):
                for j in range(8):
                    if i == j:
                        continue
                    selected = [(b, v) for b, v in rows if b[i] != b[j]]
                    if selected and all((v == sign(b[i], b[j]) for b, v in selected)):
                        choices.append((-len(selected), i, j))
            need(choices, "Ordered-pair grammar cannot fit this task")
            _, i, j = min(choices)
            chain.append([i, j])
            rows = [(b, v) for b, v in rows if b[i] == b[j]]
            need(len(chain) <= 7, "Equality-prefix forest has at most seven independent edges")
        need(all((v == 0 for b, v in rows)), "Ordered candidate zero leaf")
        cells[str(cfg)] = {"pairs": chain, "otherwise": 0}
    return {
        "schema": SCHEMA,
        "kind": "ordered_byte_comparisons",
        "input_bits": 96,
        "configurations": list(range(9)),
        "cells": cells,
        "post_bytes": "identity",
    }


def value(s, state):
    if s.get("schema") == "affine-state-contract-v1":
        packed = affine.evaluate(s, affine.vector(state), state["cfg"])
        return affine.split_output(packed)
    cell = s["cells"][str(state["cfg"])]
    b = state["entry"]
    if s["kind"] == "bounded_uint32_integer_affine":
        r = cell["base"] + sum((a * v for a, v in zip(cell["coefficients"], [state["x"]] + b)))
    else:
        r = next((sign(b[i], b[j]) for i, j in cell["pairs"] if b[i] != b[j]), 0)
    return [r] + b


def emit(s, name="rf_summary", with_parity=True):
    if s.get("schema") == "affine-state-contract-v1":
        text = affine.emit(s, name)
        return text if with_parity else text.removeprefix(affine.PARITY + "\n")
    lines = ["static uint32_t " + name + "(uint32_t x,unsigned cfg,unsigned char*b){", "(void)x;"]
    for cfg in range(9):
        cell = s["cells"][str(cfg)]
        lines += ["if(cfg==" + str(cfg) + "U){"]
        if s["kind"] == "bounded_uint32_integer_affine":
            lines += ["uint32_t out=" + str(cell["base"]) + "U;"]
            for j, a in enumerate(cell["coefficients"]):
                if a:
                    lines += [
                        "out+="
                        + str(a)
                        + "U*"
                        + ("x" if j == 0 else "(uint32_t)b[" + str(j - 1) + "]")
                        + ";"
                    ]
            lines += ["return out;}"]
        else:
            for i, j in cell["pairs"]:
                lines += [
                    "if(b["
                    + str(i)
                    + "]!=b["
                    + str(j)
                    + "]){if(b["
                    + str(i)
                    + "]<b["
                    + str(j)
                    + "])return UINT32_MAX;return 1U;}"
                ]
            lines += ["return 0U;}"]
    return "\n".join(lines + ["return 0U;}"]) + "\n"


def harness(t, s, normalized=False):
    wrapper = affine.wrapper(t)
    if normalized:
        need(t["api"] == "memcmp_sign", "Only declared conditional-return normalization")
        wrapper = wrapper.replace(
            '#include "source/src/string/memcmp.c"', '#include "normalized/memcmp.c"'
        )
    text = (
        wrapper
        + emit(s)
        + affine.PORTABLE
        + '\nvoid harness(void){uint32_t x=nondet_u();unsigned cfg=nondet_u();AF_ASSUME(cfg<9U);\n_Alignas(8) unsigned char actual[8],predicted[8];\nfor(unsigned i=0;i<8;i++){actual[i]=nondet_b();predicted[i]=actual[i];}\nuint32_t r=af_actual(x,cfg,actual),p=rf_summary(x,cfg,predicted);\nAF_ASSERT(r==p,"target.return");\n'
    )
    for j in range(8):
        text += (
            "AF_ASSERT(actual["
            + str(j)
            + "]==predicted["
            + str(j)
            + '],"target.byte'
            + str(j)
            + '");\n'
        )
    return text + "}\n"


def normalize_return(source):
    old_text = "return n ? *l-*r : 0;"
    new_text = "if (n) return *l-*r;\n\treturn 0;"
    need(source.count(old_text) == 1, "Unique typed conditional return")
    return source.replace(old_text, new_text)


def bridge(t, corrupt=False):
    text = (
        affine.wrapper(t)
        + '\n#define memcmp rf_normalized_memcmp\n#include "normalized/memcmp.c"\n#undef memcmp\n'
        + affine.PORTABLE
        + "\nvoid harness(void){uint32_t x=nondet_u();unsigned cfg=nondet_u();AF_ASSUME(cfg<9U);\n_Alignas(8) unsigned char actual[8],other[8];\nfor(unsigned i=0;i<8;i++){actual[i]=nondet_b();other[i]=actual[i];}\nuint32_t r=af_actual(x,cfg,actual);\nint v=rf_normalized_memcmp(other+af_profiles[cfg][1],other+af_profiles[cfg][2],af_profiles[cfg][0]);\nuint32_t p=v<0?UINT32_MAX:v>0?1U:0U;\n"
    )
    text += "AF_ASSERT(r==" + ("(p^1U)" if corrupt else "p") + ',"target.return");\n'
    for j in range(8):
        text += (
            "AF_ASSERT(actual["
            + str(j)
            + "]==other["
            + str(j)
            + '],"target.byte'
            + str(j)
            + '");\n'
        )
    return text + "}\n"
