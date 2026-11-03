"""Independent writer-emission and model checker."""

from pathlib import Path
import ast
import hashlib
import json
import re
import z3

MAX_X = 1114111

EXPECTED = {"target.return"} | {"target.byte" + str(i) for i in range(8)}


def need(x, s):
    if not x:
        raise ValueError(s)


def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_expr(text, x, initial):
    node = ast.parse(re.sub(r"(\d+)U\b", r"\1", text), mode="eval").body

    def convert(q):
        if isinstance(q, ast.Constant) and type(q.value) is int and 0 <= q.value < 2**32:
            return z3.BitVecVal(q.value, 32)
        if isinstance(q, ast.Name) and q.id in ["x", "initial"]:
            return x if q.id == "x" else initial
        if isinstance(q, ast.UnaryOp) and isinstance(q.op, ast.Invert):
            return ~convert(q.operand)
        if isinstance(q, ast.BinOp):
            a, b = convert(q.left), convert(q.right)
            if isinstance(q.op, ast.BitAnd):
                return a & b
            if isinstance(q.op, ast.BitOr):
                return a | b
            if isinstance(q.op, (ast.LShift, ast.RShift)):
                need(
                    isinstance(q.right, ast.Constant)
                    and type(q.right.value) is int
                    and 0 <= q.right.value < 32,
                    "Fixed defined shift",
                )
                return a << b if isinstance(q.op, ast.LShift) else z3.LShR(a, b)
        raise ValueError("Unsupported generated C expression")

    return convert(node)


def parse_emitted(text):
    lines = text.splitlines()
    need(
        lines[0] == "static int bg_summary(unsigned x,unsigned cap,unsigned char *dst){",
        "Emitted signature",
    )
    need(lines[-1] == "return 0;}", "Emitted function end")
    result = {}
    pos = 1
    while pos < len(lines) - 1:
        group = lines[pos]
        need(re.fullmatch(r"if\(cap==\d+U(?:\|\|cap==\d+U)*\)\{", group), "Capacity dispatch")
        caps = list(map(int, re.findall(r"cap==(\d+)U", group)))
        pos += 1
        cells = []
        start = 0
        while pos < len(lines) - 1 and lines[pos] != "}":
            q = re.fullmatch(r"if\(x<=(\d+)U\)\{", lines[pos])
            need(q is not None, "Input branch")
            hi = int(q[1])
            pos += 1
            exprs = {}
            while pos < len(lines) and lines[pos].startswith("{unsigned initial="):
                q = re.fullmatch(
                    r"\{unsigned initial=dst\[(\d)\];dst\[(\d)\]=\(unsigned char\)\((.*)\);\}",
                    lines[pos],
                )
                need(q is not None and q[1] == q[2] and int(q[1]) < 8, "Own-byte assignment")
                i = int(q[1])
                need(i not in exprs, "Unique byte assignment")
                exprs[i] = q[3]
                pos += 1
            q = re.fullmatch(r"return (-?\d+);\}", lines[pos])
            need(q is not None, "Constant return")
            need(start <= hi <= MAX_X, "Ordered intervals")
            cells.append({"lo": start, "hi": hi, "ret": int(q[1]), "exprs": exprs})
            start = hi + 1
            pos += 1
        need(
            start == MAX_X + 1 and pos < len(lines) - 1 and lines[pos] == "}",
            "Complete group cover",
        )
        pos += 1
        for cap in caps:
            need(0 <= cap <= 8 and cap not in result, "Capacity uniqueness")
            result[cap] = cells
    return result


def check_emission(folder):
    spec = read(folder / "contract.json")
    code = (folder / "summary.c").read_text()
    need(
        spec["schema"] == "bit-projection-contract-v1"
        and spec["domain"] == [0, MAX_X]
        and spec["bytes"] == 8,
        "Independent summary domain",
    )
    actual = parse_emitted(code)
    need(set(actual) == set(spec["capacities"]), "Independent capacity cover")
    checked = 0
    for cap, cells in actual.items():
        saved = spec["cells"][str(cap)]
        need(len(cells) == len(saved), "Cell count")
        for a, b in zip(cells, saved):
            need(
                all(type(b[k]) is int and a[k] == b[k] for k in ["lo", "hi", "ret"]),
                "Cell bounds and return",
            )
            need(
                len(b["features"]) == 64
                and all(type(t) is int and 0 <= t < 46 for t in b["features"]),
                "Feature schema",
            )
            x = z3.BitVec("q", 32)
            initial_byte = z3.BitVec("initial_byte", 8)
            initial = z3.ZeroExt(24, initial_byte)
            differences = []
            for i in range(8):
                expr = parse_expr(a["exprs"][i], x, initial) if i in a["exprs"] else initial
                expected = z3.BitVecVal(0, 32)
                for bit, t in enumerate(b["features"][i * 8 : i * 8 + 8]):
                    if t < 2:
                        v = z3.BitVecVal(t, 32)
                    elif t < 23:
                        v = z3.LShR(x, t - 2) & 1
                    elif t < 44:
                        v = (~z3.LShR(x, t - 23)) & 1
                    elif t == 44:
                        v = z3.LShR(initial, bit) & 1
                    else:
                        v = (~z3.LShR(initial, bit)) & 1
                    expected |= v << bit
                differences.append((expr & 255) != expected)
            solver = z3.Solver()
            solver.set(timeout=10000)
            solver.add(z3.UGE(x, a["lo"]), z3.ULE(x, a["hi"]), z3.Or(differences))
            need(
                solver.check() == z3.unsat,
                "C emission and model must agree for all inputs/entry bytes",
            )
            checked += 8
    harness = (folder / "check.c").read_text()
    need(harness.count(code) == 1, "Checked C contains exact certified emission")
    seal = read(folder / "candidate_seal.json")
    for filename, key in [
        ("contract.json", "contract_sha256"),
        ("summary.c", "summary_sha256"),
        ("check.c", "check_sha256"),
    ]:
        need(sha(folder / filename) == seal[key], "Sealed candidate " + filename)
    return {
        "all_checks_passed": True,
        "symbolic_byte_obligations": checked,
        "Z3_version": z3.get_version_string(),
        "arbitrary_input_and_entry_byte_not_enumerated": True,
        "general_C_frontend_certified": False,
    }


