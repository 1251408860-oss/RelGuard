"""Shared file, hash and receipt utilities."""

from datetime import datetime, timezone
import hashlib
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def now():
    return datetime.now(timezone.utc).isoformat()


def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1048576), b""):
            h.update(b)
    return h.hexdigest()
