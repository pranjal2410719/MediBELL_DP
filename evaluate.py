import joblib
import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    recall_score,
    classification_report,
    confusion_matrix
)

from utils.preprocessing import preprocess_with_dp

print("RUNNING FILE:", os.path.abspath(__file__))

epsilon = 1.0
data_path = "data/synthetic_dataset_25k_40symptoms.csv"

# Load trained model
model = joblib.load("models/dp_model.pkl")
le = joblib.load("models/label_encoder.pkl")

# Load data
X_dp, y = preprocess_with_dp(data_path, epsilon)
y_enc = le.transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X_dp,
    y_enc,
    test_size=0.2,
    random_state=42,
    stratify=y_enc
)

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)
macro_f1 = f1_score(y_test, pred, average="macro")
macro_recall = recall_score(y_test, pred, average="macro")

print("\n==============================")
print("MEDIBELL – DP EVALUATION")
print("==============================")
print(f"Accuracy          : {acc:.4f}")
print(f"Macro F1          : {macro_f1:.4f}")
print(f"Macro Recall      : {macro_recall:.4f}")
print("\nPer-Class Report:\n")
print(classification_report(y_test, pred, target_names=le.classes_))
print("Confusion Matrix:\n")
print(confusion_matrix(y_test, pred))
print("==============================\n")
