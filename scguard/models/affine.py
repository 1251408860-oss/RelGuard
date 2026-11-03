"""Affine state models, basis inference and relational elimination."""

from copy import deepcopy
import random
import struct

N = 96

CONSTANT = 1 << N

TARGETS = ["target.return"] + ["target.byte" + str(i) for i in range(8)]

OBSERVERS = {
    "return": list(range(32)),
    "first4": list(range(32, 64)),
    "last4": list(range(64, 96)),
    "buffer8": list(range(32, 96)),
    "full": list(range(96)),
}

PROFILES = [
    (0, 0, 0),
    (4, 0, 4),
    (4, 4, 0),
    (6, 0, 2),
    (6, 2, 0),
    (8, 0, 0),
    (1, 3, 4),
    (3, 1, 2),
    (3, 2, 1),
]

ROW = struct.Struct("<II8B")

OUTPUT = struct.Struct("<I8B")


def need(ok, text):
    if not ok:
        raise ValueError(text)


def state(z, cfg):
    return {"x": z & 0xFFFFFFFF, "cfg": cfg, "entry": list((z >> 32).to_bytes(8, "little"))}


def vector(s):
    return s["x"] | (int.from_bytes(bytes(s["entry"]), "little") << 32)


def output_vector(row):
    return row[0] | (int.from_bytes(bytes(row[1:]), "little") << 32)


def split_output(z):
    return [z & 0xFFFFFFFF] + list((z >> 32).to_bytes(8, "little"))


def dataset():
    rows = []
    index = {}
    basis = {}
    rng = random.Random(2026110203)

    def add(s):
        key = (s["x"], s["cfg"], tuple(s["entry"]))
        if key not in index:
            index[key] = len(rows)
            rows.append(s)
        return index[key]

    for cfg in range(9):
        basis[str(cfg)] = [add(state(z, cfg)) for z in [0] + [1 << i for i in range(N)]]
    held = []
    for cfg in range(9):
        for z in [2**N - 1, 0x555555555555555555555555, 0xAAAAAAAAAAAAAAAAAAAAAAAA] + [
            rng.getrandbits(N) for _ in range(512)
        ]:
            held.append(add(state(z, cfg)))
    return {
        "cases": rows,
        "basis_case_ids": basis,
        "held_out_case_ids": held,
        "seed": 2026110203,
        "input_bits": N,
        "basis_is_candidate_construction_not_source_proof": True,
    }


def write_cases(path, states):
    with path.open("wb") as f:
        for s in states:
            f.write(ROW.pack(s["x"], s["cfg"], *s["entry"]))


def observations(body, count):
    need(len(body) == count * 12, "Complete uint32/eight-byte native stream")
    return [list(OUTPUT.unpack_from(body, 12 * i)) for i in range(count)]


def learn(data, values):
    cells = {}
    for cfg, ids in data["basis_case_ids"].items():
        need(len(ids) == 97, "Origin and 96 unit vectors")
        origin = output_vector(values[ids[0]])
        rows = [CONSTANT if (origin >> j) & 1 else 0 for j in range(N)]
        for i, identity in enumerate(ids[1:]):
            column = output_vector(values[identity]) ^ origin
            for j in range(N):
                if (column >> j) & 1:
                    rows[j] |= 1 << i
        cells[cfg] = rows
    return validate(
        {
            "schema": "affine-state-contract-v1",
            "input_bits": 96,
            "output_bits": 96,
            "configurations": list(range(9)),
            "rows": cells,
        }
    )


def validate(s):
    need(
        type(s) is dict
        and set(s) == {"schema", "input_bits", "output_bits", "configurations", "rows"},
        "Exact affine schema",
    )
    need(
        s["schema"] == "affine-state-contract-v1"
        and type(s["input_bits"]) is int
        and s["input_bits"] == 96
        and type(s["output_bits"]) is int
        and s["output_bits"] == 96,
        "Affine dimensions",
    )
    need(
        s["configurations"] == list(range(9)) and all(type(x) is int for x in s["configurations"]),
        "Exact configuration cube",
    )
    need(set(s["rows"]) == set(map(str, range(9))), "Every configuration")
    for rows in s["rows"].values():
        need(
            type(rows) is list
            and len(rows) == 96
            and all(type(x) is int and 0 <= x < 2**97 for x in rows),
            "96 strict coefficient rows",
        )
    return s


