import copy
import hashlib
import importlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scguard import core
from scguard.reference import DATA, read, tasks


class CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = tasks("cross_family")
        cls.writers = tasks("writer")
        cls.crc = cls.tasks["miniz-3.1.0-crc32"]["model"]
        cls.integer = cls.tasks["miniz-3.1.0-adler32"]["model"]
        cls.ordered = cls.tasks["musl-1.2.4-memcmp_sign"]["model"]

    def test_all_modules_import_without_external_jobs(self):
        import pkgutil
        import scguard

        names = [
            row.name for row in pkgutil.walk_packages(scguard.__path__, scguard.__name__ + ".")
        ]
        with patch("subprocess.run", side_effect=AssertionError("Unexpected external execution")):
            for name in names:
                importlib.import_module(name)

    def test_all_reference_models_have_valid_schemas(self):
        for row in list(self.tasks.values()) + list(self.writers.values()):
            core.validate_model(row["model"])

    def test_writer_model_decision_accepts_capacity_states(self):
        model = self.writers["libgrapheme-2.0.1"]["model"]
        state = {"x": 65, "cap": 8, "entry": [37] * 8}
        self.assertEqual(core.decide_model(model, model, state, state, "full"), "SUPPORT")

    def test_writer_model_decision_rejects_boolean_capacity(self):
        model = self.writers["libgrapheme-2.0.1"]["model"]
        state = {"x": 65, "cap": True, "entry": [37] * 8}
        self.assertEqual(core.decide_model(model, model, state, state, "full"), "UNKNOWN")

    def test_writer_export_matches_all_saved_guards(self):
        for folder in (DATA / "writer/guards").iterdir():
            if folder.is_dir():
                binding = read(folder / "binding.json")
                left, right = [self.writers[t["id"]]["model"] for t in binding["source_contracts"]]
                self.assertEqual(
                    core.export_guard(left, right), (folder / "guard.c").read_text(encoding="utf-8")
                )

    def test_latest_affine_emission_checker_rejects_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            code = core.affine.emit(self.crc)
            (folder / "contract.json").write_text(json.dumps(self.crc), encoding="utf-8")

            def seal(body):
                (folder / "summary.c").write_text(body, encoding="utf-8")
                (folder / "check.c").write_text(body, encoding="utf-8")
                record = {
                    key: hashlib.sha256((folder / filename).read_bytes()).hexdigest()
                    for filename, key in [
                        ("contract.json", "contract_sha256"),
                        ("summary.c", "summary_sha256"),
                        ("check.c", "check_sha256"),
                    ]
                }
                (folder / "candidate_seal.json").write_text(json.dumps(record), encoding="utf-8")

            seal(code)
            self.assertTrue(core.certificate.check_emission(folder)["all_checks_passed"])
            seal(code.replace("uint32_t o0=w0;", "uint32_t o0=(w0^1U);", 1))
            with self.assertRaises(ValueError):
                core.certificate.check_emission(folder)

    def test_boolean_configuration_is_rejected(self):
        s = {"x": 0, "cfg": True, "entry": [0] * 8}
        self.assertEqual(core.decide_model(self.crc, self.crc, s, s, "return"), "UNKNOWN")

    def test_boolean_entry_byte_is_rejected(self):
        s = {"x": 0, "cfg": 1, "entry": [False] * 8}
        self.assertFalse(core.valid_state(s))

    def test_invalid_observer_is_unknown(self):
        s = {"x": 0, "cfg": 0, "entry": [0] * 8}
        self.assertEqual(core.decide_model(self.crc, self.crc, s, s, "missing"), "UNKNOWN")

    def test_crc_kernel_has_checked_rank(self):
        result = core.build_kernel(self.crc, self.crc, 8, 8, "return")
        self.assertEqual(result["independent_check"]["rank"], 32)
        self.assertEqual(result["independent_check"]["free_pair_bits"], 160)

    def test_corrupted_reduction_certificate_is_rejected(self):
        result = core.build_kernel(self.crc, self.crc, 8, 8, "return")
        bad = copy.deepcopy(result["system"])
        bad["rows"][0] ^= 1
        with self.assertRaises(ValueError):
            core.certificate.check_reduction(result["original_rows"], bad)

    def test_self_xor_is_rejected_as_noninvertible(self):
        result = core.build_kernel(self.crc, self.crc, 8, 8, "return")
        bad = copy.deepcopy(result["system"])
        bad["operations"].append(["xor", 0, 0])
        with self.assertRaises(ValueError):
            core.certificate.check_reduction(result["original_rows"], bad)

    def test_typed_return_has_no_affine_rank(self):
        with self.assertRaises(ValueError):
            core.build_kernel(self.integer, self.integer, 8, 8, "return")

    def test_typed_model_byte_projection_has_a_kernel(self):
        result = core.build_kernel(self.integer, self.integer, 8, 8, "first4")
        self.assertEqual(result["independent_check"]["rank"], 32)

    def test_negative_integer_coefficient_is_rejected(self):
        bad = copy.deepcopy(self.integer)
        bad["cells"]["0"]["coefficients"][0] = -1
        with self.assertRaises(ValueError):
            core.mixed_check.model(bad)

    def test_prefix_emission_is_checked(self):
        result = core.prefix_check.check(self.integer, core.prefix.emit(self.integer))
        self.assertTrue(result["all_checks_passed"])

    def test_initial_lane_overflow_is_rejected(self):
        code = core.prefix.emit(self.integer)
        start = code.index("uint32_t lo=")
        end = code.index(";", start)
        bad = code[:start] + "uint32_t lo=65536U,hi=0U" + code[end:]
        with self.assertRaises(ValueError):
            core.prefix_check.check(self.integer, bad)

    def test_invalid_ordered_index_is_rejected(self):
        bad = copy.deepcopy(self.ordered)
        bad["cells"]["8"]["pairs"][0] = [0, 8]
        with self.assertRaises(ValueError):
            core.mixed_check.model(bad)

    def test_export_matches_saved_c_guards(self):
        for folder in (DATA / "cross_family/guards").iterdir():
            if folder.is_dir():
                binding = read(folder / "binding.json")
                left = self.tasks[binding["left"]["id"]]["model"]
                right = self.tasks[binding["right"]["id"]]["model"]
                self.assertEqual(
                    core.export_mixed_guard(left, right),
                    (folder / "guard.c").read_text(encoding="utf-8"),
                )

    def test_each_source_route_emits_actual_obligations(self):
        selections = [
            ("miniz-3.1.0-crc32", "direct"),
            ("miniz-3.1.0-crc32", "crc-step"),
            ("miniz-3.1.0-crc32", "crc-stream"),
            ("miniz-3.1.0-crc32", "crc-frame"),
            ("miniz-3.1.0-crc32", "crc-dfcc-step"),
            ("miniz-3.1.0-adler32", "adler-ranges"),
            ("miniz-3.1.0-adler32", "integer-prefix"),
            ("musl-1.2.4-memcmp_sign", "typed-conditional"),
            ("musl-1.2.4-memcmp_sign", "typed-bridge"),
        ]
        with patch("subprocess.run", side_effect=AssertionError("Harness generation must be pure")):
            for identity, route in selections:
                task = self.tasks[identity]
                code = core.source_harness(task["target"], task["model"], route)
                self.assertIn("#include", code)
                self.assertGreater(len(code), 100)
            task = self.writers["libgrapheme-2.0.1"]
            self.assertIn("target.byte7", core.source_harness(task["target"], task["model"]))


