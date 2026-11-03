"""Run from the repository root with python -m examples.quickstart."""

from scguard.core import build_kernel, export_mixed_guard
from scguard.reference import tasks

catalogue = tasks("cross_family")
left = catalogue["miniz-3.1.0-crc32"]["model"]
right = catalogue["miniz-3.1.1-crc32"]["model"]
kernel = build_kernel(left, right, 8, 8, "return")
print("CRC return rank:", kernel["independent_check"]["rank"])
print("Free pair bits:", kernel["independent_check"]["free_pair_bits"])
print("Generated C guard characters:", len(export_mixed_guard(left, right)))
