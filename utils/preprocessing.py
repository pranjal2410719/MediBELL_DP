import pandas as pd

from dp.ldp_mechanism import apply_laplace_ldp
from dp.gender_dp import encode_gender, dp_gender_series


# =================================================
# TRAINING (CSV)
# =================================================

def preprocess_with_dp(csv_path, epsilon=1.0, label_col="disease"):

    df = pd.read_csv(csv_path)

    X = df.drop(columns=[label_col])
    y = df[label_col]

    X_dp = apply_dp(X, epsilon)

    return X_dp, y


# =================================================
# SHARED CORE DP LOGIC
# =================================================

def apply_dp(X, epsilon):

    categorical_cols = ["gender"]
    numeric_cols = [c for c in X.columns if c not in categorical_cols]

    # numeric
    X_numeric = X[numeric_cols].astype(float)
    X_numeric_dp = apply_laplace_ldp(X_numeric, epsilon)

    # gender
    gender_encoded = X["gender"].apply(encode_gender)
    gender_dp = dp_gender_series(gender_encoded, epsilon)

    X_cat_dp = pd.DataFrame({"gender": gender_dp})

    X_dp = pd.concat(
        [X_numeric_dp.reset_index(drop=True),
         X_cat_dp.reset_index(drop=True)],
        axis=1
    )

    return X_dp
