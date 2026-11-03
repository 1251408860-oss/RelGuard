"""Current independent affine-emission and reduction-certificate checker."""

import ast
import re
import hashlib
import json


def need(x, s):
    if not x:
        raise ValueError(s)


def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


PARITY = """static unsigned af_parity(uint32_t v){
v^=v>>16;v^=v>>8;v^=v>>4;return (0x6996U>>(v&15U))&1U;}
"""

PACK = """uint32_t w0=x,w1=0,w2=0;
for(unsigned i=0;i<4;i++){w1|=(uint32_t)b[i]<<(8U*i);w2|=(uint32_t)b[i+4]<<(8U*i);}
"""


def check_reduction(original, system):
    need(
        type(system["rank"]) is int
        and type(system["inconsistent"]) is bool
        and (system["free_pair_bits"] is None or type(system["free_pair_bits"]) is int),
        "Strict rank and consistency types",
    )
    rows = list(original)
    need(all(type(v) is int and 0 <= v < 2**193 for v in rows), "Pair row schema")
    for op in system["operations"]:
        need(
            type(op) is list and len(op) == 3 and op[0] in ["swap", "xor"],
            "Elementary invertible operation",
        )
        kind, i, j = op
        need(
            type(i) is type(j) is int and 0 <= i < len(rows) and 0 <= j < len(rows) and i != j,
            "Distinct valid row indices",
        )
        if kind == "swap":
            rows[i], rows[j] = rows[j], rows[i]
        else:
            rows[i] ^= rows[j]
    need(rows == system["rows"], "Replayed row operation certificate")
    pivots = []
    for row in rows:
        coeff = row & ((1 << 192) - 1)
        if not coeff:
            continue
        pivot = (coeff & -coeff).bit_length() - 1
        need(not pivots or pivot > pivots[-1], "Increasing pivots")
        pivots.append(pivot)
    for i, pivot in enumerate(pivots):
        need(
            all(((r >> pivot) & 1) == (1 if j == i else 0) for j, r in enumerate(rows)),
            "Reduced pivot column",
        )
    need(all((r & ((1 << 192) - 1)) == 0 for r in rows[len(pivots) :]), "Zero-row suffix")
    inconsistent = any(r == 1 << 192 for r in rows)
    need(
        system["rank"] == len(pivots) and system["inconsistent"] == inconsistent,
        "Checked rank and consistency",
    )
    need(
        system["free_pair_bits"] == (None if inconsistent else 192 - len(pivots)),
        "Checked solution dimension",
    )
    return {
        "all_checks_passed": True,
        "rank": len(pivots),
        "inconsistent": inconsistent,
        "free_pair_bits": system["free_pair_bits"],
    }


