import pandas as pd
import joblib

from dp.ldp_mechanism import apply_ldp
from utils.validation import validate_symptoms

from utils.config_loader import load_config

config = load_config()
epsilon = config["privacy"]["epsilon"]

# load artifacts
model = joblib.load("models/disease_model.pkl")
le = joblib.load("models/label_encoder.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

# example patient input
new_patient = [
    1,0,1,0,1,0,0,1,0,0,
    1,0,0,1,0,1,0,0,1,0,
    0,1,0,0,1,0,1,0,0,1,
    0,0,1,0,1,0,0,1,0,0
]

# validate input
validate_symptoms(new_patient, len(feature_columns))

# convert to DataFrame
df_patient = pd.DataFrame(
    [new_patient],
    columns=feature_columns
)

# apply DP
epsilon = 1.0
df_patient_dp = apply_ldp(df_patient, epsilon)

# predict
pred = model.predict(df_patient_dp)
print("Predicted Disease:", le.inverse_transform(pred)[0])
