import joblib
import pandas as pd
import os

from utils.preprocessing import apply_dp   # ⭐ IMPORTANT


print("RUNNING FILE:", os.path.abspath(__file__))


# ==================================================
# Load model + encoder
# ==================================================
model = joblib.load("models/dp_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")


epsilon = 1.0   # SAME epsilon used during training


# ==================================================
# New IoT patient data
# ==================================================
new_patient = {
    "age": 45,
    "gender": "female",
    "smoker": 0,
    "heart_rate": 88,
    "blood_pressure": 130,
    "cholesterol_level": 200,
    "fever": 2,
    "cough": 1,
    "fatigue": 2,
    "shortness_of_breath": 1,
    "headache": 0,
    "runny_nose": 0,
    "sore_throat": 0,
    "chest_pain": 0,
    "body_ache": 1,
    "nausea": 0,
    "vomiting": 0,
    "diarrhea": 0,
    "dizziness": 0,
    "chills": 1,
    "loss_of_smell": 0,
    "loss_of_taste": 0,
    "wheezing": 1,
    "rash": 0,
    "eye_irritation": 0,
    "ear_pain": 0,
    "sweating": 1,
    "joint_pain": 0,
    "abdominal_pain": 0,
    "back_pain": 0,
    "blurred_vision": 0,
    "dry_cough": 1,
    "wet_cough": 0,
    "sinus_pressure": 0,
    "sneezing": 0,
    "rapid_heartbeat": 1,
    "slow_heartbeat": 0,
    "dehydration": 0,
    "loss_of_appetite": 1,
    "sleep_disturbance": 1,
    "anxiety": 1,
    "irritability": 0,
    "muscle_spasm": 0,
    "skin_redness": 0,
    "itchiness": 0,
    "breathing_difficulty": 1
}


# ==================================================
# Convert to DataFrame
# ==================================================
df_new = pd.DataFrame([new_patient])


# ==================================================
# APPLY SAME DP (CRITICAL STEP)
# ==================================================
df_new_dp = apply_dp(df_new, epsilon)


# ==================================================
# Predict
# ==================================================
pred_encoded = model.predict(df_new_dp)[0]
pred_disease = label_encoder.inverse_transform([pred_encoded])[0]


print("Predicted disease (encoded):", pred_encoded)
print("Predicted disease (name):", pred_disease)
