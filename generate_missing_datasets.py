import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

np.random.seed(42)

# Ensure directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

# -------------------------------------------------
# 1. DEFINE DISEASES AND SYMPTOMS
# -------------------------------------------------
DISEASES = [
    "Common Cold",
    "Pneumonia",
    "Asthma",
    "Influenza",
    "Allergy",
    "COVID-19",
    "Bronchitis",
    "Tuberculosis"
]

SYMPTOMS = [
    "fever", "cough", "fatigue", "shortness_of_breath", "headache",
    "runny_nose", "sore_throat", "chest_pain", "body_ache", "nausea",
    "vomiting", "diarrhea", "dizziness", "chills", "loss_of_smell",
    "loss_of_taste", "wheezing", "rash", "eye_irritation", "ear_pain",
    "sweating", "joint_pain", "abdominal_pain", "back_pain", "blurred_vision",
    "dry_cough", "wet_cough", "sinus_pressure", "sneezing", "rapid_heartbeat",
    "slow_heartbeat", "dehydration", "loss_of_appetite", "sleep_disturbance",
    "anxiety", "irritability", "muscle_spasm", "skin_redness", "itchiness",
    "breathing_difficulty"
]

N_SAMPLES = 25000

# Helper to generate one realistic patient record
def generate_patient(disease):
    record = {
        "age": np.random.randint(10, 80),
        "gender": np.random.choice(["Male", "Female"]),
        "smoker": np.random.choice([0, 1], p=[0.7, 0.3]),
        "heart_rate": np.random.randint(60, 100),
        "blood_pressure": np.random.randint(90, 140),
        "cholesterol_level": np.random.randint(150, 260)
    }
    
    # Initialize all symptoms to 0/1 with low base probability
    for s in SYMPTOMS:
        record[s] = np.random.choice([0, 1], p=[0.95, 0.05])
        
    # Disease-specific characteristics
    if disease == "Common Cold":
        record.update({
            "cough": np.random.choice([0, 1], p=[0.1, 0.9]),
            "runny_nose": np.random.choice([0, 1], p=[0.1, 0.9]),
            "sneezing": np.random.choice([0, 1], p=[0.1, 0.9]),
            "sore_throat": np.random.choice([0, 1], p=[0.2, 0.8]),
            "fever": np.random.choice([0, 1], p=[0.7, 0.3])
        })
    elif disease == "Pneumonia":
        record.update({
            "fever": np.random.choice([0, 1], p=[0.1, 0.9]),
            "cough": np.random.choice([0, 1], p=[0.1, 0.9]),
            "shortness_of_breath": np.random.choice([0, 1], p=[0.2, 0.8]),
            "chest_pain": np.random.choice([0, 1], p=[0.3, 0.7]),
            "fatigue": np.random.choice([0, 1], p=[0.2, 0.8]),
            "heart_rate": np.random.randint(90, 120),
            "blood_pressure": np.random.randint(85, 110)
        })
    elif disease == "Asthma":
        record.update({
            "shortness_of_breath": np.random.choice([0, 1], p=[0.1, 0.9]),
            "wheezing": np.random.choice([0, 1], p=[0.1, 0.9]),
            "cough": np.random.choice([0, 1], p=[0.4, 0.6])
        })
    elif disease == "Influenza":
        record.update({
            "fever": np.random.choice([0, 1], p=[0.05, 0.95]),
            "fatigue": np.random.choice([0, 1], p=[0.1, 0.9]),
            "body_ache": np.random.choice([0, 1], p=[0.1, 0.9]),
            "chills": np.random.choice([0, 1], p=[0.15, 0.85]),
            "cough": np.random.choice([0, 1], p=[0.2, 0.8]),
            "headache": np.random.choice([0, 1], p=[0.25, 0.75])
        })
    elif disease == "Allergy":
        record.update({
            "sneezing": np.random.choice([0, 1], p=[0.1, 0.9]),
            "runny_nose": np.random.choice([0, 1], p=[0.1, 0.9]),
            "eye_irritation": np.random.choice([0, 1], p=[0.2, 0.8]),
            "itchiness": np.random.choice([0, 1], p=[0.2, 0.8])
        })
    elif disease == "COVID-19":
        record.update({
            "fever": np.random.choice([0, 1], p=[0.1, 0.9]),
            "cough": np.random.choice([0, 1], p=[0.1, 0.9]),
            "fatigue": np.random.choice([0, 1], p=[0.2, 0.8]),
            "shortness_of_breath": np.random.choice([0, 1], p=[0.2, 0.8]),
            "loss_of_smell": np.random.choice([0, 1], p=[0.15, 0.85]),
            "loss_of_taste": np.random.choice([0, 1], p=[0.15, 0.85]),
            "heart_rate": np.random.randint(90, 120)
        })
    elif disease == "Bronchitis":
        record.update({
            "cough": np.random.choice([0, 1], p=[0.05, 0.95]),
            "fatigue": np.random.choice([0, 1], p=[0.3, 0.7]),
            "chest_pain": np.random.choice([0, 1], p=[0.4, 0.6]),
            "wheezing": np.random.choice([0, 1], p=[0.3, 0.7])
        })
    elif disease == "Tuberculosis":
        record.update({
            "cough": np.random.choice([0, 1], p=[0.05, 0.95]),
            "fatigue": np.random.choice([0, 1], p=[0.2, 0.8]),
            "sweating": np.random.choice([0, 1], p=[0.3, 0.7]),
            "loss_of_appetite": np.random.choice([0, 1], p=[0.25, 0.75]),
            "chest_pain": np.random.choice([0, 1], p=[0.3, 0.7])
        })
        
    record["disease"] = disease
    return record

