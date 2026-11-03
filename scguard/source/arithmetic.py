"""Arithmetic range obligations and checked source normalization."""

from ..models import affine
from .. import _io as artifacts

RANGE_TARGETS = ["range.block_initial", "range.low_before_mod", "range.high_before_mod"] + [
    "target.byte" + str(i) for i in range(8)
]

BLOCK = "size_t block_len = buf_len % 5552;"

MOD = "s1 %= 65521U, s2 %= 65521U;"


def instrument(source):
    artifacts.need(source.count(BLOCK) == source.count(MOD) == 1, "Unique arithmetic locations")
    return source.replace(
        BLOCK, 'AF_ASSERT(buf_len<5552U,"range.block_initial");\n        ' + BLOCK
    ).replace(
        MOD,
        'AF_ASSERT(s1<65521U,"range.low_before_mod");\n            AF_ASSERT(s2<65521U,"range.high_before_mod");\n            '
        + MOD,
    )


def reduce_source(source):
    return source.replace(BLOCK, "size_t block_len = buf_len;").replace(MOD, "(void)s1, (void)s2;")


def translation_check(source, annotated, reduced):
    q = "size_t block_len = buf_len % 5552;"
    r = "s1 %= 65521U, s2 %= 65521U;"
    artifacts.need(
        source.count(q) == source.count(r) == 1
        and "mz_uint32 i, s1 = (mz_uint32)(adler & 0xffff), s2 = (mz_uint32)(adler >> 16);"
        in source,
        "Declared unsigned source arithmetic",
    )
    expected = source.replace(
        q, 'AF_ASSERT(buf_len<5552U,"range.block_initial");\n        ' + q
    ).replace(
        r,
        'AF_ASSERT(s1<65521U,"range.low_before_mod");\n            AF_ASSERT(s2<65521U,"range.high_before_mod");\n            '
        + r,
    )
    artifacts.need(
        annotated == expected,
        "Only ghost range assertions added; all original computations retained",
    )
    artifacts.need(
        reduced
        == source.replace(q, "size_t block_len = buf_len;").replace(r, "(void)s1, (void)s2;"),
        "Only three checked unsigned remainder operations removed",
    )
    return {
        "all_checks_passed": True,
        "conditional_on_all_original_range_targets_and_unsigned_identity": True,
        "remainder_rule": "For unsigned a and positive d, 0 <= a < d implies a % d = a",
        "C11_sections": ["6.5.5", "6.5.16.2"],
        "moduli_from_original_source": [5552, 65521],
        "original_loop_updates_and_return_unchanged": True,
        "general_C_normalizer_claimed": False,
    }


def range_driver(t):
    return (
        "#include <stdint.h>\n"
        + affine.PORTABLE
        + affine.wrapper(t).replace('#include "source/miniz.c"', '#include "instrumented/miniz.c"')
        + "\nvoid harness(void){uint32_t x=nondet_u();unsigned cfg=nondet_u();AF_ASSUME(cfg<9U);\n_Alignas(8) unsigned char actual[8],before[8];\nfor(unsigned i=0;i<8;i++){actual[i]=nondet_b();before[i]=actual[i];}\n(void)af_actual(x,cfg,actual);\n"
        + "".join(
            (
                "AF_ASSERT(actual["
                + str(j)
                + "]==before["
                + str(j)
                + '],"target.byte'
                + str(j)
                + '");\n'
                for j in range(8)
            )
        )
        + "}\n"
    )


def leaf(unsafe=False):
    text = (
        "#include <stdint.h>\n"
        + affine.PORTABLE
        + "void harness(void){uint32_t a=nondet_u();uint64_t n=nondet_u();\n"
    )
    if not unsafe:
        text += "AF_ASSUME(a<65521U);AF_ASSUME(n<9U);\n"
    return (
        text
        + 'AF_ASSERT(a%65521U==a,"lemma.uint32_mod");\nAF_ASSERT(n%5552U==n,"lemma.uint64_mod");}\n'
    )
