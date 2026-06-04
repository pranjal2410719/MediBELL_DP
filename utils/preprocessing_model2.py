import pandas as pd
from dp.ldp_mechanism import apply_laplace_ldp
from dp.gender_dp import encode_gender, dp_gender_series


def preprocess_model2(csv_path, epsilon):

    df = pd.read_csv(csv_path)

    print("\n=== BEFORE PROCESSING ===")
    print(df["disease"].value_counts())

    # -------------------------------
    # FIX 1: Ensure disease is string
    # -------------------------------
    df["disease"] = df["disease"].astype(str)

    # -------------------------------
    # FIX 2: Remove rare classes
    # -------------------------------
    counts = df["disease"].value_counts()
    df = df[df["disease"].isin(counts[counts >= 5].index)]

    # -------------------------------
    # FIX 3: Limit number of classes
    # -------------------------------
    top_classes = df["disease"].value_counts().nlargest(8).index
    df = df[df["disease"].isin(top_classes)]

    print("\n=== AFTER CLASS FILTERING ===")
    print(df["disease"].value_counts())

    # -------------------------------
    # Drop irrelevant columns
    # -------------------------------
    drop_cols = [
        "Device Name",
        "Suggestions for health wearable devices.",
        "Date_of_Birth",
        "Fireboult", "Fireboult.1", "Fireboult.2",
        "Fireboult.3", "Fireboult.4",
        "Fireboult.5", "Fireboult.6"
    ]

    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # -------------------------------
    # Encode categorical values
    # -------------------------------
    df = df.replace({"Yes": 1, "No": 0})
    df = df.replace({"Low": 0, "Moderate": 1, "High": 2})

    # -------------------------------
    # Split X, y (IMPORTANT)
    # -------------------------------
    X = df.drop(columns=["disease"])
    y = df["disease"]

    if y.nunique() < 2:
        raise ValueError("Dataset invalid: only one class after filtering")

    # -------------------------------
    # Identify columns
    # -------------------------------
    gender_col = None
    for col in X.columns:
        if col.lower() == "gender":
            gender_col = col
            break

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if gender_col in numeric_cols:
        numeric_cols.remove(gender_col)

    # -------------------------------
    # Apply DP ONLY on features
    # -------------------------------
    if numeric_cols:
        X_numeric = X[numeric_cols].astype(float)
        X_numeric_dp = apply_laplace_ldp(X_numeric, epsilon)
    else:
        X_numeric_dp = pd.DataFrame()

    if gender_col:
        gender_encoded = X[gender_col].apply(encode_gender)
        gender_dp = dp_gender_series(gender_encoded, epsilon)
        X_gender_dp = pd.DataFrame({gender_col: gender_dp})
    else:
        X_gender_dp = pd.DataFrame()

    other_cols = [
        col for col in X.columns
        if col not in numeric_cols and col != gender_col
    ]

    X_other = X[other_cols].reset_index(drop=True)

    X_final = pd.concat(
        [
            X_numeric_dp.reset_index(drop=True),
            X_gender_dp.reset_index(drop=True),
            X_other
        ],
        axis=1
    )

    print("\n=== FINAL LABEL DISTRIBUTION ===")
    print(y.value_counts())

    return X_final, y