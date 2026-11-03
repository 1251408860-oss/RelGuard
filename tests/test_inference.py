import unittest
from scguard.inference.active import learn_writer
from scguard.inference.fit import infer_reference
from scguard.models import writer


class InferenceTests(unittest.TestCase):
    def test_current_affine_candidate_is_reconstructed(self):
        result = infer_reference("miniz-3.1.0-crc32")
        self.assertTrue(result["matches_recorded_candidate"])
        self.assertFalse(result["source_admission_performed"])

    def test_current_integer_candidate_is_reconstructed(self):
        self.assertTrue(infer_reference("miniz-3.1.0-adler32")["matches_recorded_candidate"])

    def test_current_ordered_candidate_is_reconstructed(self):
        self.assertTrue(infer_reference("musl-1.2.4-memcmp_sign")["matches_recorded_candidate"])

    def test_active_queries_close_sparse_feature_ambiguity(self):
        def oracle(capacity, x, entry):
            return 1, [128 | (x & 63)] + [entry] * 7

        points = [0, 256, 65536, writer.MAX_X]
        result = learn_writer([8], points, oracle)
        self.assertTrue(result["ambiguities_closed"])
        self.assertTrue(result["rounds"][0]["new_query_inputs"])
        for x in [1, 63, 64, 255, 65537, writer.MAX_X]:
            state = {"x": x, "cap": 8, "entry": [37] * 8}
            self.assertEqual(writer.image(result["model"], state), [1, 128 | (x & 63)] + [37] * 7)


if __name__ == "__main__":
    unittest.main()