# -------------------------------------------------
# 2. GENERATE 25k CLINICAL DATASET
# -------------------------------------------------
print("Generating 25k clinical dataset...")
samples_per_class = N_SAMPLES // len(DISEASES)
data = []
for d in DISEASES:
    for _ in range(samples_per_class):
        data.append(generate_patient(d))

df = pd.DataFrame(data)
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("data/synthetic_dataset_25k_40symptoms.csv", index=False)
print("Saved data/synthetic_dataset_25k_40symptoms.csv")

# -------------------------------------------------
# 3. GENERATE SURVEY/MODEL 2 DATASETS
# -------------------------------------------------
print("Generating survey and final datasets...")
# MODEL_2_MediBELL.csv and FINAL_DATABASE_MEDIBELL.csv need to have extra columns dropped by preprocess_model2
df_survey = df.copy()

# Add columns that preprocess_model2 drops
df_survey["Device Name"] = np.random.choice(["Fitbit Luxe", "Apple Watch S9", "Garmin Venu"], size=len(df_survey))
df_survey["Suggestions for health wearable devices."] = "Check vitals regularly."
df_survey["Date_of_Birth"] = "1990-01-01"
for i in range(7):
    col = f"Fireboult.{i}" if i > 0 else "Fireboult"
    df_survey[col] = "N/A"

# Replace binary columns with "Yes"/"No" and "Low"/"Moderate"/"High" to test the mappings in preprocess_model2
# We map smoker to Yes/No
df_survey["smoker"] = df_survey["smoker"].replace({1: "Yes", 0: "No"})
# We map blood_pressure to Low/Moderate/High based on value ranges
df_survey["blood_pressure"] = pd.cut(
    df_survey["blood_pressure"],
    bins=[0, 100, 125, 200],
    labels=["Low", "Moderate", "High"]
).astype(str)

df_survey.to_csv("data/MODEL_2_MediBELL.csv", index=False)
df_survey.to_csv("data/FINAL_DATABASE_MEDIBELL.csv", index=False)
print("Saved data/MODEL_2_MediBELL.csv and data/FINAL_DATABASE_MEDIBELL.csv")

# -------------------------------------------------
# 4. TRAIN & SAVE BASELINE MODEL FOR PREDICT PIPELINE
# -------------------------------------------------
print("Training baseline RandomForest model on symptoms...")
X_symptoms = df[SYMPTOMS]
y = df["disease"]

le = LabelEncoder()
y_enc = le.fit_transform(y)

model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_symptoms, y_enc)

# Save artifacts
joblib.dump(model, "models/disease_model.pkl")
joblib.dump(le, "models/label_encoder.pkl")
joblib.dump(SYMPTOMS, "models/feature_columns.pkl")
print("Saved models/disease_model.pkl, label_encoder.pkl, and feature_columns.pkl")

# -------------------------------------------------
# 5. TRAIN & SAVE FEDERATED MODEL FOR APP.PY PREDICT
# -------------------------------------------------
print("Training federated model2 on survey dataset...")
from train_model2_dp import train_model2
model2, _ = train_model2("data/MODEL_2_MediBELL.csv", epsilon=10.0)
joblib.dump(model2, "models/federated_model.pkl")
print("Saved models/federated_model.pkl")

print("All missing datasets and models have been successfully generated and configured.")