def evaluate(s, z, cfg):
    need(
        type(z) is int and 0 <= z < 2**96 and type(cfg) is int and cfg in range(9), "Declared cube"
    )
    packed = z | CONSTANT
    out = 0
    for i, row in enumerate(s["rows"][str(cfg)]):
        out |= ((row & packed).bit_count() % 2) << i
    return out


PARITY = """static unsigned af_parity(uint32_t v){
v^=v>>16;v^=v>>8;v^=v>>4;return (0x6996U>>(v&15U))&1U;}
"""


def bit_expression(row):
    mask = row & (CONSTANT - 1)
    terms = []
    if mask.bit_count() == 1:
        bit = mask.bit_length() - 1
        terms.append("((w" + str(bit // 32) + ">>" + str(bit % 32) + "U)&1U)")
    else:
        for word in range(3):
            chunk = (mask >> (word * 32)) & 0xFFFFFFFF
            if chunk:
                terms.append("af_parity(w" + str(word) + "&0x" + format(chunk, "08x") + "U)")
    if row & CONSTANT:
        terms.append("1U")
    return "(" + "^".join(terms) + ")" if terms else "0U"


def word_expression(rows, word):
    subset = rows[word * 32 : word * 32 + 32]
    for source in range(3):
        if subset == [1 << (source * 32 + i) for i in range(32)]:
            return "w" + str(source)
    terms = [
        ("(" + bit_expression(row) + "<<" + str(i) + "U)") for i, row in enumerate(subset) if row
    ]
    return "|".join(terms) if terms else "0U"


PACK = """uint32_t w0=x,w1=0,w2=0;
for(unsigned i=0;i<4;i++){w1|=(uint32_t)b[i]<<(8U*i);w2|=(uint32_t)b[i+4]<<(8U*i);}
"""


def emit(s, name="af_summary"):
    validate(s)
    lines = [
        PARITY,
        "static uint32_t " + name + "(uint32_t x,unsigned cfg,unsigned char *b){",
        PACK,
    ]
    for cfg in range(9):
        rows = s["rows"][str(cfg)]
        lines += ["if(cfg==" + str(cfg) + "U){"]
        for word in range(3):
            lines += ["uint32_t o" + str(word) + "=" + word_expression(rows, word) + ";"]
        for j in range(8):
            lines += [
                "b["
                + str(j)
                + "]=(unsigned char)(o"
                + str(1 + j // 4)
                + ">>"
                + str(8 * (j % 4))
                + "U);"
            ]
        lines += ["return o0;}"]
    return "\n".join(lines + ["return 0U;}"]) + "\n"


def wrapper(t):
    pre = """#include <stdint.h>
#include <stddef.h>
#include <limits.h>
_Static_assert(CHAR_BIT==8 && sizeof(uint32_t)==4 && sizeof(void*)==8,"ABI");
"""
    if t["project"] == "miniz":
        pre += """#define MINIZ_NO_ARCHIVE_APIS
#define MINIZ_NO_ZLIB_APIS
#define MINIZ_NO_ZLIB_COMPATIBLE_NAMES
#include "source/miniz.c"
"""
        call = (
            "mz_crc32((mz_ulong)x,b,(size_t)cfg)"
            if t["api"] == "crc32"
            else "mz_adler32((mz_ulong)1,b,(size_t)cfg)"
        )
        pre += (
            "static uint32_t af_actual(uint32_t x,unsigned cfg,unsigned char*b){(void)x;return (uint32_t)"
            + call
            + ";}\n"
        )
    elif t["project"] == "musl":
        pre += (
            """#define memcpy af_upstream_memcpy
#define memmove af_upstream_memmove
#define memcmp af_upstream_memcmp
#include "source/src/string/memcpy.c"
#include "source/src/string/memmove.c"
#include "source/src/string/memcmp.c"
#undef memcpy
#undef memmove
#undef memcmp
static const unsigned af_profiles[9][3]={"""
            + ",".join("{" + ",".join(map(str, p)) + "}" for p in PROFILES)
            + """};
static uint32_t af_actual(uint32_t x,unsigned cfg,unsigned char*b){
(void)x;unsigned n=af_profiles[cfg][0],src=af_profiles[cfg][1],dst=af_profiles[cfg][2];
"""
        )
        if t["api"] == "memmove":
            pre += "void*p=af_upstream_memmove(b+dst,b+src,n);return (uint32_t)((unsigned char*)p-b);}\n"
        else:
            pre += "int v=af_upstream_memcmp(b+src,b+dst,n);return v<0?UINT32_MAX:v>0?1U:0U;}\n"
    else:
        pre += t["synthetic_wrapper"]
    return pre


PORTABLE = """
#ifdef BG_ESBMC
#define AF_ASSUME(p) __ESBMC_assume(p)
#define AF_ASSERT(p,n) __ESBMC_assert(p,n)
#else
#define AF_ASSUME(p) __CPROVER_assume(p)
#define AF_ASSERT(p,n) __CPROVER_assert(p,n)
#endif
uint32_t nondet_u(void);unsigned char nondet_b(void);
"""


def harness(t, s, tamper=False):
    if tamper:
        s = deepcopy(s)
        s["rows"]["0"][0] ^= CONSTANT
    text = (
        wrapper(t)
        + emit(s)
        + PORTABLE
        + """
void harness(void){uint32_t x=nondet_u();unsigned cfg=nondet_u();AF_ASSUME(cfg<9U);
_Alignas(8) unsigned char actual[8],predicted[8];
for(unsigned i=0;i<8;i++){actual[i]=nondet_b();predicted[i]=actual[i];}
uint32_t r=af_actual(x,cfg,actual),p=af_summary(x,cfg,predicted);
AF_ASSERT(r==p,"target.return");
"""
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


def native(t):
    return (
        wrapper(t)
        + """
#include <stdio.h>
int main(void){uint32_t x,cfg;_Alignas(8) unsigned char b[8];
while(fread(&x,4,1,stdin)==1){if(fread(&cfg,4,1,stdin)!=1||fread(b,8,1,stdin)!=1||cfg>8)return 2;
uint32_t r=af_actual(x,cfg,b);if(fwrite(&r,4,1,stdout)!=1||fwrite(b,8,1,stdout)!=1)return 3;
}return ferror(stdin)?4:0;}
"""
    )


def equations(a, b, ca, cb, observer):
    validate(a)
    validate(b)
    need(observer in OBSERVERS, "Declared projection")
    rows = []
    for bit in OBSERVERS[observer]:
        left, right = a["rows"][str(ca)][bit], b["rows"][str(cb)][bit]
        rows.append(
            (left & (CONSTANT - 1))
            | ((right & (CONSTANT - 1)) << 96)
            | (((left >> 96) ^ (right >> 96)) << 192)
        )
    return rows


def reduce_system(original):
    rows = list(original)
    ops = []
    pivot = 0
    for col in range(192):
        found = next((j for j in range(pivot, len(rows)) if (rows[j] >> col) & 1), None)
        if found is None:
            continue
        if found != pivot:
            rows[pivot], rows[found] = rows[found], rows[pivot]
            ops.append(["swap", pivot, found])
        for j in range(len(rows)):
            if j != pivot and (rows[j] >> col) & 1:
                rows[j] ^= rows[pivot]
                ops.append(["xor", j, pivot])
        pivot += 1
        if pivot == len(rows):
            break
    inconsistent = any(r == 1 << 192 for r in rows)
    return {
        "rows": rows,
        "operations": ops,
        "rank": pivot,
        "inconsistent": inconsistent,
        "free_pair_bits": None if inconsistent else 192 - pivot,
    }


def solution(system, rng):
    need(not system["inconsistent"], "Consistent guard")
    z = rng.getrandbits(192)
    for row in system["rows"]:
        coeff = row & ((1 << 192) - 1)
        if not coeff:
            continue
        pivot = (coeff & -coeff).bit_length() - 1
        required = (row >> 192) ^ ((coeff & z).bit_count() % 2)
        z ^= required << pivot
    return z
