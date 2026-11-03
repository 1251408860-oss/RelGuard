"""Integrity and binary readers for the saved public evaluation records."""

from pathlib import Path
import hashlib
import json
import struct

DATA = Path(__file__).resolve().parent / "data"
ROW = struct.Struct("<II8B")
REQUEST = struct.Struct("<II8BII8BI")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for data in iter(lambda: f.read(1048576), b""):
            h.update(data)
    return h.hexdigest()


def verify_manifest(root=DATA):
    manifest = read(root / "manifest.sha256.json")
    for record in manifest["files"]:
        relative = Path(record["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Unsafe reference path")
        path = root / relative
        if not path.is_file() or digest(path) != record["sha256"]:
            raise ValueError("Reference record changed: " + record["path"])
    return {"files_checked": len(manifest["files"]), "all_hashes_match": True}


def tasks(cohort, root=DATA):
    return {x["target"]["id"]: x for x in read(root / cohort / "source_tasks.json")}


def native_records(folder, signed=False):
    cases = (folder / "cases.bin").read_bytes()
    a, b = [(folder / ("native_" + opt + ".stdout.bin")).read_bytes() for opt in ["O0", "O2"]]
    if a != b or len(cases) % 16 or len(a) * 16 != len(cases) * 12:
        raise ValueError("Incomplete or inconsistent native streams")
    result = {}
    output = struct.Struct("<i8B" if signed else "<I8B")
    for i in range(len(cases) // 16):
        state = cases[16 * i : 16 * i + 16]
        value = list(output.unpack_from(a, i * 12))
        if state in result and result[state] != value:
            raise ValueError("Conflicting native state")
        result[state] = value
    return result


def unpack_state(payload, field):
    x, cfg, *entry = ROW.unpack(payload)
    return {"x": x, field: cfg, "entry": entry}
