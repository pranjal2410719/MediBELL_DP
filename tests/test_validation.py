import unittest
from utils.validation import validate_symptoms

class TestValidation(unittest.TestCase):

    def test_valid_input(self):
        symptoms = [0, 1, 0, 1]
        self.assertTrue(validate_symptoms(symptoms, 4))

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            validate_symptoms([0, 1], 4)

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            validate_symptoms([0, 2, 1, 0], 4)

if __name__ == "__main__":
    unittest.main()