class FieldAdmissionTests(unittest.TestCase):
    def raw(self, return_failure=False, unsafe=False, missing=False):
        props = [
            {"description": "target.return", "status": "FAILURE" if return_failure else "SUCCESS"}
        ]
        props += [{"description": "target.byte" + str(i), "status": "SUCCESS"} for i in range(8)]
        if missing:
            props.pop()
        props.append({"description": "array bounds", "status": "FAILURE" if unsafe else "SUCCESS"})
        failed = unsafe or return_failure
        body = json.dumps(
            [{"result": props}, {"cProverStatus": "failure" if failed else "success"}]
        ).encode()
        folder = Path(self.folder.name)
        (folder / "CBMC.stdout.bin").write_bytes(body)
        (folder / "CBMC.stderr.txt").write_bytes(b"")
        receipt = {
            "timed_out": False,
            "exit_code": 10 if failed else 0,
            "stdout_sha256": hashlib.sha256(body).hexdigest(),
            "stderr_sha256": hashlib.sha256(b"").hexdigest(),
        }
        (folder / "CBMC.execution.json").write_text(json.dumps(receipt), encoding="utf-8")
        return core.field_reader.fields(folder, "CBMC", "cbmc")

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.folder.cleanup()

    def test_complete_safe_fields_are_admitted(self):
        result = self.raw()
        self.assertTrue(result["completed_safe"])
        self.assertEqual(result["fields"], ["SUPPORT"] * 9)

    def test_failed_return_preserves_checked_byte_fields(self):
        result = self.raw(return_failure=True)
        self.assertTrue(result["completed_safe"])
        self.assertEqual(result["fields"], ["REFUTE"] + ["SUPPORT"] * 8)

    def test_failed_safety_refuses_every_field(self):
        result = self.raw(unsafe=True)
        self.assertFalse(result["completed_safe"])
        self.assertEqual(result["fields"], ["UNKNOWN"] * 9)

    def test_missing_target_remains_unknown(self):
        result = self.raw(missing=True)
        self.assertFalse(result["completed_safe"])


if __name__ == "__main__":
    unittest.main()
