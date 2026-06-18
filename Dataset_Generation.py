import pandas as pd
import numpy as np

np.random.seed(42)

# -------------------------------
# Define diseases (REAL LABELS)
# -------------------------------
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

N_SAMPLES = 250000  # 2.5 Lakhs (25L model)


def generate_sample(disease):
    """Generate one patient record based on disease"""

    base = {
        "fever": 0,
        "cough": 0,
        "fatigue": 0,
        "breathlessness": 0,
        "chest_pain": 0,
        "oxygen_level": np.random.randint(92, 100),
        "age": np.random.randint(10, 80),
        "gender": np.random.choice(["Male", "Female"])
    }

    # Disease-specific patterns
    if disease == "Pneumonia":
        base.update({
            "fever": 1,
            "cough": 1,
            "breathlessness": 1,
            "chest_pain": 1,
            "oxygen_level": np.random.randint(85, 92)
        })

    elif disease == "Asthma":
        base.update({
            "breathlessness": 1,
            "cough": 1
        })

    elif disease == "Influenza":
        base.update({
            "fever": 1,
            "fatigue": 1,
            "cough": 1
        })

    elif disease == "COVID-19":
        base.update({
            "fever": 1,
            "cough": 1,
            "fatigue": 1,
            "breathlessness": 1,
            "oxygen_level": np.random.randint(85, 93)
        })

    elif disease == "Tuberculosis":
        base.update({
            "cough": 1,
            "fatigue": 1,
            "chest_pain": 1
        })

    elif disease == "Bronchitis":
        base.update({
            "cough": 1,
            "fatigue": 1
        })

    elif disease == "Allergy":
        base.update({
            "cough": 1
        })

    elif disease == "Common Cold":
        base.update({
            "cough": 1,
            "fever": np.random.choice([0, 1])
        })

    base["disease"] = disease

    return base


def generate_dataset():
    data = []

    # Balanced distribution
    samples_per_class = N_SAMPLES // len(DISEASES)

    for disease in DISEASES:
        for _ in range(samples_per_class):
            data.append(generate_sample(disease))

    df = pd.DataFrame(data)

    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)

    return df


# -------------------------------
# Create multiple client datasets
# -------------------------------
def create_federated_clients(df):

    # Split into 3 clients (non-IID)
    client_1 = df[df["disease"].isin(["Pneumonia", "Asthma", "COVID-19"])]
    client_2 = df[df["disease"].isin(["Influenza", "Allergy", "Common Cold"])]
    client_3 = df[df["disease"].isin(["Bronchitis", "Tuberculosis", "COVID-19"])]

    client_1.to_csv("data/client_1.csv", index=False)
    client_2.to_csv("data/client_2.csv", index=False)
    client_3.to_csv("data/client_3.csv", index=False)

    print("Datasets generated:")
    print("Client 1:", client_1["disease"].value_counts())
    print("Client 2:", client_2["disease"].value_counts())
    print("Client 3:", client_3["disease"].value_counts())


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":

    df = generate_dataset()
    create_federated_clients(df)

    print("\nSample:")
    print(df.head())