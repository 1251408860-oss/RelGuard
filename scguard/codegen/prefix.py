"""Checked prefix emission for bounded integer models."""

from ..checks import model as basecheck
from .. import _io as artifacts


def emit(s):
    basecheck.model(s)
    lines = ["static uint32_t rf_summary(uint32_t x,unsigned cfg,unsigned char*b){", "(void)x;"]
    for cfg in range(9):
        cell = s["cells"][str(cfg)]
        coeff = cell["coefficients"]
        artifacts.need(coeff[0] == 0, "Prefix emitter currently uses only bytes")
        low = [v & 65535 for v in coeff[1:]]
        high = [v >> 16 for v in coeff[1:]]
        used = max([j + 1 for j in range(8) if low[j] or high[j]] or [0])
        artifacts.need(low == [1] * used + [0] * (8 - used), "Unit prefix feature coefficients")
        delta = [high[j] - (high[j + 1] if j + 1 < 8 else 0) for j in range(used)]
        artifacts.need(all((v >= 0 for v in delta)), "Nonnegative discrete differences")
        lo = cell["base"] & 65535
        hi = (cell["base"] >> 16) - lo * sum(delta)
        artifacts.need(hi >= 0, "Nonnegative factored constant")
        lines += [
            "if(cfg==" + str(cfg) + "U){",
            "uint32_t lo=" + str(lo) + "U,hi=" + str(hi) + "U;",
        ]
        for j, d in enumerate(delta):
            lines += ["lo+=(uint32_t)b[" + str(j) + "];"]
            if d:
                lines += ["hi+=" + ("lo" if d == 1 else str(d) + "U*lo") + ";"]
        lines += ["return (hi<<16U)|lo;}"]
    return "\n".join(lines + ["return 0U;}"]) + "\n"
