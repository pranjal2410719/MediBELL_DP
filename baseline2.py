import pandas as pd
import os

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

print("RUNNING FILE:", os.path.abspath(__file__))

# ============================
# Load data
# ============================
#df = pd.read_csv("data/FINAL_DATABASE_MEDIBELL.csv")

try:
    df = pd.read_csv("data/FINAL_DATABASE_MEDIBELL.csv", encoding="latin-1")
except UnicodeDecodeError:
    try:
        df = pd.read_csv("data/FINAL_DATABASE_MEDIBELL.csv", encoding="utf-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv("data/FINAL_DATABASE_MEDIBELL.csv", encoding="cp1252") # or windows-1252
        except UnicodeDecodeError:
            print("Error: Could not decode CSV file.  Please investigate the file's encoding.")
            exit() # Exit if encoding cannot be determined

X = df.drop(columns=["disease"])
y = df["disease"]

categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numeric_cols = X.select_dtypes(exclude=["object"]).columns.tolist()

# ============================
# Model
# ============================
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("num", "passthrough", numeric_cols)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    ))
])

le = LabelEncoder()
y_enc = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc,
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
# Save per-class metrics
# ============================
report = classification_report(
    y_test,
    pred,
    target_names=le.classes_,
    output_dict=True
)

df_report = pd.DataFrame(report).transpose()

os.makedirs("models2", exist_ok=True)
df_report.to_csv("models2/baseline_report.csv")

# ============================
# Structured Output
# ============================
print("\n==============================")
print("MEDIBELL – BASELINE (NO DP)")
print("==============================")
print("Privacy           : None (Raw Data)")
print("Model             : RandomForest")
print(f"Test Accuracy     : {acc:.4f}")
print(f"Macro F1 Score    : {macro_f1:.4f}")
print(f"Macro Recall      : {macro_recall:.4f}")
print("Per-class metrics saved → models/baseline_report.csv")
print("==============================\n")
