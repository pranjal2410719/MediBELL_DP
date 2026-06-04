import unittest
import pandas as pd
import joblib

from dp.ldp_mechanism import apply_ldp
from utils.validation import validate_symptoms

class TestPredictionPipeline(unittest.TestCase):

    def test_prediction_runs(self):
        model = joblib.load("models/disease_model.pkl")
        le = joblib.load("models/label_encoder.pkl")
        feature_columns = joblib.load("models/feature_columns.pkl")

        symptoms = [0] * len(feature_columns)
        validate_symptoms(symptoms, len(feature_columns))

        df = pd.DataFrame([symptoms], columns=feature_columns)
        df_dp = apply_ldp(df, epsilon=1.0)

        pred = model.predict(df_dp)
        disease = le.inverse_transform(pred)

        self.assertIsInstance(disease[0], str)

if __name__ == "__main__":
    unittest.main()
