"""Independent typed-model schema and emission checks."""

import hashlib
import json
import re

MAX = 2**32 - 1


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def model(s):
    need(
        s["schema"] == "bounded-observation-model-v1"
        and type(s["input_bits"]) is int
        and s["input_bits"] == 96,
        "Model input schema",
    )
    need(
        s["configurations"] == list(range(9)) and all(type(v) is int for v in s["configurations"]),
        "Full declared configuration cover",
    )
    need(
        set(s["cells"]) == set(map(str, range(9))) and s["post_bytes"] == "identity",
        "Every cell and object observation",
    )
    for cell in s["cells"].values():
        if s["kind"] == "bounded_uint32_integer_affine":
            need(set(cell) == {"base", "coefficients", "minimum", "maximum"}, "Integer cell schema")
            a = cell["coefficients"]
            base = cell["base"]
            need(
                type(base) is int
                and 0 <= base <= MAX
                and len(a) == 9
                and all(type(v) is int and 0 <= v <= MAX for v in a),
                "Strict nonnegative integer coefficients",
            )
            maximum = base + a[0] * MAX + 255 * sum(a[1:])
            need(maximum <= MAX, "Whole-box no-wrap certificate")
            need(
                type(cell["minimum"]) is int
                and type(cell["maximum"]) is int
                and cell["minimum"] == base
                and cell["maximum"] == maximum,
                "Exact integer range",
            )
        else:
            need(
                s["kind"] == "ordered_byte_comparisons"
                and set(cell) == {"pairs", "otherwise"}
                and type(cell["otherwise"]) is int
                and cell["otherwise"] == 0,
                "Ordered cell schema",
            )
            need(type(cell["pairs"]) is list and len(cell["pairs"]) <= 7, "Bounded ordered list")
            for pair in cell["pairs"]:
                need(
                    type(pair) is list
                    and len(pair) == 2
                    and all(type(i) is int and 0 <= i < 8 for i in pair)
                    and pair[0] != pair[1],
                    "Strict byte indices",
                )


def emission(folder):
    s = read(folder / "model.json")
    model(s)
    code = (folder / "summary.c").read_text()
    seal = read(folder / "candidate_seal.json")
    need(
        sha(folder / "model.json") == seal["model_sha256"]
        and sha(folder / "summary.c") == seal["summary_sha256"],
        "Model and emission seals",
    )
    for name, key in [
        ("check.c", "check_sha256"),
        ("normalized_check.c", "normalized_check_sha256"),
    ]:
        if (folder / name).exists():
            need(
                sha(folder / name) == seal[key] and (folder / name).read_text().count(code) == 1,
                "Exact checked emitted summary and harness seal",
            )
    lines = code.splitlines()
    need(
        lines[:2]
        == ["static uint32_t rf_summary(uint32_t x,unsigned cfg,unsigned char*b){", "(void)x;"],
        "Exact restricted summary interface",
    )
    pos = 2
    for cfg in range(9):
        need(lines[pos] == "if(cfg==" + str(cfg) + "U){", "Ordered exhaustive configurations")
        pos += 1
        cell = s["cells"][str(cfg)]
        if s["kind"] == "bounded_uint32_integer_affine":
            q = re.fullmatch(r"uint32_t out=(\d+)U;", lines[pos])
            need(q is not None and int(q[1]) == cell["base"], "Integer origin")
            pos += 1
            got = [0] * 9
            while lines[pos] != "return out;}":
                q = re.fullmatch(r"out\+=(\d+)U\*(x|\(uint32_t\)b\[([0-7])\]);", lines[pos])
                need(q is not None, "Accepted uint32 integer expression")
                j = 0 if q[2] == "x" else int(q[3]) + 1
                need(got[j] == 0 and 0 < int(q[1]) <= MAX, "Unique integer feature")
                got[j] = int(q[1])
                pos += 1
            need(got == cell["coefficients"], "Emitted coefficients")
            pos += 1
        else:
            pairs = []
            while lines[pos] != "return 0U;}":
                q = re.fullmatch(
                    r"if\(b\[([0-7])\]!=b\[([0-7])\]\)\{if\(b\[\1\]<b\[\2\]\)return UINT32_MAX;return 1U;\}",
                    lines[pos],
                )
                need(q is not None, "Exact byte-order branch semantics")
                pairs.append([int(q[1]), int(q[2])])
                pos += 1
            need(pairs == cell["pairs"], "Exact ordered branch list")
            pos += 1
    need(lines[pos:] == ["return 0U;}"], "No unchecked statements")
    return {
        "all_checks_passed": True,
        "method": "exact restricted integer/byte-order C interpretation",
        "all_96_input_bits": True,
        "SMT_or_external_C_jobs": 0,
        "general_C_frontend_certified": False,
    }


def evaluate(s, state):
    cell = s["cells"][str(state["cfg"])]
    b = state["entry"]
    if s["kind"] == "bounded_uint32_integer_affine":
        out = cell["base"] + sum(a * v for a, v in zip(cell["coefficients"], [state["x"]] + b))
    else:
        out = 0
        for i, j in cell["pairs"]:
            if b[i] != b[j]:
                out = MAX if b[i] < b[j] else 1
                break
    return [out] + list(b)


def normalization(original, normalized):
    # This deliberately accepts only the fully typed tiny function shape used
    # here, not an untyped rewrite of arbitrary conditional expressions.
    shape = r"#include <string\.h>\s+int memcmp\(const void \*vl, const void \*vr, size_t n\)\s*\{\s*const unsigned char \*l=vl, \*r=vr;\s*for \(; n && \*l == \*r; n--, l\+\+, r\+\+\);\s*return n \? \*l-\*r : 0;\s*\}\s*"
    need(
        re.fullmatch(shape, original) is not None,
        "Recognized complete typed function; pure condition and both int branches",
    )
    token = "return n ? *l-*r : 0;"
    prefix, suffix = original.split(token)
    need(
        normalized == prefix + "if (n) return *l-*r;\n\treturn 0;" + suffix,
        "Only the admitted conditional-return lowering",
    )
    return {
        "all_checks_passed": True,
        "rule": "C11 N1570 6.5.15 paragraphs 4-5 and 6.8.6.4",
        "same_condition_evaluated_once_same_selected_int_expression": True,
        "unchosen_dereference_not_evaluated": True,
        "both_branches_have_int_type_under_CHAR_BIT_8_INT32": True,
        "algorithm_body_loop_and_original_source_archive_unchanged": True,
        "restricted_source_translation_trust_not_general_C_validation": True,
    }