def source_verdict(folder, label, engine):
    receipt = read(folder / (label + ".execution.json"))
    for suffix, key in [(".stdout.bin", "stdout_sha256"), (".stderr.txt", "stderr_sha256")]:
        need(sha(folder / (label + suffix)) == receipt[key], "Independent raw output hash")
    if receipt["timed_out"]:
        return "UNKNOWN"
    if engine == "cbmc":
        if receipt["exit_code"] not in [0, 10]:
            return "UNKNOWN"
        try:
            raw = read(folder / (label + ".stdout.bin"))
        except (ValueError, UnicodeError):
            return "UNKNOWN"
        props = [p for item in raw for p in item.get("result", [])]
        target = [p for p in props if p.get("description") in EXPECTED]
        if len(target) != 9 or set(p["description"] for p in target) != EXPECTED:
            return "UNKNOWN"
        if any(p["status"] != "SUCCESS" for p in props if p not in target):
            return "UNKNOWN"
        finals = [p["cProverStatus"] for p in raw if "cProverStatus" in p]
        if (
            all(p["status"] == "SUCCESS" for p in target)
            and finals == ["success"]
            and receipt["exit_code"] == 0
        ):
            return "SUPPORT"
        if (
            any(p["status"] == "FAILURE" for p in target)
            and finals == ["failure"]
            and receipt["exit_code"] == 10
        ):
            return "REFUTE"
    else:
        if receipt["exit_code"] not in [0, 1]:
            return "UNKNOWN"
        body = "\n".join(
            (folder / (label + suffix)).read_text(errors="replace")
            for suffix in [".stdout.bin", ".stderr.txt"]
        )
        props = re.findall(
            r"^\s+(PASSED|FAILED)\s+\[([^\]]+)\]\s+line\s+\d+\s+([^\n]+)", body, re.M
        )
        target = [p for p in props if p[2].strip() in EXPECTED]
        totals = re.findall(r"\*\* (\d+) of (\d+) properties failed, (\d+) passed", body)
        if len(target) != 9 or set(p[2].strip() for p in target) != EXPECTED or len(totals) != 1:
            return "UNKNOWN"
        fail, n, passed = map(int, totals[0])
        if len(props) != n or fail + passed != n or fail != sum(p[0] == "FAILED" for p in props):
            return "UNKNOWN"
        if any(p[0] != "PASSED" for p in props if p not in target):
            return "UNKNOWN"
        if (
            all(p[0] == "PASSED" for p in target)
            and receipt["exit_code"] == 0
            and "VERIFICATION SUCCESSFUL" in body
        ):
            return "SUPPORT"
        if (
            any(p[0] == "FAILED" for p in target)
            and receipt["exit_code"] == 1
            and "VERIFICATION FAILED" in body
        ):
            return "REFUTE"
    return "UNKNOWN"


def model_value(s, state):
    # Separate implementation: per-byte arithmetic, no generator imports.
    x, cap = state["x"], state["cap"]
    cell = None
    for q in s["cells"][str(cap)]:
        if q["lo"] <= x <= q["hi"]:
            cell = q
            break
    need(cell is not None, "Input covered")
    result = [cell["ret"]]
    for byte in range(8):
        value = 0
        for k in range(8):
            token = cell["features"][byte * 8 + k]
            if token == 0:
                bit = 0
            elif token == 1:
                bit = 1
            elif token <= 22:
                bit = (x // (2 ** (token - 2))) % 2
            elif token <= 43:
                bit = 1 - (x // (2 ** (token - 23))) % 2
            elif token == 44:
                bit = (state["entry"][byte] // (2**k)) % 2
            else:
                bit = 1 - (state["entry"][byte] // (2**k)) % 2
            value += bit * (2**k)
        result.append(value)
    return result
