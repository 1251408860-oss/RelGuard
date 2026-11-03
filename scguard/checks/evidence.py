"""Receipt-bound per-field source-result admission."""

import re
from .. import _io as artifacts

EXPECTED = ["target.return"] + ["target.byte" + str(i) for i in range(8)]


def fields(folder, label, engine):
    unknown = {"completed_safe": False, "fields": ["UNKNOWN"] * 9}
    receipt = folder / (label + ".execution.json")
    if not receipt.exists():
        return unknown
    r = artifacts.read(receipt)
    for suffix, key in [(".stdout.bin", "stdout_sha256"), (".stderr.txt", "stderr_sha256")]:
        artifacts.need(
            artifacts.sha(folder / (label + suffix)) == r[key], "Raw field receipt identity"
        )
    if r["timed_out"]:
        return unknown
    if engine == "cbmc":
        if r["exit_code"] not in [0, 10]:
            return unknown
        try:
            d = artifacts.read(folder / (label + ".stdout.bin"))
        except Exception:
            return unknown
        props = [p for item in d for p in item.get("result", [])]
        wanted = [p for p in props if p.get("description") in EXPECTED]
        if len(wanted) != 9 or {p["description"] for p in wanted} != set(EXPECTED):
            return unknown
        if any((p["status"] != "SUCCESS" for p in props if p not in wanted)):
            return unknown
        failure = any((p["status"] == "FAILURE" for p in wanted))
        if r["exit_code"] != (10 if failure else 0) or [
            p["cProverStatus"] for p in d if "cProverStatus" in p
        ] != ["failure" if failure else "success"]:
            return unknown
        statuses = {p["description"]: p["status"] for p in wanted}
        if not all((s in ["SUCCESS", "FAILURE"] for s in statuses.values())):
            return unknown
        return {
            "completed_safe": True,
            "fields": ["SUPPORT" if statuses[n] == "SUCCESS" else "REFUTE" for n in EXPECTED],
        }
    if r["exit_code"] not in [0, 1]:
        return unknown
    text = "\n".join(
        ((folder / (label + s)).read_text(errors="replace") for s in [".stdout.bin", ".stderr.txt"])
    )
    props = re.findall(
        "^\\s+(PASSED|FAILED)\\s+\\[([^\\]]+)\\]\\s+line\\s+\\d+\\s+([^\\n]+)", text, re.M
    )
    wanted = [p for p in props if p[2].strip() in EXPECTED]
    total = re.findall("\\*\\* (\\d+) of (\\d+) properties failed, (\\d+) passed", text)
    if len(wanted) != 9 or {p[2].strip() for p in wanted} != set(EXPECTED) or len(total) != 1:
        return unknown
    failed, n, passed = map(int, total[0])
    if (
        n != len(props)
        or failed + passed != n
        or failed != sum((p[0] == "FAILED" for p in props))
        or any((p[0] != "PASSED" for p in props if p not in wanted))
    ):
        return unknown
    if (
        r["exit_code"] != (1 if failed else 0)
        or ("VERIFICATION FAILED" if failed else "VERIFICATION SUCCESSFUL") not in text
    ):
        return unknown
    statuses = {p[2].strip(): p[0] for p in wanted}
    return {
        "completed_safe": True,
        "fields": ["SUPPORT" if statuses[n] == "PASSED" else "REFUTE" for n in EXPECTED],
    }


def fast_value(spec, state):
    z = state["x"] | int.from_bytes(bytes(state["entry"]), "little") << 32 | 1 << 96
    bits = sum(
        ((r & z).bit_count() % 2 << i for i, r in enumerate(spec["rows"][str(state["cfg"])]))
    )
    return [bits & 4294967295] + list((bits >> 32).to_bytes(8, "little"))
