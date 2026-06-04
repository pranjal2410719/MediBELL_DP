import joblib
import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    recall_score,
    classification_report
)

from utils.preprocessing import preprocess_with_dp

print("RUNNING FILE:", os.path.abspath(__file__))

epsilon = 1.0
data_path = "data/synthetic_dataset_25k_40symptoms.csv"

# ============================
# Load + DP
# ============================
X_dp, y = preprocess_with_dp(data_path, epsilon)

categorical_cols = ["gender"]
numeric_cols = [c for c in X_dp.columns if c not in categorical_cols]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced"
        ))
    ]
)

le = LabelEncoder()
y_enc = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X_dp,
    y_enc,
    test_size=0.2,
    random_state=42,
    stratify=y_enc
)

model.fit(X_train, y_train)
pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)
macro_f1 = f1_score(y_test, pred, average="macro")
macro_recall = recall_score(y_test, pred, average="macro")

# ============================
# Save model
# ============================
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/dp_model.pkl")
joblib.dump(le, "models/label_encoder.pkl")

# ============================
# Save per-class metrics
# ============================
report = classification_report(
    y_test,
    pred,
    target_names=le.classes_,
    output_dict=True
)

df_report = pd.DataFrame(report).transpose()
df_report.to_csv("models/dp_report.csv")

# ============================
# Structured Output
# ============================
print("\n==============================")
print("MEDIBELL – DP TRAINING RESULT")
print("==============================")
print(f"Epsilon           : {epsilon}")
print("Privacy           : Laplace + Randomized Response")
print("Model             : RandomForest (class_weight=balanced)")
print(f"Test Accuracy     : {acc:.4f}")
print(f"Macro F1 Score    : {macro_f1:.4f}")
print(f"Macro Recall      : {macro_recall:.4f}")
print("Per-class metrics saved → models/dp_report.csv")
print("Model Saved       : models/dp_model.pkl")
print("==============================\n")
