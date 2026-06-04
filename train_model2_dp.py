from utils.preprocessing_model2 import preprocess_model2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score


def train_model2(data_path, epsilon, global_model=None):

    X, y = preprocess_model2(data_path, epsilon)

    # dtype fix
    for col in X.columns:
        if X[col].dtype == "object":
            X[col] = X[col].astype(str)

    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", SimpleImputer(strategy="mean"), numeric_cols)
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

    if global_model is not None:
        model = global_model

    # SAFE SPLIT
    stratify = y if y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=stratify
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred) * 100

    return model, acc


def extract_weights(model):
    clf = model.named_steps["classifier"]
    return {
        "coef": clf.coef_,
        "intercept": clf.intercept_
    }


def load_weights(model, weights):
    clf = model.named_steps["classifier"]
    clf.coef_ = weights["coef"]
    clf.intercept_ = weights["intercept"]
    return model