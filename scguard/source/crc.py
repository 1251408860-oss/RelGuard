"""CRC source obligations, composition and operational frame."""

from ..models import affine
from .. import _io as artifacts


def compose_check(spec):
    one = spec["rows"]["1"]
    identity = [1 << i for i in range(96)]
    artifacts.need(one[32:] == identity[32:], "One-byte object frame")
    allowed = (1 << 40) - 1 | 1 << 96
    artifacts.need(
        all((r & ~allowed == 0 for r in one[:32])), "Step return only uses seed and first byte"
    )
    current = [1 << i for i in range(32)]
    for n in range(9):
        artifacts.need(
            spec["rows"][str(n)] == current + identity[32:],
            "Full proposal equals iterated inferred step at length " + str(n),
        )
        new = []
        for row in one[:32]:
            value = row & 1 << 96
            for k in range(32):
                if row >> k & 1:
                    value ^= current[k]
            if n < 8:
                for bit in range(8):
                    if row >> 32 + bit & 1:
                        value ^= 1 << 32 + 8 * n + bit
            new.append(value)
        current = new
    return {
        "all_checks_passed": True,
        "all_lengths": list(range(9)),
        "source_step_not_handwritten_CRC_semantics": True,
        "requires_source_step_stream_bridge_and_operational_frame": True,
    }


def step_source(t, s):
    return affine.harness(t, s).replace("AF_ASSUME(cfg<9U);", "AF_ASSUME(cfg==1U);")


def stream_source(t):
    text = (
        affine.wrapper(t)
        + affine.PORTABLE
        + '\nvoid harness(void){uint32_t x=nondet_u();unsigned cfg=nondet_u();AF_ASSUME(cfg<9U);\n_Alignas(8) unsigned char actual[8],initial[8];\nfor(unsigned i=0;i<8;i++){actual[i]=nondet_b();initial[i]=actual[i];}\nuint32_t r=af_actual(x,cfg,actual),p=x;\nfor(unsigned i=0;i<cfg;i++){_Alignas(8) unsigned char one[8]={0};one[0]=initial[i];p=af_actual(p,1U,one);}\nAF_ASSERT(r==p,"target.return");\n'
    )
    for i in range(8):
        text += (
            "AF_ASSERT(actual["
            + str(i)
            + "]==initial["
            + str(i)
            + '],"target.byte'
            + str(i)
            + '");\n'
        )
    return text + "}\n"


def frame_source(t):
    text = (
        affine.wrapper(t)
        + '\nuint32_t nondet_u(void);unsigned char nondet_b(void);\nuint32_t af_pure(uint32_t x,unsigned cfg,unsigned char*b)\n__CPROVER_requires(cfg<9U)\n__CPROVER_requires(__CPROVER_is_fresh(b,8))\n__CPROVER_assigns()\n__CPROVER_ensures(__CPROVER_return_value<=UINT32_MAX)\n{return af_actual(x,cfg,b);}\nvoid harness(void){uint32_t x=nondet_u();unsigned cfg=nondet_u();__CPROVER_assume(cfg<9U);\n_Alignas(8) unsigned char b[8],before[8];for(unsigned i=0;i<8;i++){b[i]=nondet_b();before[i]=b[i];}\nuint32_t r=af_pure(x,cfg,b);\n__CPROVER_assert(r<=UINT32_MAX,"target.frame.return_type");\n'
    )
    for j in range(8):
        text += (
            "__CPROVER_assert(b["
            + str(j)
            + "]==before["
            + str(j)
            + '],"target.frame.byte'
            + str(j)
            + '");\n'
        )
    return text + '__CPROVER_assert(cfg>8U,"target.frame.nonvacuity_FALSE");}\n'


def enforced_step_source(t, s, corrupt=False):
    compose_check(s)
    expected = affine.word_expression(s["rows"]["1"], 0)
    helper = (
        affine.PARITY
        + "static uint32_t af_expected(uint32_t x,unsigned char byte){uint32_t w0=x,w1=byte,w2=0;return "
        + expected
        + ";}\n"
    )
    text = frame_source(t)
    pos = text.index("uint32_t af_pure(")
    text = text[:pos] + helper + text[pos:]
    rhs = "(af_expected(x,b[0])^1U)" if corrupt else "af_expected(x,b[0])"
    text = text.replace(
        "__CPROVER_ensures(__CPROVER_return_value<=UINT32_MAX)",
        "__CPROVER_ensures(__CPROVER_return_value<=UINT32_MAX)\n__CPROVER_ensures(cfg!=1U || __CPROVER_return_value=="
        + rhs
        + ")",
    )
    return text
