import unittest

import pandas as pd

from utils.calculations import calculate_eihwam, eihwam_weight


class EIHWAMWeightTests(unittest.TestCase):
    def test_level_weights_accept_numeric_levels(self):
        self.assertEqual(eihwam_weight(1, "ENGG1000"), 0)
        self.assertEqual(eihwam_weight(2, "ENGG2000"), 2)
        self.assertEqual(eihwam_weight(3, "ENGG3000"), 3)
        self.assertEqual(eihwam_weight(4, "ENGG4000"), 4)
        self.assertEqual(eihwam_weight(7, "ENGG7000"), 4)

    def test_thesis_name_overrides_level_four_weight(self):
        self.assertEqual(eihwam_weight(4, "AMME4000 Design Project"), 4)
        self.assertEqual(eihwam_weight(4, "AMME4000 Honours Thesis A"), 8)

    def test_eihwam_uses_thesis_weight_without_a_manual_weight_column(self):
        record = pd.DataFrame(
            {
                "Unit": ["ENGG1000", "ENGG2000", "ENGG3000", "AMME4000 Design", "AMME4000 Thesis"],
                "Level": [1, 2, 3, 4, 4],
                "CP": [6, 6, 6, 6, 6],
                "Mark": [99, 60, 70, 80, 90],
                "Status": ["Completed"] * 5,
            }
        )

        expected = (60 * 12 + 70 * 18 + 80 * 24 + 90 * 48) / (12 + 18 + 24 + 48)
        self.assertAlmostEqual(calculate_eihwam(record), expected)


if __name__ == "__main__":
    unittest.main()