def value(spec, state):
    bits = [(state["x"] // (2**j)) % 2 for j in range(32)]
    bits += [(state["entry"][i] // (2**j)) % 2 for i in range(8) for j in range(8)]
    out = []
    for row in spec["rows"][str(state["cfg"])]:
        out.append((row >> 96) ^ sum(bits[j] for j in range(96) if (row >> j) & 1) % 2)
    packed = sum(v * (2**j) for j, v in enumerate(out))
    return [packed % (2**32)] + list((packed >> 32).to_bytes(8, "little"))


C = 1 << 96


def constant(v):
    return [C if (v >> i) & 1 else 0 for i in range(32)]


def const_value(rows):
    if any(r not in [0, C] for r in rows):
        return None
    return sum((r == C) << i for i, r in enumerate(rows))


def expression(text):
    words = {"w" + str(w): [1 << (32 * w + i) for i in range(32)] for w in range(3)}
    node = ast.parse(re.sub(r"(0x[0-9a-fA-F]+|\d+)U\b", r"\1", text), mode="eval").body

    def convert(q):
        if isinstance(q, ast.Constant) and type(q.value) is int and 0 <= q.value < 2**32:
            return constant(q.value)
        if isinstance(q, ast.Name) and q.id in words:
            return words[q.id]
        if (
            isinstance(q, ast.Call)
            and isinstance(q.func, ast.Name)
            and q.func.id == "af_parity"
            and len(q.args) == 1
            and not q.keywords
        ):
            answer = 0
            for r in convert(q.args[0]):
                answer ^= r
            return [answer] + [0] * 31
        if isinstance(q, ast.BinOp):
            a, b = convert(q.left), convert(q.right)
            if isinstance(q.op, ast.BitXor):
                return [x ^ y for x, y in zip(a, b)]
            if isinstance(q.op, ast.BitAnd):
                va, vb = const_value(a), const_value(b)
                need(va is not None or vb is not None, "Only constant-masked affine AND")
                mask = va if va is not None else vb
                other = b if va is not None else a
                return [r if (mask >> i) & 1 else 0 for i, r in enumerate(other)]
            if isinstance(q.op, ast.BitOr):
                result = []
                for x, y in zip(a, b):
                    if x == y or y == 0:
                        result.append(x)
                    elif x == 0:
                        result.append(y)
                    elif x == C or y == C or x ^ y == C:
                        result.append(C)
                    else:
                        raise ValueError("Overlapping non-affine OR rejected")
                return result
            if isinstance(q.op, (ast.LShift, ast.RShift)):
                need(
                    isinstance(q.right, ast.Constant)
                    and type(q.right.value) is int
                    and 0 <= q.right.value < 32,
                    "Defined constant shift",
                )
                k = q.right.value
                return (
                    ([0] * k + a[: 32 - k]) if isinstance(q.op, ast.LShift) else (a[k:] + [0] * k)
                )
        raise ValueError("Unsupported affine C expression")

    return convert(node)


def qualify_parity():
    # Exact linear interpretation of each unsigned XOR/shift; only the
    # final four-bit lookup is enumerated (all 16 possibilities).
    rows = [1 << i for i in range(32)]
    for shift in [16, 8, 4]:
        rows = [r ^ (rows[i + shift] if i + shift < 32 else 0) for i, r in enumerate(rows)]
    total = 0
    for r in rows[:4]:
        total ^= r
    need(total == (1 << 32) - 1, "Fold retains every source bit exactly once")
    need(
        all(((0x6996 >> v) & 1) == v.bit_count() % 2 for v in range(16)),
        "Exhaustive final parity nibble",
    )
    return {
        "all_uint32_values": True,
        "symbolic_linear_fold": True,
        "final_lookup_inputs_exhaustively_checked": 16,
        "SMT_or_external_C_jobs": 0,
    }


def check_emission(folder):
    spec = read(folder / "contract.json")
    code = (folder / "summary.c").read_text()
    seal = read(folder / "candidate_seal.json")
    need(
        spec["schema"] == "affine-state-contract-v1"
        and spec["input_bits"] == spec["output_bits"] == 96
        and spec["configurations"] == list(range(9))
        and all(type(v) is int for v in spec["configurations"]),
        "Exact independent domain",
    )
    need(set(spec["rows"]) == set(map(str, range(9))), "Every configuration")
    for filename, key in [
        ("contract.json", "contract_sha256"),
        ("summary.c", "summary_sha256"),
        ("check.c", "check_sha256"),
    ]:
        need(sha(folder / filename) == seal[key], "Candidate seal " + filename)
    need(
        (folder / "check.c").read_text().count(code) == 1,
        "Exact emitted function in source harness",
    )
    prefix = (
        PARITY
        + "\nstatic uint32_t af_summary(uint32_t x,unsigned cfg,unsigned char *b){\n"
        + PACK
        + "\n"
    )
    need(
        code.startswith(prefix) and code.endswith("return 0U;}\n"),
        "Exact uint32 helper/data-pack kernel",
    )
    lines = code[len(prefix) : -len("return 0U;}\n")].splitlines()
    pos = 0
    checks = 0
    qualify_parity()
    for cfg in range(9):
        need(lines[pos] == "if(cfg==" + str(cfg) + "U){", "Exhaustive ordered config")
        pos += 1
        rows = spec["rows"][str(cfg)]
        need(
            len(rows) == 96 and all(type(r) is int and 0 <= r < 2**97 for r in rows),
            "Strict coefficient schema",
        )
        for word in range(3):
            q = re.fullmatch("uint32_t o" + str(word) + "=(.*);", lines[pos])
            need(q is not None, "Output word")
            pos += 1
            need(
                expression(q[1]) == rows[word * 32 : word * 32 + 32],
                "Exact symbolic emitted word coefficients",
            )
            checks += 1
        for j in range(8):
            need(
                lines[pos]
                == "b["
                + str(j)
                + "]=(unsigned char)(o"
                + str(1 + j // 4)
                + ">>"
                + str(8 * (j % 4))
                + "U);",
                "Byte extraction",
            )
            pos += 1
        need(lines[pos] == "return o0;}", "Return normalization")
        pos += 1
    need(pos == len(lines), "No unchecked statements")
    return {
        "all_checks_passed": True,
        "universal_uint32_word_checks": checks,
        "method": "exact restricted bit-polynomial interpretation",
        "parity_helper_symbolically_and_exhaustively_qualified": True,
        "general_C_frontend_certified": False,
        "SMT_queries": 0,
    }
