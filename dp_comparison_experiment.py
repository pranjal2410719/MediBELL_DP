import matplotlib.pyplot as plt

from utils.preprocessing import preprocess_with_dp
from train_model2_dp import train_model2

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ===============================
# CONFIG
# ===============================
epsilons = [0.1, 0.5, 1.0, 2.0, 5.0]

dataset_1 = "data/synthetic_dataset_25k_40symptoms.csv"
dataset_2 = "data/MODEL_2_MediBELL.csv"


def train_model1_temp(data_path, epsilon):

    X, y = preprocess_with_dp(data_path, epsilon)

    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = X.select_dtypes(exclude=["object"]).columns.tolist()

    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols)
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced"
        ))
    ])

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, stratify=y_enc, random_state=42
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    return accuracy_score(y_test, pred) * 100


# ===============================
# RUN EXPERIMENT
# ===============================
acc_1 = []
acc_2 = []

for eps in epsilons:
    print("\n==============================")
    print(f"Running epsilon = {eps}")

    acc1 = train_model1_temp(dataset_1, eps)
    acc2 = train_model2(dataset_2, eps)

    acc_1.append(acc1)
    acc_2.append(acc2)

    print(f"Clinical Dataset Accuracy : {acc1:.4f}")
    print(f"Survey Dataset Accuracy   : {acc2:.4f}")



# ===============================
# PLOT
# ===============================
plt.figure()

plt.plot(epsilons, acc_1, marker='o')
plt.plot(epsilons, acc_2, marker='o')

plt.xlabel("Privacy Level (Epsilon)")
plt.ylabel("Accuracy (%)")
plt.title("Privacy vs Accuracy (Two Datasets)")
plt.legend(["Clinical Dataset", "Survey Dataset"])

plt.show()
