import joblib
import pandas as pd
import os

from utils.preprocessing import apply_dp   # ⭐ MUST ADD


print("RUNNING FILE:", os.path.abspath(__file__))


# =================================================
# Load model + label encoder
# =================================================
model = joblib.load("models/dp_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

epsilon = 1.0   # SAME as training


# =================================================
# Helper input functions
# =================================================
def ask_int(prompt, default=0):
    val = input(f"{prompt} [default={default}]: ").strip()
    return int(val) if val != "" else default


def ask_choice(prompt, choices, default):
    val = input(f"{prompt} {choices} [default={default}]: ").strip().lower()
    return val if val in choices else default


print("\n=== IoT Health DP Prediction ===\n")


# =================================================
# Collect patient input
# =================================================
age = ask_int("Age", 40)
gender = ask_choice("Gender", ["male", "female"], "male")
smoker = ask_int("Smoker (0=no, 1=yes)", 0)

fever = ask_int("Fever severity (0–3)", 0)
cough = ask_int("Cough severity (0–3)", 0)
fatigue = ask_int("Fatigue severity (0–3)", 0)
shortness_of_breath = ask_int("Shortness of breath (0–3)", 0)
chest_pain = ask_int("Chest pain (0–3)", 0)
breathing_difficulty = ask_int("Breathing difficulty (0–3)", 0)


# =================================================
# Build feature vector
# =================================================
new_patient = {
    "age": age,
    "gender": gender,
    "smoker": smoker,
    "heart_rate": 80,
    "blood_pressure": 120,
    "cholesterol_level": 180,
    "fever": fever,
    "cough": cough,
    "fatigue": fatigue,
    "shortness_of_breath": shortness_of_breath,
    "headache": 0,
    "runny_nose": 0,
    "sore_throat": 0,
    "chest_pain": chest_pain,
    "body_ache": 0,
    "nausea": 0,
    "vomiting": 0,
    "diarrhea": 0,
    "dizziness": 0,
    "chills": 0,
    "loss_of_smell": 0,
    "loss_of_taste": 0,
    "wheezing": 0,
    "rash": 0,
    "eye_irritation": 0,
    "ear_pain": 0,
    "sweating": 0,
    "joint_pain": 0,
    "abdominal_pain": 0,
    "back_pain": 0,
    "blurred_vision": 0,
    "dry_cough": 0,
    "wet_cough": 0,
    "sinus_pressure": 0,
    "sneezing": 0,
    "rapid_heartbeat": 0,
    "slow_heartbeat": 0,
    "dehydration": 0,
    "loss_of_appetite": 0,
    "sleep_disturbance": 0,
    "anxiety": 0,
    "irritability": 0,
    "muscle_spasm": 0,
    "skin_redness": 0,
    "itchiness": 0,
    "breathing_difficulty": breathing_difficulty
}


df_new = pd.DataFrame([new_patient])


# =================================================
# APPLY SAME DP (CRITICAL STEP)
# =================================================
df_new_dp = apply_dp(df_new, epsilon)


# =================================================
# Predict
# =================================================
pred_encoded = model.predict(df_new_dp)[0]
pred_disease = label_encoder.inverse_transform([pred_encoded])[0]


print("\n=== Prediction Result ===")
print("Predicted disease:", pred_disease)
