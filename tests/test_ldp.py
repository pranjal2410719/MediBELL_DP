import unittest
import pandas as pd
import numpy as np

from dp.ldp_mechanism import randomized_response, apply_ldp

class TestLDPMechanism(unittest.TestCase):

    def test_randomized_response_binary_output(self):
        for _ in range(100):
            out = randomized_response(1, epsilon=1.0)
            self.assertIn(out, [0, 1])

    def test_randomized_response_invalid_epsilon(self):
        with self.assertRaises(ValueError):
            randomized_response(1, epsilon=0)

    def test_apply_ldp_shape_preserved(self):
        df = pd.DataFrame({
            "s1": [0, 1, 0, 1],
            "s2": [1, 1, 0, 0]
        })

        df_noisy = apply_ldp(df, epsilon=1.0)
        self.assertEqual(df.shape, df_noisy.shape)

if __name__ == "__main__":
    unittest.main()
