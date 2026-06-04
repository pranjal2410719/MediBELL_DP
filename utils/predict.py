import joblib
import pandas as pd
from utils.preprocessing_model2 import preprocess_model2


# -------------------------------
# Load Model (GLOBAL MODEL)
# -------------------------------
model = joblib.load("models/federated_model.pkl")


# -------------------------------
# Rule-Based Safety Layer
# -------------------------------
def rule_based_filter(row):

    # extreme temperature
    if row["temperature"] > 105:
        return "⚠️ Critical Fever (Check Immediately)"

    # only fever case
    if (
        row["fever"] == 1 and
        row["cough"] == 0 and
        row["breathlessness"] == 0
    ):
        return "Mild Fever / Viral Infection"

    return None


# -------------------------------
# Safe Prediction Function
# -------------------------------
def safe_predict(input_dict):

    df = pd.DataFrame([input_dict])

    # Step 1: Rule Check
    rule_result = rule_based_filter(input_dict)
    if rule_result is not None:
        return {
            "prediction": rule_result,
            "confidence": "rule-based"
        }

    # Step 2: Preprocess
    df.to_csv("temp_input.csv", index=False)
    X, _ = preprocess_model2("temp_input.csv", epsilon=1.0)

    # Step 3: Prediction
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]

    confidence = max(proba)

    return {
        "prediction": pred,
        "confidence": round(confidence, 2)
    }