"""Public model, guard and source-obligation interfaces."""

from .models import writer, affine, typed as mixed
from .checks import writer as writer_check, affine as certificate, model as mixed_check
from .checks import prefix as prefix_check, evidence as field_reader
from .codegen import prefix
from .codegen.writer import export_guard as export_writer_guard
from .source import crc, arithmetic

OBSERVERS = ["return", "first4", "last4", "buffer8", "full"]
FIELDS = {
    "return": [0],
    "first4": [1, 2, 3, 4],
    "last4": [5, 6, 7, 8],
    "buffer8": list(range(1, 9)),
    "full": list(range(9)),
}
MASKS = {"return": 1, "first4": 30, "last4": 480, "buffer8": 510, "full": 511}


def validate_model(model):
    if model.get("schema") == "bit-projection-contract-v1":
        return writer.validate(model)
    if model.get("schema") == "affine-state-contract-v1":
        return affine.validate(model)
    mixed_check.model(model)
    return model


def model_value(model, state):
    if model.get("schema") == "bit-projection-contract-v1":
        return writer_check.model_value(model, state)
    return mixed.value(model, state)


def valid_state(state):
    return (
        type(state) is dict
        and set(state) == {"x", "cfg", "entry"}
        and type(state["x"]) is int
        and 0 <= state["x"] <= 0xFFFFFFFF
        and type(state["cfg"]) is int
        and 0 <= state["cfg"] <= 8
        and type(state["entry"]) is list
        and len(state["entry"]) == 8
        and all(type(v) is int and 0 <= v <= 255 for v in state["entry"])
    )


def decide_model(left, right, a, b, observer):
    """Evaluate model equality; source admission is an input of the full pipeline."""
    left_writer = left.get("schema") == "bit-projection-contract-v1"
    right_writer = right.get("schema") == "bit-projection-contract-v1"
    if left_writer != right_writer:
        return "UNKNOWN"
    valid_a = writer.valid_input(a, left["capacities"]) if left_writer else valid_state(a)
    valid_b = writer.valid_input(b, right["capacities"]) if right_writer else valid_state(b)
    if type(observer) is not str or observer not in FIELDS or not valid_a or not valid_b:
        return "UNKNOWN"
    av, bv = model_value(left, a), model_value(right, b)
    return "SUPPORT" if all(av[j] == bv[j] for j in FIELDS[observer]) else "REFUTE"


def affine_projection(model, observer):
    if model.get("schema") == "bit-projection-contract-v1":
        return None
    if model.get("schema") == "affine-state-contract-v1":
        return model
    if observer not in {"first4", "last4", "buffer8"}:
        return None
    if model["post_bytes"] != "identity":
        raise ValueError("The byte projection requires an admitted identity postcondition")
    return {
        "schema": "affine-state-contract-v1",
        "input_bits": 96,
        "output_bits": 96,
        "configurations": list(range(9)),
        "rows": {str(c): [0] * 32 + [1 << (32 + i) for i in range(64)] for c in range(9)},
    }


def build_kernel(left, right, ca, cb, observer):
    if type(ca) is not int or type(cb) is not int or not 0 <= ca <= 8 or not 0 <= cb <= 8:
        raise ValueError("Configurations must be integers in 0..8")
    if type(observer) is not str or observer not in OBSERVERS:
        raise ValueError("Unknown observer")
    a, b = affine_projection(left, observer), affine_projection(right, observer)
    if a is None or b is None:
        raise ValueError("This observation uses a typed integer or ordered predicate")
    original = affine.equations(a, b, ca, cb, observer)
    system = affine.reduce_system(original)
    check = certificate.check_reduction(original, system)
    return {"original_rows": original, "system": system, "independent_check": check}


KERNEL = """int af_guard(uint32_t xa,unsigned ca,const unsigned char*a,uint32_t xb,unsigned cb,const unsigned char*b,unsigned obs){
if(!a||!b||ca>8U||cb>8U||obs>4U)return 0;
unsigned char left[8],right[8];for(unsigned i=0;i<8;i++){left[i]=a[i];right[i]=b[i];}
uint32_t ra=rf_left(xa,ca,left),rb=rf_right(xb,cb,right);int equal=1;
if(obs==0U||obs==4U)equal=ra==rb;
unsigned start=obs==2U?4U:0U,end=obs==1U?4U:8U;
if(obs!=0U)for(unsigned i=start;i<end;i++)if(left[i]!=right[i])equal=0;
return equal?1:2;}
"""


def export_mixed_guard(a, b):
    validate_model(a)
    validate_model(b)
    return (
        "#include <stdint.h>\n#include <limits.h>\n"
        '_Static_assert(CHAR_BIT==8&&sizeof(uint32_t)==4,"ABI");\n'
        + mixed.emit(a, "rf_left")
        + mixed.emit(b, "rf_right", with_parity=False)
        + KERNEL
    )


def export_guard(left, right):
    """Export the current guard for either the writer or cross-family grammar."""
    validate_model(left)
    validate_model(right)
    is_writer = [m.get("schema") == "bit-projection-contract-v1" for m in [left, right]]
    if all(is_writer):
        return export_writer_guard(left, right)
    if any(is_writer):
        raise ValueError("Both models must use compatible observer and return conventions")
    return export_mixed_guard(left, right)


def source_harness(task, model, route="direct"):
    """Emit obligations. A model checker must establish them before admission."""
    validate_model(model)
    if model.get("schema") == "bit-projection-contract-v1":
        if route != "direct":
            raise ValueError("Writer harness uses the original-source route")
        return writer.harness(task, model)
    if route == "direct":
        return (
            affine.harness(task, model)
            if model.get("schema") == "affine-state-contract-v1"
            else mixed.harness(task, model)
        )
    if route == "typed-conditional" and task["api"] == "memcmp_sign":
        return mixed.harness(task, model, normalized=True)
    if route == "integer-prefix" and task["api"] == "adler32":
        code = prefix.emit(model)
        prefix_check.check(model, code)
        return (
            mixed.harness(task, model)
            .replace(mixed.emit(model), code)
            .replace('#include "source/miniz.c"', '#include "reduced/miniz.c"')
        )
    if task.get("api") == "crc32":
        if route == "crc-step":
            return crc.step_source(task, model)
        if route == "crc-stream":
            return crc.stream_source(task)
        if route == "crc-frame":
            return crc.frame_source(task)
        if route == "crc-dfcc-step":
            return crc.enforced_step_source(task, model)
    if route == "adler-ranges" and task.get("api") == "adler32":
        return arithmetic.range_driver(task)
    if route == "typed-bridge" and task.get("api") == "memcmp_sign":
        return mixed.bridge(task)
    raise ValueError("Route does not apply to this task")
