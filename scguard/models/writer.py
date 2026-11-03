"""Bit-projection writer contracts, inference and C generation."""

from copy import deepcopy
from collections import defaultdict
import hashlib
import json
import random

MAX_X = 0x10FFFF

WIDTH = 8

INPUT_BITS = 21

KEEP = 44

INVERT_KEEP = 45

FEATURES = 46

TARGETS = ["target.return"] + ["target.byte" + str(i) for i in range(WIDTH)]

OBSERVERS = {
    "return": [0],
    "first4": [1, 2, 3, 4],
    "last4": [5, 6, 7, 8],
    "buffer8": list(range(1, 9)),
    "full": list(range(9)),
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def feature(token, x, initial, bit):
    if token < 2:
        return token
    if token < 23:
        return (x >> (token - 2)) & 1
    if token < 44:
        return 1 ^ ((x >> (token - 23)) & 1)
    if token == KEEP:
        return (initial >> bit) & 1
    if token == INVERT_KEEP:
        return 1 ^ ((initial >> bit) & 1)
    raise ValueError("Unknown bit feature")


def candidates(x, zero, ones):
    # Features 0/1, input bits 0..20, their inversions, same entry bit/inverse.
    one = 2
    for b in range(INPUT_BITS):
        one |= 1 << ((2 + b) if ((x >> b) & 1) else (23 + b))
    zero_mask = ((1 << 44) - 1) ^ one
    masks = []
    for z, f in zip(zero, ones):
        for b in range(8):
            zb, fb = (z >> b) & 1, (f >> b) & 1
            masks.append(
                (one if zb else zero_mask)
                if zb == fb
                else (1 << (KEEP if zb == 0 else INVERT_KEEP))
            )
    return masks


def validate(s):
    need(
        type(s) is dict and set(s) == {"schema", "domain", "capacities", "bytes", "cells"},
        "Summary schema",
    )
    need(
        s["schema"] == "bit-projection-contract-v1"
        and s["domain"] == [0, MAX_X]
        and type(s["domain"]) is list
        and all(type(v) is int for v in s["domain"])
        and type(s["bytes"]) is int
        and s["bytes"] == WIDTH,
        "Fixed machine domain",
    )
    caps = s["capacities"]
    need(type(caps) is list and caps and len(caps) == len(set(caps)), "Capacity schema")
    need(all(type(c) is int and 0 <= c <= 8 for c in caps), "Strict capacity values")
    need(set(s["cells"]) == set(map(str, caps)), "Every declared capacity")
    for cap in caps:
        cells = s["cells"][str(cap)]
        need(type(cells) is list and cells, "Nonempty cells")
        next_x = 0
        for cell in cells:
            need(type(cell) is dict and set(cell) == {"lo", "hi", "ret", "features"}, "Cell schema")
            need(all(type(cell[k]) is int for k in ["lo", "hi", "ret"]), "Strict cell integers")
            need(
                cell["lo"] == next_x and cell["lo"] <= cell["hi"] <= MAX_X,
                "Disjoint complete cover",
            )
            need(-8 <= cell["ret"] <= 8, "Supported small return constant")
            fs = cell["features"]
            need(type(fs) is list and len(fs) == 64, "Every destination bit")
            need(all(type(t) is int and 0 <= t < FEATURES for t in fs), "Valid bit features")
            next_x = cell["hi"] + 1
        need(next_x == MAX_X + 1, "Full declared input domain")
    return s


def training_points():
    rng = random.Random(2026110201)
    points = set(range(512)) | set(range(0, MAX_X + 1, 256)) | {MAX_X}
    for k in range(21):
        for d in [-1, 0, 1]:
            x = (1 << k) + d
            if 0 <= x <= MAX_X:
                points.add(x)
    points.update(rng.randrange(MAX_X + 1) for _ in range(512))
    return sorted(points)


def learn(caps, points, observations):
    """observations[(cap,x,entry_byte)] -> (ret, eight output bytes).

    Greedy conjunction of compatible bit features. Its cuts are proposals,
    not certified source branches or a claim of minimal partition size.
    """
    need(points[0] == 0 and points[-1] == MAX_X, "Training includes domain endpoints")
    cells = {}
    for c in caps:
        result = []
        lo = 0
        running = None
        ret = None
        for x in points:
            r0, z = observations[c, x, 0]
            r1, f = observations[c, x, 255]
            need(r0 == r1 and -8 <= r0 <= 8, "Return must fit state-independent grammar")
            current = candidates(x, z, f)
            intersection = (
                [a & b for a, b in zip(running, current)] if running is not None else current
            )
            if running is not None and (r0 != ret or any(v == 0 for v in intersection)):
                result.append(
                    {
                        "lo": lo,
                        "hi": x - 1,
                        "ret": ret,
                        "features": [(v & -v).bit_length() - 1 for v in running],
                    }
                )
                lo = x
                running = current
                ret = r0
            else:
                running = intersection
                ret = r0
        result.append(
            {
                "lo": lo,
                "hi": MAX_X,
                "ret": ret,
                "features": [(v & -v).bit_length() - 1 for v in running],
            }
        )
        cells[str(c)] = result
    return validate(
        {
            "schema": "bit-projection-contract-v1",
            "domain": [0, MAX_X],
            "capacities": list(caps),
            "bytes": WIDTH,
            "cells": cells,
        }
    )


def valid_input(state, caps):
    return (
        type(state) is dict
        and set(state) == {"x", "cap", "entry"}
        and type(state["x"]) is int
        and 0 <= state["x"] <= MAX_X
        and type(state["cap"]) is int
        and state["cap"] in caps
        and type(state["entry"]) is list
        and len(state["entry"]) == WIDTH
        and all(type(b) is int and 0 <= b <= 255 for b in state["entry"])
    )


def image(s, state, drop_frame=False):
    need(valid_input(state, s["capacities"]), "Outside summary domain")
    x = state["x"]
    cell = next(c for c in s["cells"][str(state["cap"])] if x <= c["hi"])
    dest = []
    for i in range(WIDTH):
        value = 0
        for bit, token in enumerate(cell["features"][i * 8 : i * 8 + 8]):
            value |= feature(token, x, 0 if drop_frame else state["entry"][i], bit) << bit
        dest.append(value)
    return [cell["ret"]] + dest


def decide(a, b, left, right, observer, admitted=False, policy="typed"):
    if (
        admitted is not True
        or type(observer) is not str
        or observer not in OBSERVERS
        or type(policy) is not str
        or policy not in ["typed", "whole_entry", "return_for_all", "drop_frame"]
        or not valid_input(left, a["capacities"])
        or not valid_input(right, b["capacities"])
    ):
        return {
            "status": "UNKNOWN",
            "reason": "binding_domain_observer_or_source_obligation_missing",
        }
    ia, ib = image(a, left, policy == "drop_frame"), image(b, right, policy == "drop_frame")
    fields = OBSERVERS[observer]
    if policy == "whole_entry":
        same = left == right and a == b
        return {
            "status": "SUPPORT" if same else "UNKNOWN",
            "reason": "whole_entry_and_summary_identity",
        }
    if policy == "return_for_all":
        equal = ia[0] == ib[0]
    else:
        equal = all(ia[j] == ib[j] for j in fields)
    return {
        "status": "SUPPORT" if equal else "REFUTE",
        "changed_fields": [j for j in fields if ia[j] != ib[j]],
        "reason": policy,
    }


def byte_expr(tokens):
    constant = 0
    keep = 0
    inverse = 0
    groups = defaultdict(int)
    for b, t in enumerate(tokens):
        if t == 1:
            constant |= 1 << b
        elif t == KEEP:
            keep |= 1 << b
        elif t == INVERT_KEEP:
            inverse |= 1 << b
        elif t >= 2:
            is_inverse = t >= 23
            source = t - (23 if is_inverse else 2)
            groups[is_inverse, source - b] |= 1 << b
    terms = []
    if constant:
        terms.append(str(constant) + "U")
    if keep:
        terms.append("(initial&" + str(keep) + "U)")
    if inverse:
        terms.append("((~initial)&" + str(inverse) + "U)")
    for (inv, shift), mask in sorted(groups.items()):
        value = "x" if shift == 0 else "(x" + (">>" if shift > 0 else "<<") + str(abs(shift)) + "U)"
        if inv:
            value = "(~" + value + ")"
        terms.append("(" + value + "&" + str(mask) + "U)")
    return "|".join(terms) or "0U"


def emit(s, name="bg_summary"):
    validate(s)
    groups = defaultdict(list)
    for c in s["capacities"]:
        groups[json.dumps(s["cells"][str(c)], sort_keys=True)].append(c)
    lines = ["static int " + name + "(unsigned x,unsigned cap,unsigned char *dst){"]
    for packed, caps in sorted(groups.items(), key=lambda item: min(item[1])):
        lines.append("if(" + "||".join("cap==" + str(c) + "U" for c in caps) + "){")
        for cell in json.loads(packed):
            lines.append("if(x<=" + str(cell["hi"]) + "U){")
            for i in range(WIDTH):
                tokens = cell["features"][i * 8 : i * 8 + 8]
                if tokens == [KEEP] * 8:
                    continue
                expr = byte_expr(tokens)
                lines.append(
                    "{unsigned initial=dst["
                    + str(i)
                    + "];dst["
                    + str(i)
                    + "]=(unsigned char)("
                    + expr
                    + ");}"
                )
            lines.append("return " + str(cell["ret"]) + ";}")
        lines.append("}")
    lines.append("return 0;}")
    return "\n".join(lines) + "\n"


def corrupt(s):
    bad = deepcopy(s)
    first = bad["cells"][str(bad["capacities"][0])][0]
    old = first["features"][0]
    first["features"][0] = 1 if old == 0 else 0
    return bad


def wrap(target):
    pre = "#include <stdint.h>\n#include <stddef.h>\n#include <limits.h>\n"
    pre += '_Static_assert(CHAR_BIT==8 && sizeof(int)==4 && sizeof(void*)==8,"ABI");\n'
    pre += '#ifdef BG_UNSIGNED_CHAR\n_Static_assert((char)255>0,"unsigned char configuration");\n#else\n_Static_assert((char)255==-1,"signed char configuration");\n#endif\n'
    pre += '#include "source/' + target["unit"] + '"\n'
    if target["project"] == "lua":
        code = '_Static_assert(UTF8BUFFSZ==8,"Lua destination extent");\nstatic int bg_actual(unsigned x,unsigned cap,unsigned char *dst){(void)cap;return luaO_utf8esc((char*)dst,(unsigned long)x);}\n'
    elif target["project"] == "libgrapheme":
        code = "static int bg_actual(unsigned x,unsigned cap,unsigned char *dst){return (int)grapheme_encode_utf8((uint_least32_t)x,(char*)dst,(size_t)cap);}\n"
    elif target["project"] == "utf8h":
        code = "static int bg_actual(unsigned x,unsigned cap,unsigned char *dst){void *p=utf8catcodepoint((void*)dst,(utf8_int32_t)x,(size_t)cap);return p?(int)((unsigned char*)p-dst):-1;}\n"
    else:
        code = target["wrapper"]
    return pre + code


PORTABLE = """
#ifdef BG_ESBMC
#define BG_ASSUME(p) __ESBMC_assume(p)
#define BG_ASSERT(p,t) __ESBMC_assert(p,t)
#else
#define BG_ASSUME(p) __CPROVER_assume(p)
#define BG_ASSERT(p,t) __CPROVER_assert(p,t)
#endif
"""


def harness(target, s, bad=False):
    pred = corrupt(s) if bad else s
    cap = "||".join("cap==" + str(c) + "U" for c in s["capacities"])
    source = (
        wrap(target)
        + emit(pred)
        + PORTABLE
        + """
unsigned nondet_u(void);unsigned char nondet_b(void);
void harness(void){unsigned x=nondet_u(),cap=nondet_u();
BG_ASSUME(x<=1114111U);BG_ASSUME("""
        + cap
        + """);
unsigned char actual[8],predicted[8];
for(unsigned i=0;i<8;i++){actual[i]=nondet_b();predicted[i]=actual[i];}
int r=bg_actual(x,cap,actual),p=bg_summary(x,cap,predicted);
BG_ASSERT(r==p,"target.return");
"""
    )
    for i in range(WIDTH):
        source += f'BG_ASSERT(actual[{i}]==predicted[{i}],"target.byte{i}");\n'
    return source + "}\n"


def native(target):
    return (
        wrap(target)
        + """
#include <stdio.h>
int main(void){uint32_t x,cap;unsigned char b[8];
while(fread(&x,4,1,stdin)==1){
 if(fread(&cap,4,1,stdin)!=1 || fread(b,8,1,stdin)!=1)return 2;
 int r=bg_actual(x,cap,b);
 if(fwrite(&r,4,1,stdout)!=1 || fwrite(b,8,1,stdout)!=1)return 3;
}return ferror(stdin)?4:0;}
"""
    )
