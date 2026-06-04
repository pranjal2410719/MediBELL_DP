import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from utils.preprocessing import preprocess_with_dp


# ==================================================
# CONFIG
# ==================================================
epsilons = [0.1, 0.5, 1.0, 2.0, 5.0, 6.0]
baseline_accuracy = 0.9678  # No-DP baseline accuracy

dp_accuracies = []


# ==================================================
# RUN EXPERIMENT
# ==================================================
for eps in epsilons:

    print("\n==============================")
    print(f"Running epsilon = {eps}")

    X_dp, y = preprocess_with_dp(
        "data/synthetic_dataset_25k_40symptoms.csv",
        epsilon=eps
    )

    categorical_cols = ["gender"]
    numeric_cols = [c for c in X_dp.columns if c not in categorical_cols]

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    model = Pipeline(
        steps=[
            ("pre", ColumnTransformer([
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
                ("num", "passthrough", numeric_cols)
            ])),
            ("clf", RandomForestClassifier(
                n_estimators=150,
                random_state=42,
                n_jobs=-1
            ))
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X_dp, y_enc,
        test_size=0.2,
        random_state=42,
        stratify=y_enc
    )

    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    dp_accuracies.append(acc)

    print(f"Epsilon = {eps:.1f} → DP Accuracy = {acc:.4f}")


# ==================================================
# PREPARE DATA FOR PLOTTING
# ==================================================
dp_percent = [a * 100 for a in dp_accuracies]
baseline_percent = [baseline_accuracy * 100] * len(epsilons)

x = np.arange(len(epsilons))
width = 0.35


# ==================================================
# GROUPED BAR GRAPH
# ==================================================
plt.figure(figsize=(8, 5))

plt.bar(x - width/2, dp_percent, width, label="With DP")
plt.bar(x + width/2, baseline_percent, width, label="Without DP")

plt.xlabel("Epsilon (Privacy Level)")
plt.ylabel("Accuracy (%)")
plt.title("Privacy vs Accuracy Tradeoff")
plt.xticks(x, epsilons)
plt.ylim(0, 100)
plt.legend()

# Add value labels
for i, v in enumerate(dp_percent):
    plt.text(i - width/2, v + 1, f"{v:.1f}%", ha='center')

for i, v in enumerate(baseline_percent):
    plt.text(i + width/2, v + 1, f"{v:.1f}%", ha='center')

plt.tight_layout()
plt.show()
